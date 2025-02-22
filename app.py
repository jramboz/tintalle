from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLabel, QFileDialog, QTreeWidgetItem, QCheckBox
from PySide6.QtGui import QColor, QPixmap, QIcon, QColorConstants
import PySide6.QtCore as QtCore
from PySide6.QtCore import Qt
from PySide6 import QtAsyncio
from ui_mainwindow import Ui_MainWindow
from py2saber import Saber_Controller, NoAnimaSaberException, InvalidSaberResponseException
from threadrunner import *
from dialogs import *
from animaterminal import AnimaTerminalWindow
import version_compare as vc
import firmware
import color as Color
from enum import Enum, auto
import logging
import sys
import os
import asyncio
import platform
import resources_rc
from datetime import datetime
from copy import deepcopy
import json
import glob

script_version = '0.6.1'
script_authors = 'Jason Ramboz'
script_repo = 'https://github.com/jramboz/tintalle'

# Get the directory for where resources are stored
# We have to do some tricks to get it on Mac, because of the .app structure
if platform.system() == 'Darwin':
    resourcedir = os.path.sep.join(sys.argv[0].split(os.path.sep)[:-1])
    # Check if running inside a .app package
    if resourcedir.endswith('MacOS'):
        contentsdir = os.path.sep.join(resourcedir.split(os.path.sep)[:-1])
        resourcedir = os.path.join(contentsdir, 'Resources')
    else: # Not in an app, regular method works fine
        resourcedir = os.path.dirname(__file__)
else:
    resourcedir = os.path.dirname(__file__)

class SCStatus(Enum):
    '''Enum for saber connection status'''
    DISCONNECTED = auto()
    SEARCHING = auto()
    CONNECTING = auto()
    CONNECTED = auto()
    NO_SABER = auto()


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
        self.connect_button.clicked.connect(lambda: asyncio.ensure_future(self.connect_button_handler()))
        self.action_Refresh_Ports.triggered.connect(lambda: asyncio.ensure_future(self.update_ports()))
        self.action_Show_Hide_Log.triggered.connect(self.show_hide_log_handler)
        self.action_Debug_Mode.triggered.connect(self.debug_mode_handler)
        self.action_Reload_Config.triggered.connect(self.reload_config_action_handler)
        self.action_about.triggered.connect(self.about_action_handler)
        self.action_Save_Log_to_File.triggered.connect(self.save_log_to_file_action_handler)
        self.action_Export_Anima_config_ini.triggered.connect(self.export_anima_config_ini_action_handler)
        self.action_Save_Colors.triggered.connect(self.save_colors_action_handler)
        self.action_Load_Colors.triggered.connect(self.load_colors_action_handler)
        self.action_Reset_Saber_to_Defaults.triggered.connect(self.reset_saber_to_defaults_action_handler)
        self.action_Anima_Terminal.triggered.connect(self.anima_terminal_action_handler)
        
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
        self.save_all_banks_button.clicked.connect(self.save_all_colors_button_handler)
        self.preview_color_button.clicked.connect(self.preview_button_handler)
        self.erase_button.clicked.connect(self.erase_button_handler)
        self.upload_button.clicked.connect(self.upload_button_handler)
        self.sound_save_button.clicked.connect(self.sound_save_button_handler)
        self.reset_sound_changes_button.clicked.connect(self.reload_config_action_handler)
        self.auto_assign_effects_button.clicked.connect(self.auto_assign_effects_button_handler)

        self.files_treeWidget.itemSelectionChanged.connect(self.set_effects_checkboxes)

        for box in self.effects_buttonGroup.buttons():
            box.stateChanged.connect(self.update_sound_config)

        self.show()

        # Search for connected sabers
        self.display_connection_status(SCStatus.SEARCHING)
        # Even though I'm running this in the context of QtAsyncio.run(), it seems that it doesn't
        # start its own loop until _after_ the Main_Window is finished its __init__. So I have to 
        # use asyncio.run() here instead of asyncio.ensure_future() to start up the loop.
        # After this, everything else should be okay to use asyncio.ensure_future()
        asyncio.run(self.update_ports())

    def about_action_handler(self):
        dlg = AboutDialog(script_version, script_authors, script_repo, self)
        dlg.exec()
    
    async def _close_window(self):
        '''When window is about to close, disconnect Anima first. This will also check for unsaved changes.'''
        # Try to disconnect, prompt to save changes if applicable
        await self.disconnect_saber()
        if not self.sc:  # if disconnect was successful, continue with close
            self.close()

    def closeEvent(self, event):
        if self.sc:
            # If connected, wait for disconnect
            asyncio.ensure_future(self._close_window())
            event.ignore()
        else:
            super().closeEvent(event)

    # --------------------------------- #
    # Saber connection handling methods #
    # --------------------------------- #

    async def update_ports(self) -> None:
        '''Update the list of ports in saber_select_box'''
        self.saber_select_box.clear()
        self.display_connection_status(SCStatus.SEARCHING)
        ports = await Saber_Controller.get_anima_ports()
        if ports:
            for port in ports:
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
            self.action_Refresh_Ports.setEnabled(False)
            self.refresh_ports_button.setEnabled(False)
            self.action_Export_Anima_config_ini.setEnabled(True)
            self.action_Reset_Saber_to_Defaults.setEnabled(True)
            self.action_Save_Colors.setEnabled(True)
            self.action_Load_Colors.setEnabled(True)
            self.action_Anima_Terminal.setEnabled(True)
        else: # disconnected
            # clear the contents
            self.clear_color_ui()
            self.clear_sound_ui()

            # disable tabs and  enable saber select
            self.content_tabWidget.setEnabled(False)
            self.action_Reload_Config.setEnabled(False)
            self.saber_select_box.setEnabled(True)
            self.action_Refresh_Ports.setEnabled(True)
            self.refresh_ports_button.setEnabled(True)
            self.action_Export_Anima_config_ini.setEnabled(False)
            self.action_Reset_Saber_to_Defaults.setEnabled(False)
            self.action_Save_Colors.setEnabled(False)
            self.action_Load_Colors.setEnabled(False)
            self.action_Anima_Terminal.setEnabled(False)

    async def connect_button_handler(self):
        if self.sc: # if connected, disconnect
            await self.disconnect_saber()
        else: # try to connect
            try:
                await self.connect_saber()
            except NoAnimaSaberException:
                error_handler(NoAnimaSaberException(), parent=self)
                self.display_connection_status(SCStatus.DISCONNECTED)
    
    async def connect_saber(self):
        '''Connect to a saber and perform initialization actions. Can also be used to refresh saber configuration.'''
        self.display_connection_status(SCStatus.CONNECTING)
        if not self.sc:
            port = self.saber_select_box.currentText()
            self.sc = await Saber_Controller.create(port, gui=True, loglevel=self.log.getEffectiveLevel())
        
        # create a "loading" box while connecting
        w = Loading_Box(self, "Connecting to saber.")
        def _fin(event): # things to do once connection is complete
            if self.saber_config:
                self.display_connection_status(SCStatus.CONNECTED)
                self.log.info(f'Connected to saber.\nSerial Number: {self.saber_info["serial"]}\nFirmware version: {self.saber_info["version"]}')
        w.closeEvent = _fin
        w.show()

        asyncio.ensure_future(self.reload_saber_configuration(w))

    async def reload_saber_configuration(self, w: QDialog = None):
        '''Reload the files list and configuration files from the saber.'''
        # display a "loading" dialog. One can be passed in, otherwise create one.
        if not w:
            w = Loading_Box(self, "Reading configuration from saber.")
            w.show()

        self.set_ui_enabled(False)
        self.saber_config = {}

        try:
            # TODO: make timeout customizable in settings
            self.saber_config = eval(await asyncio.wait_for(self.sc.read_config_ini(), timeout=10))
            self.current_config = deepcopy(self.saber_config)
            self.log.debug(f'Retrieved config.ini:\n{self.saber_config}')
            self.files_dict = await self.sc.list_files_on_saber()
            self.log.debug(f'Retrieved files from saber:\n{self.files_dict}')
            self.saber_info = await self.sc.get_saber_info()
            self.log.debug(f'Retrieved saber info: {self.saber_info}')
            self.space_info['free'] = await self.sc.get_free_space()
            self.space_info['used'] = await self.sc.get_used_space()
            self.space_info['total'] = await self.sc.get_total_space()
            self.log.debug(f'Retrieved storage info: Free - {self.space_info['free']}\tUsed - {self.space_info['used']}\tTotal - {self.space_info['total']}')
            self.log.info('Successfully retrieved configuration from saber.')

            self.update_ui_with_config()
            self.set_ui_enabled(True)
        except asyncio.TimeoutError:
            box = QMessageBox(
                QMessageBox.Critical, 
                "ERROR: Operation Timed Out", 
                '''Tintallë timed out waiting for a response from your Anima. 
                Please try turning your Anima off and back on, then try again.''',
                QMessageBox.Close,
                parent=self)
            await self.disconnect_saber()
            self.log.error('Connection timed out while reading configuration file from Anima.')
            box.exec()
        except Exception as e:
            error_handler(e)

        if w.autoclose:
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

    async def disconnect_saber(self):
        '''Disconnect saber and perform any necessary cleanup'''
        # Check if config has changed
        button: QMessageBox.StandardButton = None
        if self.current_config != self.saber_config:
            # Prompt user to save or discard changes.
            button = QMessageBox.warning(
                self,
                "Unsaved Changes",
                "You have unsaved configuration changes. Do you want to save changes to the Anima or discard them?",
                buttons = QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel,
                defaultButton = QMessageBox.Cancel
            )
            if button == QMessageBox.Save:
                await self.save_all_changes()

        if button != QMessageBox.Cancel:
            self.log.info("Disconnecting Anima.")
            self.sc = None
            self.display_connection_status(SCStatus.DISCONNECTED)

    async def save_all_changes(self):
        '''Writes any unsaved configuration changes to the attached Anima.'''
        w = Loading_Box(self, "Saving configuration to saber.")
        w.show()

        # Save only what's been changed
        for bank, _ in enumerate(self.current_config["bank"]):
            if self.current_config["bank"][bank] != self.saber_config["bank"][bank]:
                await self.save_color_bank(bank, set_active=False)
        
        if self.current_config["activeBank"] != self.saber_config["activeBank"]:
            await self.set_active_bank(self.current_config["activeBank"])
        
        for effect in self.current_config["sounds"]:
            if effect not in self.saber_config["sounds"] or self.current_config["sounds"][effect] != self.saber_config["sounds"][effect]:
                await self._save_sound_settings(w, {effect: self.current_config["sounds"][effect]}, reload=False)
        
        w.close()

    def reload_config_action_handler(self):
        button = QMessageBox.warning(
            self,
            "Reload Configuration?",
            "WARNING! This will reset any unsaved configuration changes.\n\nDo you want to continue?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No
        )

        if button == QMessageBox.Yes:
            asyncio.ensure_future(self.reload_saber_configuration())

    def reset_saber_to_defaults_action_handler(self):
        button = QMessageBox.warning(
            self,
            "Reset to Defaults?",
            "WARNING! This will erase the saber and reset it to its default configuration. This includes any custom colors and sound fonts.\n\nDo you want to continue?",
            buttons=QMessageBox.Yes | QMessageBox.No,
            defaultButton=QMessageBox.No
        )

        if button == QMessageBox.Yes:
            self.clear_color_ui()
            self.clear_sound_ui()
            asyncio.ensure_future(self._reset_to_defaults())

    async def _reset_to_defaults(self):
        self.log.info('Resetting Anima to default configuration.')
        pd = Progress_Dialog(self, "Resetting Anima", 'Erasing files...', autoclose=False)
        pd.show()

        try:
            # Erase files
            self.log.info("Erasing all files on the Anima.")
            await self.sc.erase_all_files(progress_callback=pd.progressBar.setValue)
            
            # Upload default sound font
            self.log.info("Uploading default sound font.")
            pd.messageLabel.setText("Uploading default sound font...")
            pd.progressBar.setMaximum(0)
            files = glob.glob(os.path.join(resourcedir, 'OpenCore_OEM', '*.RAW'))
            files.sort()
            files = self.move_beep_to_last(files)
            await self._upload_files(files, set_effects=False, reload_config=False, autoclose=True)

            # Send RESET and SAVE commands
            self.log.info('Sending RESET and SAVE commands.')
            pd.messageLabel.setText("Sending RESET and SAVE commands")
            pd.progressBar.setValue(0)
            pd.progressBar.setMaximum(100)
            await self.sc.send_command(b'RESET')
            result = await self.sc.read_line()
            if result != b'OK RESET\n':
                raise InvalidSaberResponseException(f'Command: RESET\nResponse: {result}')
            pd.progressBar.setValue(50)
            await self.sc.send_command(b'SAVE')
            result = await self.sc.read_line()
            if result != b'OK SAVE\n':
                raise InvalidSaberResponseException(f'Command: SAVE\nResponse: {result}')
            pd.progressBar.setValue(100)

            # Reload config
            self.log.info("Reloading configuration from Anima")
            pd.messageLabel.setText("Reloading configuration from Anima")
            pd.progressBar.setMaximum(0)
            await self.reload_saber_configuration(w=pd)

            pd.progressBar.setMaximum(100)
            pd.progressBar.setValue(100)
            pd.report("Reset complete!")

        except Exception as e:
            pd.report("An error has occurred. See the log for details.")
            error_handler(e, parent=self)
        finally:
            pd.finished()

    def anima_terminal_action_handler(self):
        terminal_window = AnimaTerminalWindow(self.sc, parent=self)
        terminal_window.setModal(True)
        terminal_window.exec()
        asyncio.ensure_future(self.reload_saber_configuration())

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
    
    def save_log_to_file_action_handler(self):
        default = os.path.join(
            os.path.expanduser('~'),
            f'tintalle-{datetime.now().strftime('%m-%d-%Y-%H%M%S')}.log'
        )
        filename = QFileDialog.getSaveFileName(
            self, 
            'Save Log As...',
            default,
            'Log Files (*.log)')[0]
        self.log.debug(f'Saving log output to file {filename}')
        
        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(self.logTextBox.toPlainText())
            except Exception as e:
                error_handler(e)
        try:
            with open(filename, 'w') as file:
                file.write(self.logTextBox.toPlainText())
        except Exception as e:
            error_handler(e)
    
    def export_anima_config_ini_action_handler(self):
        default = os.path.join(
            os.path.expanduser('~'),
            'config.ini'
        )
        filename = QFileDialog.getSaveFileName(
            self, 
            'Save config.ini As...',
            default)[0]
        self.log.debug(f'Saving config.ini to file {filename}')

        if filename:
            try:
                with open(filename, 'w') as file:
                    file.write(json.dumps(self.saber_config, indent=2))
            except Exception as e:
                error_handler(e)
    
    # Decided not to use this feature. Keeping the code here in case I change my mind later.
    # def export_current_config_action_handler(self):
    #     default = os.path.join(
    #         os.path.expanduser('~'),
    #         'config.ini'
    #     )
    #     filename = QFileDialog.getSaveFileName(
    #         self, 
    #         'Save config.ini As...',
    #         default)[0]
    #     self.log.debug(f'Saving config.ini to file {filename}')

    #     if filename:
    #         try:
    #             with open(filename, 'w') as file:
    #                 file.write(json.dumps(self.current_config, indent=2))
    #         except Exception as e:
    #             error_handler(e)

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
            asyncio.ensure_future(self._erase_all())

    async def _erase_all(self, reload_config: bool = True):
        self.log.info("Erasing all files on connected saber.")
        
        pd = Progress_Dialog(parent=self, title="Erasing Saber", message="Erasing all sound files on saber.", autoclose=not reload_config)
        pd.show()

        #worker = Worker(self.sc.erase_all_files)
        try:
            await self.sc.erase_all_files(progress_callback=pd.progressBar.setValue)
            pd.report("All sound files on saber have been erased.\nPlease re-load your sound files.")
            self.log.info("All sound files on saber have been erased. Please re-load your sound files.")
            if reload_config:
                await self.reload_saber_configuration()
        except Exception as e:
            pd.report("An error has occurred. See the log for details.")
            error_handler(e, parent=self)
        finally:
            pd.finished()

    @staticmethod
    def move_beep_to_last(files: list[str]) -> list[str]:
        '''If the list of files contains 'BEEP.RAW', move it to last. Otherwise return the list unchanged.'''
        log = logging.getLogger()
        beep_files = [file for file in files if "BEEP.RAW" in file]
        # if a BEEP.RAW is specified, move it to the end of the list.
        # NXTs seem to do better if BEEP.RAW is the last file uploaded
        if beep_files:
            for file in beep_files:
                log.debug(f'Moving BEEP file {file} to end of upload list.')
                files.remove(file)
                files.append(file)
        return files

    def upload_button_handler(self):
        # Get a list of files to upload. Can be one file or multiple files
        files = QFileDialog.getOpenFileNames(self, filter="RAW Sound File (*.RAW)")[0]
        if(files):
            files.sort()
            if self.anima_is_NXT():
                # move any BEEP.RAW files to last
                files = self.move_beep_to_last(files)
                if not files[-1].endswith('BEEP.RAW'): # if a BEEP.RAW is not included in the list to upload
                    if 'BEEP.RAW' not in self.files_dict.keys(): # and there's not already a BEEP.RAW on the saber
                        self.log.info('NXT saber detected and no BEEP.RAW provided. Adding default BEEP.RAW.')
                        files.append(os.path.join(resourcedir, 'OpenCore_OEM', 'BEEP.RAW'))
            self.log.debug(f'List of files to upload: {files}')

            asyncio.ensure_future(self._upload_files(files))

    async def _upload_files(self, files: list[str], set_effects: bool = True, reload_config: bool = True, autoclose: bool = False):
        fupd = File_Upload_Progress_Dialog(self, multifile=True if len(files) > 1 else False, autoclose=autoclose)
        fupd.set_num_files(len(files))
        fupd.show()

        for file in files:
            # Prepare info display
            self.log.info(f'Uploading file: {os.path.basename(file)}')
            self.log.debug(f'File path: {file}')
            fupd.fileNameLabel.setText(f"File: {os.path.basename(file)}")
            fupd.fileProgressBar.setValue(0)
            fupd.set_file_size(os.path.getsize(file))
            
            # Upload file
            try:
                await self.sc.write_files_to_saber([file], progress_callback=fupd.fileProgressBar.setValue, add_beep=False)
            except Exception as e:
                error_handler(e, info="We recommend erasing all files on the Anima before uploading again.", parent=self)
                fupd.halt = True
            
            # Update display with file completed
            fupd.file_completed()
            # TODO: Show 5 second waiting message.

            # Check to see if user has clicked 'Cancel'
            if fupd.halt:
                break

        fupd.upload_complete()
        try:
            if set_effects:
                await self.auto_assign_effects(reload_config=False)
            if reload_config:
                await self.reload_saber_configuration()
        except Exception as e:
            error_handler(e, parent=self)

    def clear_sound_ui(self):
        for box in self.effects_buttonGroup.buttons():
            box.blockSignals(True)
            box.setChecked(False)
            box.blockSignals(False)
        self.files_treeWidget.clear()
        self.freespace_label.setText('Free Space: ----')
        self.usedspace_label.setText('Used Space: ----')
        self.totalspace_label.setText('Total Space: ----')

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
        # TODO: add a box with a progress bar showing which effect is being saved
        w.show()

        asyncio.ensure_future(self._save_sound_settings(w, self.current_config['sounds']))

    async def _save_sound_settings(self, w: QDialog, sounds: dict, reload: bool = True):
        for effect, files in sounds.items():
            if effect == 'soundengine': continue
            self.log.info(f'Setting sounds for effect: {effect}')
            await self.sc.set_sounds_for_effect(effect, files)
            await asyncio.sleep(1)
        if reload:
            asyncio.ensure_future(self.reload_saber_configuration(w))

    async def auto_assign_effects(self, reload_config:bool = True):
        '''Automatically assign sound files to effects for the files currently on the saber.'''
        w = Loading_Box(self, "Automatically setting sound effects\nbased on the default naming scheme.")
        # TODO: add a box with a progress bar showing which effect is being saved
        w.show()

        self.log.info('Automatically assigning sound files to effects based on the default naming scheme.')
        await self.sc.auto_assign_sound_effects()
        await asyncio.sleep(2)
        w.close()

        if reload_config:
            await self.reload_saber_configuration()
    
    def auto_assign_effects_button_handler(self):
        asyncio.ensure_future(self.auto_assign_effects())

    # ------------------------- #
    # Firmware handling methods #
    # ------------------------- #

    def anima_is_NXT(self):
        if self.saber_info and self.saber_info['version'][:4] == 'NXT_':
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
        widgets = [self.r_spinbox, self.g_spinbox, self.b_spinbox, self.w_spinbox, self.r_slider, self.g_slider, self.b_slider, self.w_slider]
        for widget in widgets:
            widget.blockSignals(True)
            widget.setValue(0)
            widget.blockSignals(False)

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
    
    async def preview_color_on_saber(self, color: dict):
        '''Send the specified color to the saber for preview.'''
        self.log.debug(f'Previewing color: {color}')
        await self.sc.preview_color(*color.values())

    def preview_button_handler(self):
        self.log.info('Previewing color on saber.')
        asyncio.ensure_future(self.preview_color_on_saber(self.get_current_color()))

    def update_current_config_from_gui(self):
        '''Updates the stored configuration when the GUI elements are changed.'''
        self.current_config['activeBank'] = self.color_bank_select_box.currentIndex()
        color = self.get_current_color()
        self.current_config['bank'][self.color_bank_select_box.currentIndex()][self.get_selected_effect()] = color

    def color_save_button_handler(self):
        '''Write the values of the currently displayed bank to the saber.'''
        w = Loading_Box(self, "Saving configuration to saber.")
        w.show()

        asyncio.ensure_future(self._save_current_color(w))

    async def _save_current_color(self, w: QDialog):
        await self.save_color_bank(self.color_bank_select_box.currentIndex(), set_active=True)
        asyncio.ensure_future(self.reload_saber_configuration(w))

    def save_all_colors_button_handler(self):
        '''Write the values of all banks to the saber.'''
        w = Loading_Box(self, "Saving configuration to saber.")
        w.show()

        asyncio.ensure_future(self._save_all_colors(w))

    async def _save_all_colors(self, w: QDialog, reload: bool = True):
        # TODO: implement progress bar that fills up as each is saved
        self.log.debug('Saving all color banks to saber.')
        count = self.color_bank_select_box.count()
        for i in range(count):
            await self.save_color_bank(i, set_active=False)
            await asyncio.sleep(1)

        if reload:
            asyncio.ensure_future(self.reload_saber_configuration(w))

    async def save_color_bank(self, bank: int, set_active=True):
        self.log.info(f'Saving color bank #{bank+1} to saber.')
        m_color = self.current_config['bank'][bank]['color']
        cl_color = self.current_config['bank'][bank]['clash']
        s_color = self.current_config['bank'][bank]['swing']
        self.log.debug(f'Main color: {m_color}\nClash color: {cl_color}\nSwing color: {s_color}')

        await self._set_colors(bank, m_color, cl_color, s_color, set_active)

    async def set_active_bank(self, bank: int):
        '''Sets the provided bank number as the active bank on the Anima.'''
        self.log.info(f"Setting active color bank to #{bank + 1}")
        await self.sc.set_active_bank(bank)

    async def _set_colors(self, bank: int, m_color: dict, cl_color: dict, s_color:dict, set_active=True):
        try:
            await self.sc.set_color(bank, "color", m_color['red'], m_color['green'], m_color['blue'], m_color['white'])
            await self.sc.set_color(bank, "clash", cl_color['red'], cl_color['green'], cl_color['blue'], cl_color['white'])
            await self.sc.set_color(bank, "swing", s_color['red'], s_color['green'], s_color['blue'], s_color['white'])
            if set_active: await self.set_active_bank(bank)
        except Exception as e:
            error_handler(e)
    
    def save_colors_action_handler(self):
        default = os.path.join(
            os.path.expanduser('~'),
            'saber_colors.txt'
        )
        filename = QFileDialog.getSaveFileName(
            self, 
            'Save Colors As...',
            default)[0]
        self.log.debug(f'Saving colors to file {filename}')

        if filename:
            color_dict = {}
            color_dict['activeBank'] = self.current_config['activeBank']
            color_dict['bank'] = self.current_config['bank']
            
            try:
                with open(filename, 'w') as file:
                    file.write(json.dumps(color_dict, indent=2))
                self.log.info(f'Saved colors to file: {filename}')
            except Exception as e:
                error_handler(e)
    
    def load_colors_action_handler(self):
        filename = QFileDialog.getOpenFileName(
            self,
            'Load Colors From...',
            os.path.expanduser('~')
        )[0]

        if filename:
            try:
                with open(filename) as file:
                    color_dict = json.loads(file.read())
                    self.current_config['activeBank'] = color_dict['activeBank']
                    self.current_config['bank'] = color_dict['bank']
                    self.update_ui_with_config()
            except (json.JSONDecodeError, KeyError):
                error_handler(f'File "{filename}" does not appear to be a valid color file.')

# set icon for Windows - from https://www.pythonguis.com/tutorials/packaging-pyqt5-pyside2-applications-windows-pyinstaller/#building-a-windows-installer-with-installforge
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'com.sublunarysphere.tintalle.' + script_version
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if platform.system == "Windows":
        icon = ':/img/tintalle.ico'
    else:
        icon = ':/img/tintalle.png'
    app.setWindowIcon(QIcon(':/img/tintalle.png'))
    mainwindow = Main_Window()

    QtAsyncio.run(handle_sigint=True)
