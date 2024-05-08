from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLabel, QFileDialog, QTreeWidgetItem, QCheckBox
from PySide6.QtGui import QColor, QPixmap, QIcon, QColorConstants
import PySide6.QtCore as QtCore
from PySide6.QtCore import Qt
from ui_mainwindow import Ui_MainWindow
from py2saber import Saber_Controller, NoAnimaSaberException
from threadrunner import *
from dialogs import *
import version_compare as vc
import firmware
import color as Color
from enum import Enum, auto
import logging
import sys
import os
from asgiref.sync import sync_to_async
from AsyncioPySide6 import AsyncioPySide6
import asyncio
import platform
import resources_rc

script_version = '0.1'
script_authors = 'Jason Ramboz'
script_repo = 'https://github.com/jramboz/tintalle'

class SCStatus(Enum):
    '''Enum for saber connection status'''
    DISCONNECTED = auto()
    SEARCHING = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    NO_SABER = auto()

class Upload_Controller():
    '''Tracks state for mutli-file uploads.'''
    def __init__(self, files: list[str], display: File_Upload_Progress_Dialog, sc: Saber_Controller):
        self.files = files
        self.display = display
        self.sc = sc
        self.log = logging.getLogger()
        self.threadpool = QtCore.QThreadPool()

    def run(self):
        '''Initiate file upload.'''
        self._upload_next_file()

    def _upload_next_file(self):
        file = self.files.pop(0)
        self.log.info(f'Uploading file: {os.path.basename(file)}')
        self.log.debug(f'File path: {file}')
        self.display.fileNameLabel.setText(f'File: {os.path.basename(file)}')

        self.display.set_file_size(os.path.getsize(file))
        worker = Worker(self.sc.write_files_to_saber, [file])
        worker.signals.progress.connect(self.display.fileProgressBar.setValue)
        worker.signals.finished.connect(self._finished_callback)

        self.threadpool.start(worker)
    
    def _finished_callback(self):
        '''Function to upload the file and update the dialog. Set this as the finished callback to continue looping through the list.'''
        self.display.file_completed()

        if self.display.halt or len(self.files) == 0: #user has clicked cancel button or no more files left
            self.display.upload_complete()
            # this is kind of a hack and not great software design, but with the callbacks and all this seems to tbe the best place to put the reload
            AsyncioPySide6.runTask(self.display.parent().reload_saber_configuration())
        else:
            self._upload_next_file()
        

def getHumanReadableSize(size,precision=2):
    '''Takes a size in bytes and outputs human-readable string.'''
    # taken from https://stackoverflow.com/a/32009595
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size >= 1024 and suffixIndex < len(suffixes)-1:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])

class Main_Window(QMainWindow, Ui_MainWindow):
    sc: Saber_Controller = None
    saber_config: dict = None       # holds saber config loaded from saber
    files_dict: dict = None         # holds list of files loaded from saber
    saber_info: dict = None         # holds serial and version info
    space_info: dict = {'free' :0,  # holds free/used/total space information
                        'used': 0,
                        'total':0}
    current_config: dict = None     # holds saber config as modified in the GUI
    log = logging.getLogger()

    def __init__(self, *args, obj=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.threadpool = QtCore.QThreadPool()

        # Initialize logging
        self.logTextBox.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        self.log.addHandler(self.logTextBox)
        self.log.setLevel(logging.INFO)

        # Connect signals to slots
        self.connect_button.clicked.connect(self.connect_button_handler)
        self.action_Refresh_Ports.triggered.connect(self.update_ports)
        self.action_Show_Hide_Log.triggered.connect(self.show_hide_log_handler)
        self.action_Debug_Mode.triggered.connect(self.debug_mode_handler)
        self.action_Reload_Config.triggered.connect(self.reload_config_action_handler)
        self.action_about.triggered.connect(self.about_action_handler)
        
        self.action_Check_for_Latest_Firwmare.triggered.connect(self.fw_check_handler)
        self.action_Install_Firmware_from_File.triggered.connect(self.install_firmware_from_file_handler)

        self.r_slider.valueChanged.connect(self.color_change_handler)
        self.r_spinbox.valueChanged.connect(self.color_change_handler)
        self.g_slider.valueChanged.connect(self.color_change_handler)
        self.g_spinbox.valueChanged.connect(self.color_change_handler)
        self.b_slider.valueChanged.connect(self.color_change_handler)
        self.b_spinbox.valueChanged.connect(self.color_change_handler)
        self.w_slider.valueChanged.connect(self.color_change_handler)
        self.w_spinbox.valueChanged.connect(self.color_change_handler)

        self.color_bank_select_box.currentIndexChanged.connect(self.load_color_bank)
        self.main_radioButton.clicked.connect(self.selected_effect_changed)
        self.clash_radioButton.clicked.connect(self.selected_effect_changed)
        self.swing_radioButton.clicked.connect(self.selected_effect_changed)
        
        self.reset_color_changes_button.clicked.connect(self.reload_config_action_handler)
        self.color_save_button.clicked.connect(self.color_save_button_handler)
        self.preview_color_button.clicked.connect(self.preview_button_handler)
        self.erase_button.clicked.connect(self.erase_button_handler)
        self.upload_button.clicked.connect(self.upload_button_handler)
        self.sound_save_button.clicked.connect(self.sound_save_button_handler)
        self.reset_sound_changes_button.clicked.connect(self.reload_config_action_handler)

        self.files_treeWidget.itemSelectionChanged.connect(self.set_effects_checkboxes)

        for box in self.effects_buttonGroup.buttons():
            box.stateChanged.connect(self.update_sound_config)

        self.show()

        # Search for connected sabers
        self.display_connection_status(SCStatus.SEARCHING)
        self.update_ports()

    def about_action_handler(self):
        dlg = AboutDialog(script_version, script_authors, script_repo, self)
        dlg.exec()

    # --------------------------------- #
    # Saber connection handling methods #
    # --------------------------------- #

    def update_ports(self) -> None:
        '''Update the list of ports in saber_select_box'''
        self.saber_select_box.clear()
        self.display_connection_status(SCStatus.SEARCHING)
        ports = Saber_Controller.get_ports()
        if ports:
            for port in ports:
                if Saber_Controller.port_is_anima(port):
                    self.saber_select_box.addItem(port)
            self.display_connection_status(SCStatus.DISCONNECTED)
        else:
            self.display_connection_status(SCStatus.NO_SABER)
    
    def display_connection_status(self, status: SCStatus) -> None:
        '''Update the GUI to reflect the connection status'''
        if status == SCStatus.SEARCHING:
            self.saber_select_box.clear()
            self.connect_button.setEnabled(False)
            self.status_label.setText('SEARCHING...')
            self.set_ui_enabled(False)
        elif status == SCStatus.CONNECTED:
            self.connect_button.setEnabled(True)
            self.connect_button.setText('Disconnect')
            self.status_label.setText('CONNECTED')
            self.set_ui_enabled(True)
        elif status == SCStatus.CONNECTING:
            self.connect_button.setEnabled(False)
            self.status_label.setText('CONNECTING...')
            self.set_ui_enabled(False)
        elif status == SCStatus.DISCONNECTED:
            self.connect_button.setEnabled(True)
            self.connect_button.setText('Connect')
            self.status_label.setText('DISCONNECTED')
            self.set_ui_enabled(False)
        elif status == SCStatus.NO_SABER:
            self.connect_button.setEnabled(False)
            self.connect_button.setText('Connect')
            self.status_label.setText('No Saber Found')
            self.set_ui_enabled(False)
            self.saber_select_box.setEnabled(False)

    def set_ui_enabled(self, connected: bool = True) -> None:
        '''Enable or disable UI elements dependent on having a saber connected.''' 
        if connected:
            self.content_tabWidget.setEnabled(True)
            self.action_Reload_Config.setEnabled(True)
            self.saber_select_box.setEnabled(False)
        else: # disconnected
            # clear the contents
            self.clear_color_ui()
            self.clear_sound_ui()

            # disable tabs and  enable saber select
            self.content_tabWidget.setEnabled(False)
            self.action_Reload_Config.setEnabled(False)
            self.saber_select_box.setEnabled(True)

    def connect_button_handler(self):
        if self.sc: # if connected, disconnect
            self.disconnect_saber()
        else: # try to connect
            try:
                self.connect_saber()
            except NoAnimaSaberException:
                error_handler(NoAnimaSaberException(), parent=self)
                self.display_connection_status(SCStatus.DISCONNECTED)
    
    def connect_saber(self):
        '''Connect to a saber and perform initialization actions. Can also be used to refresh saber configuration.'''
        self.display_connection_status(SCStatus.CONNECTING)
        if not self.sc:
            port = self.saber_select_box.currentText()
            self.sc = Saber_Controller(port, gui=True, loglevel=self.log.getEffectiveLevel())
        
        # create a "loading" box while connecting
        w = Loading_Box(self, "Connecting to saber.")
        def _fin(event): # things to do once connection is complete
            self.display_connection_status(SCStatus.CONNECTED)
            self.log.info(f'Connected to saber.\nSerial Number: {self.saber_info["serial"]}\nFirmware version: {self.saber_info["version"]}')
        w.closeEvent = _fin
        w.show()

        AsyncioPySide6.runTask(self.reload_saber_configuration(w))

    async def reload_saber_configuration(self, w: QDialog = None):
        '''Reload the files list and configuration files from the saber.'''
        # display a "loading" dialog. One can be passed in, otherwise create one.
        if not w:
            w = Loading_Box(self, "Reading configuration from saber.")
            w.show()

        self.saber_config = eval(await sync_to_async(self.sc.read_config_ini)())
        self.current_config = self.saber_config
        self.log.debug(f'Retrieved config.ini:\n{self.saber_config}')
        self.files_dict = await sync_to_async(self.sc.list_files_on_saber)()
        self.log.debug(f'Retrieved files from saber:\n{self.files_dict}')
        self.saber_info = await sync_to_async(self.sc.get_saber_info)()
        self.log.debug(f'Retrieved saber info: {self.saber_info}')
        self.space_info['free'] = await sync_to_async(self.sc.get_free_space)()
        self.space_info['used'] = await sync_to_async(self.sc.get_used_space)()
        self.space_info['total'] = await sync_to_async(self.sc.get_total_space)()
        self.log.debug(f'Retrieved storage info: Free - {self.space_info['free']}\tUsed - {self.space_info['used']}\tTotal - {self.space_info['total']}')
        self.log.info('Successfully retrieved configuration from saber.')

        self.update_ui_with_config()

        w.close()

    def update_ui_with_config(self):
        '''Populates UI elements with the config data loaded from the saber.'''

        # Clear any displayed configuration
        self.clear_color_ui()
        self.clear_sound_ui()

        # Populate the list of color banks
        for i, x in enumerate(self.current_config['bank']):
            # create an icon that's just a box filled with the main blade color
            pixmap = QPixmap(self.color_bank_select_box.iconSize())
            pixmap.fill(QColor(*Color.get_mixed_color(*x['color'].values())))
            self.color_bank_select_box.addItem(QIcon(pixmap), f'Bank #{i+1}')
        activeBank = self.current_config['activeBank']
        self.color_bank_select_box.setCurrentIndex(activeBank)
        self.set_color_inputs_to_color(self.current_config['bank'][activeBank][self.get_selected_effect()])

        # Populate sound files list
        items = []
        
        for name, size in self.files_dict.items():
            items.append(QTreeWidgetItem([name, str(size)]))
        
        # Check for any missing files that config.ini expects
        config_files = []
        for effect in self.current_config['sounds'].keys():
            if effect == 'soundengine': continue # just skip this one. Not sure what it's for, but it isn't an effect
            config_files += self.current_config['sounds'][effect]
        config_files = list(set(config_files)) #remove duplicates
        missing_files = [i for i in config_files if i not in self.files_dict.keys()] # filter to only items that are not in the files list
        self.log.debug(f'Config.ini expects these files, but they are not present on the saber: {missing_files}')

        for file in missing_files:
            item = QTreeWidgetItem([file, '0'])
            for i in [0, 1]:
                font = item.font(i)
                font.setItalic(True)
                #brush = item.foreground(i)
                # brush.setColor(QColor('red'))
                item.setFont(i, font)
                item.setForeground(i, QColor('red'))
            items.append(item)

        self.files_treeWidget.insertTopLevelItems(0, items)
        self.files_treeWidget.sortItems(0, Qt.SortOrder.AscendingOrder)
        self.files_treeWidget.resizeColumnToContents(0)
        self.files_treeWidget.setCurrentItem(self.files_treeWidget.topLevelItem(0))

        # Display space usage
        self.freespace_label.setText('Free Space: ' + getHumanReadableSize(self.space_info['free']))
        self.usedspace_label.setText('Used Space: ' + getHumanReadableSize(self.space_info['used']))
        self.totalspace_label.setText('Total Space: ' + getHumanReadableSize(self.space_info['total']))

    def disconnect_saber(self):
        '''Disconnect saber and perform any necessary cleanup'''
        self.sc = None
        self.display_connection_status(SCStatus.DISCONNECTED)

    def reload_config_action_handler(self):
        button = QMessageBox.warning(
            self,
            "Reload Configuration?",
            "WARNING! This will reset any unsaved configuration changes.\n\nDo you want to continue?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No
        )

        if button == QMessageBox.Yes:
            AsyncioPySide6.runTask(self.reload_saber_configuration())

    # ------------------------- #
    # Logging and debug methods #
    # ------------------------- #

    def show_hide_log_handler(self):
        if self.logTextBox.isVisible():
            self.logTextBox.hide()
        else:
            self.logTextBox.show()
    
    def debug_mode_handler(self, enabled: bool):
        if enabled:
            self.log.setLevel(logging.DEBUG)
            if self.sc:
                self.sc.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
            if self.sc:
                self.sc.log.setLevel(logging.INFO)

    # --------------------------- #
    # Sound file handling methods #
    # --------------------------- #

    def erase_button_handler(self):
        button = QMessageBox.warning(
            self,
            "Erase All Sound Files?",
            "WARNING! This will erase all sound files on the saber. You will need to upload all files again.\n\nDo you want to continue?",
            buttons=QMessageBox.Ok | QMessageBox.Cancel,
            defaultButton=QMessageBox.Cancel
        )

        if button == QMessageBox.Ok:
            self.log.info("Erasing all files on connected saber.")
            
            #set up thread
            pd = Progress_Dialog(parent=self, title="Erasing Saber", message="Erasing all sound files on saber.")
            worker = Worker(self.sc.erase_all_files)

            def f():
                '''Actions to do when task is finished.'''
                pd.finished()
                AsyncioPySide6.runTask(self.reload_saber_configuration())

            def e(error: tuple):
                '''What to do with an error.'''
                pd.report("An error has occurred. See the log for details.")
                error_handler(e, parent=self)

            def r(obj: object):
                '''What to do with task result.'''
                pd.report("All sound files on saber have been erased.\nPlease re-load your sound files.")
                self.log.info("All sound files on saber have been erased. Please re-load your sound files.")

            worker.signals.finished.connect(f)
            worker.signals.error.connect(e)
            worker.signals.result.connect(r)
            worker.signals.progress.connect(pd.progressBar.setValue)

            # execute thread and show progress dialog
            pd.show()
            self.threadpool.start(worker)

    uc: Upload_Controller = None
    def upload_button_handler(self):
        # Get a list of files to upload. Can be one file or multiple files
        files = QFileDialog.getOpenFileNames(self, filter="RAW Sound File (*.RAW)")[0]
        self.log.debug(f'List of files to upload: {files}')
        
        if(files):
            # Create the file upload progress dialog
            if len(files) == 1:
                display = File_Upload_Progress_Dialog(parent=self)
            else:
                display = File_Upload_Progress_Dialog(parent=self, multifile=True)
                display.set_num_files(len(files))
            display.show()
            
            # Create and run the upload controller
            self.uc = Upload_Controller(files, display, self.sc)
            #TODO: Use worker to run in thread, then refresh files display when finished
            try:
                self.uc.run()
            except Exception as e:
                error_handler(e, parent=self)

    def clear_sound_ui(self):
        for box in self.effects_buttonGroup.buttons():
            box.blockSignals(True)
            box.setChecked(False)
            box.blockSignals(False)
        self.files_treeWidget.clear()

    @staticmethod
    def get_effect_for_checkBox(box: QCheckBox) -> str:
        '''Returns the sound effect name that corresponds to the specified checkbox.'''
        match box.text():
            case 'Power On':
                return 'on'
            case 'Power Off':
                return 'off'
            case 'Hum':
                return 'hum'
            case 'Clash':
                return 'clash'
            case 'Swing':
                return 'swing'
            case 'SmoothSwing A':
                return 'smoothSwingA'
            case 'SmoothSwing B':
                return 'smoothSwingB'
            case _:
                return ''

    def set_effects_checkboxes(self):
        '''Set the effects checkboxes based on the currently selected sound file.'''
        file = self.files_treeWidget.selectedItems()[0].data(0, Qt.ItemDataRole.DisplayRole) if self.files_treeWidget.selectedItems() else ''
        for box in self.effects_buttonGroup.buttons():
            box.blockSignals(True)
            effect = self.get_effect_for_checkBox(box)
            if effect in self.current_config['sounds']:
                box.setChecked(file in self.current_config['sounds'][effect])
            box.blockSignals(False)
    
    def update_sound_config(self, s: Qt.CheckState):
        '''Update the current sound configuration to add or remove the selected filename from the list for the effect.'''
        box = self.sender()
        effect = self.get_effect_for_checkBox(box)
        filename = self.files_treeWidget.selectedItems()[0].text(0)
        state = Qt.CheckState(s)
        if state == Qt.CheckState.Checked:
            self.log.debug(f'Adding file {filename} to effect {effect}.')
            if effect not in self.current_config['sounds'].keys():
                self.current_config['sounds'][effect] = []
            self.current_config['sounds'][effect].append(filename)
            self.current_config['sounds'][effect].sort()
        elif state == Qt.CheckState.Unchecked:
            self.log.debug(f'Removing file {filename} from effect {effect}.')
            self.current_config['sounds'][effect].remove(filename)
        self.log.debug(f'Updated list for effect {effect}: {self.current_config['sounds'][effect]}')

    def sound_save_button_handler(self):
        '''Write the sound file effect settings to the saber.'''
        w = Loading_Box(self, "Saving configuration to saber.")
        w.show()

        async def _save_sound_settings(self, w):
            for effect, files in self.current_config['sounds'].items():
                if effect == 'soundengine': continue
                self.log.info(f'Setting sounds for effect: {effect}')
                self.sc.set_sounds_for_effect(effect, files)
                await asyncio.sleep(2)
            AsyncioPySide6.runTask(self.reload_saber_configuration(w))

        AsyncioPySide6.runTask(_save_sound_settings(self, w))

    # ------------------------- #
    # Firmware handling methods #
    # ------------------------- #

    def anima_is_NXT(self):
        if self.saber_info['version'][:4] == 'NXT_':
            return True
        return False
    
    def display_NXT_warning(self):
        self.log.info('Your saber appears to be an Anima NXT. Tintallë does not support firmware uploads for Anima NXT at this time.')
        dlg = QMessageBox(QMessageBox.Information, 'Information', 'Anima NXT Detected', QMessageBox.Ok, self)
        dlg.setInformativeText('Your saber appears to be an Anima NXT. Tintallë does not support firmware uploads for Anima NXT at this time.')
        dlg.exec()

    def fw_check_handler(self):
        if self.anima_is_NXT():
            self.display_NXT_warning()
            return

        self.log.info('Checking for latest OpenCore firwmare.')
        fw_info = firmware.check_latest_fw_release()
        self.log.debug(f'Firmware info retrieved: {fw_info}')

        # if a saber is connected, compare to installed FW version
        if (self.saber_info): #TODO: store an actual connection state that can be checked
            self.log.debug('Comparing to latest firmware to version installed on connected saber.')
            self.log.debug(f'Installed version: {self.saber_info["version"]}, Latest version: {fw_info[0]}')
            if vc.is_higher(fw_info[0], self.saber_info['version']):
                # Display message and prompt to download/install newer version
                self.log.info(f'Newer official firmware available: v{fw_info[0]}')
                r = QMessageBox.question(self, 'New Firmware Available', f'New OpenCore firmware available: v{fw_info[0]}. Would you like to install it?', QMessageBox.Yes | QMessageBox.No)
                
                if r == QMessageBox.Yes:
                    try:
                        filename = firmware.download_fw(self, url=fw_info[1])
                        firmware.upload_firmware(filename, self)
                    except Exception as e:
                        error_handler(e, parent=self)
            else:
                # Display message
                self.log.info('No newer firmware available.')
                dlg = QMessageBox(QMessageBox.Information, 'Information', 'No newer firmware available.', QMessageBox.Ok, self)
                dlg.setInformativeText(f'There is no newer firmware than the one currently installed on your saber. The latest official OpenCore release is v{fw_info[0]}')
                dlg.exec()
                
        else: # no saber connected, display the latest version and offer to download
            dlg = QMessageBox(self)
            dlg.setText(f'The latest official OpenCore release is v{fw_info[0]}')
            dlg.setInformativeText('Click the Save button to download a copy.')
            dlg.setIcon(QMessageBox.Information)
            dlg.setStandardButtons(QMessageBox.Save | QMessageBox.Close)
            dlg.setDefaultButton(QMessageBox.Close)
            r = dlg.exec()

            if r == QMessageBox.Save:
                firmware.prompt_for_location_and_download_fw(self, url=fw_info[1])

    def install_firmware_from_file_handler(self):
        if self.anima_is_NXT():
            self.display_NXT_warning()
            return
        
        fw_file = QFileDialog.getOpenFileName(self, caption='Open Firmware File', filter='OpenCore Firwmare File (*.hex)')[0]
        if fw_file:
            try:
                firmware.upload_firmware(fw_file, self)
            except Exception as e:
                error_handler(e, parent=self)
    
    # ---------------------- #
    # Color handling methods #
    # ---------------------- #
    
    def load_color_bank(self, index: int):
        '''Load color info from specified color bank index into GUI'''
        bank = self.current_config['bank'][index]
        for effect, color in bank.items():
            self.display_color_preview(effect, color)
        self.current_config['activeBank'] = index
        self.set_color_inputs_to_color(self.current_config['bank'][index][self.get_selected_effect()])
    
    def set_color_inputs_to_color(self, color: dict):
        self.r_spinbox.setValue(color["red"])
        self.g_spinbox.setValue(color["green"])
        self.b_spinbox.setValue(color["blue"])
        self.w_spinbox.setValue(color["white"])
    
    def display_color_preview(self, effect: str, color: dict):
        box = self._get_box_for_effect(effect)
        p = box.palette()
        p.setColor(box.backgroundRole(), QColor(*Color.get_mixed_color(*color.values())))
        box.setPalette(p)

    def clear_color_ui(self):
        '''Clear and reset all color UI settings.'''
        self.color_bank_select_box.clear()
        self.r_spinbox.setValue(0)
        self.g_spinbox.setValue(0)
        self.b_spinbox.setValue(0)
        self.w_spinbox.setValue(0)
        self.main_radioButton.setChecked(True)
        p = QApplication.palette()
        self.main_color_label.setPalette(p)
        self.clash_color_label.setPalette(p)
        self.swing_color_label.setPalette(p)

    def get_selected_effect(self) -> str:
        '''Returns a string corresponding to which effect radio box is selected.
        Possible return values are "color", "clash", and "swing".'''
        if self.main_radioButton.isChecked():
            return "color"
        elif self.clash_radioButton.isChecked():
            return "clash"
        elif self.swing_radioButton.isChecked():
            return "swing"
        return "" # This shouldn't ever happen
    
    def selected_effect_changed(self):
        '''Sets the sliders to the proper values when user switches the active effect.'''
        # Yeah, I could do this as one line, but this is easier to read
        effect = self.get_selected_effect()
        bank = self.color_bank_select_box.currentIndex()
        color = self.current_config['bank'][bank][effect]
        self.set_color_inputs_to_color(color)

    def _get_box_for_effect(self, effect: str) -> QLabel:
        match effect:
            case "color":
                return self.main_color_label
            case "clash":
                return self.clash_color_label
            case "swing":
                return self.swing_color_label
            case _:
                return

    def color_change_handler(self, value: int):
        '''Handle value changed in the color specifier'''
        match self.sender():
            case self.r_slider | self.r_spinbox:
                self.r_slider.setValue(value)
                self.r_spinbox.setValue(value)
            case self.g_slider | self.g_spinbox:
                self.g_slider.setValue(value)
                self.g_spinbox.setValue(value)
            case self.b_slider | self.b_spinbox:
                self.b_slider.setValue(value)
                self.b_spinbox.setValue(value)
            case self.w_slider | self.w_spinbox:
                self.w_slider.setValue(value)
                self.w_spinbox.setValue(value)
        
        self.update_current_config_from_gui()
        self.update_color_display()

    def update_color_display(self):
        '''Update the color preview display based on the color specified in the GUI state'''
        effect = self.get_selected_effect()
        color = self.get_current_color()
        self.display_color_preview(effect, color)

    def get_current_color(self) -> dict:
        '''Returns a color dict with the current valuse set in the GUI'''
        return {
            "red": self.r_spinbox.value(),
            "green": self.g_spinbox.value(),
            "blue": self.b_spinbox.value(),
            "white": self.w_spinbox.value()
        }
    
    def preview_color_on_saber(self, color: dict):
        '''Send the specified color to the saber for preview.'''
        self.log.debug(f'Previewing color: {color}')
        self.sc.preview_color(*color.values())

    def preview_button_handler(self):
        self.log.info('Previewing color on saber.')
        self.preview_color_on_saber(self.get_current_color())

    def update_current_config_from_gui(self):
        '''Updates the stored configuration when the GUI elements are changed.'''
        self.current_config['activeBank'] = self.color_bank_select_box.currentIndex() +1
        color = self.get_current_color()
        self.current_config['bank'][self.color_bank_select_box.currentIndex()][self.get_selected_effect()] = color

    def color_save_button_handler(self):
        '''Write the values of the currently displayed bank to the saber.'''
        w = Loading_Box(self, "Saving configuration to saber.")
        w.show()

        i = self.color_bank_select_box.currentIndex()
        self.log.info(f'Saving color bank #{i+1} to saber.')
        m_color = self.current_config['bank'][i]['color']
        cl_color = self.current_config['bank'][i]['clash']
        s_color = self.current_config['bank'][i]['swing']
        self.log.debug(f'Main color: {m_color}\nClash color: {cl_color}\nSwing color: {s_color}')

        try:
            AsyncioPySide6.runTask(self._set_colors(i, m_color, cl_color, s_color, w))
        except Exception as e:
            error_handler(e)
    
    async def _set_colors(self, bank: int, m_color: dict, cl_color: dict, s_color:dict, w: QDialog = None):
        try:
            await sync_to_async(self.sc.set_color)(bank, "color", m_color['red'], m_color['green'], m_color['blue'], m_color['white'])
            await sync_to_async(self.sc.set_color)(bank, "clash", cl_color['red'], cl_color['green'], cl_color['blue'], cl_color['white'])
            await sync_to_async(self.sc.set_color)(bank, "swing", s_color['red'], s_color['green'], s_color['blue'], s_color['white'])
            await sync_to_async(self.sc.set_active_bank)(bank)
        except Exception as e:
            error_handler(e)
        finally:
            AsyncioPySide6.runTask(self.reload_saber_configuration(w))

# set icon for Windows - from https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/#building-a-windows-installer-with-installforge
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'com.sublunarysphere.tintalle.' + script_version
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    app = QApplication(sys.argv)
    if platform.system == "Windows":
        icon = ':/img/tintalle.ico'
    else:
        icon = ':/img/tintalle.png'
    app.setWindowIcon(QIcon(':/img/tintalle.png'))
    with AsyncioPySide6.use_asyncio():
        mainwindow = Main_Window()

        app.exec()
