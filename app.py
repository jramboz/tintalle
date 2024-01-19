from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QProgressBar, QFileDialog, QPushButton
import PySide6.QtCore as QtCore
from ui_mainwindow import Ui_MainWindow
from py2saber import Saber_Controller, NoAnimaSaberException
from threadrunner import *
from dialogs import *
import version_compare as vc
import firmware
from enum import Enum, auto
import logging
import sys
import os

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
        else:
            self._upload_next_file()
        

class Main_Window(QMainWindow, Ui_MainWindow):
    sc: Saber_Controller = None
    saber_config: dict = None
    files_dict: dict = None
    saber_info: dict = None
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
        self.action_Reload_Config.triggered.connect(self.reload_saber_configuration)
        self.action_Check_for_Latest_Firwmare.triggered.connect(self.fw_check_handler)
        self.action_Install_Firmware_from_File.triggered.connect(self.install_firmware_from_file_handler)
        self.erase_button.clicked.connect(self.erase_button_handler)
        self.upload_button.clicked.connect(self.upload_button_handler)
        self.show()

        # Search for connected sabers
        self.display_connection_status(SCStatus.SEARCHING)
        self.update_ports()

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
           self.content_tabWidget.setEnabled(False)
           self.action_Reload_Config.setEnabled(False)
           self.saber_select_box.setEnabled(True)
           
    def error_handler(self, e):
        '''Generic error handler.'''
        self.log.error('An error has occurred.')
        self.log.error(e)

    def connect_button_handler(self):
        if self.sc: # if connected, disconnect
            self.disconnect_saber()
        else: # try to connect
            try:
                self.connect_saber()
            except NoAnimaSaberException:
                self.error_handler(NoAnimaSaberException)
                self.display_connection_status(SCStatus.DISCONNECTED)
    
    def connect_saber(self):
        '''Connect to a saber and perform initialization actions. Can also be used to refresh saber configuration.'''
        self.display_connection_status(SCStatus.CONNECTING)
        if not self.sc:
            port = self.saber_select_box.currentText()
            self.sc = Saber_Controller(port, gui=True)
        self.reload_saber_configuration()
        self.display_connection_status(SCStatus.CONNECTED)
        self.log.info(f'Connected to saber.\nSerial Number: {self.saber_info["serial"]}\nFirmware version: {self.saber_info["version"]}')

    def reload_saber_configuration(self):
        '''Reload the files list and configuration files from the saber.'''
        # display a "loading" dialog. Probably this will happen fast enough that most people won't even see it.
        w = QDialog(parent=self)
        w.setModal(True)
        w.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint)
        w.layout = QVBoxLayout()
        w.layout.addWidget(QLabel("Reading configuration from saber."))
        bar = QProgressBar()
        bar.setMaximum(0)
        w.layout.addWidget(bar)
        w.setLayout(w.layout)
        w.show()

        self.saber_config = eval(self.sc.read_config_ini())
        self.log.debug(f'Retrieved config.ini:\n{self.saber_config}')
        self.files_dict = self.sc.list_files_on_saber()
        self.log.debug(f'Retrieved files from saber:\n{self.files_dict}')
        self.saber_info = self.sc.get_saber_info()
        self.log.debug(f'Retrieved saber info: {self.saber_info}')
        self.log.info('Successfully retrieved configuration from saber.')

        w.close()

    def disconnect_saber(self):
        '''Disconnect saber and perform any necessary cleanup'''
        self.sc = None
        self.display_connection_status(SCStatus.DISCONNECTED)

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

            def e(error: tuple):
                '''What to do with an error.'''
                pd.report("An error has occurred. See the log for details.")
                self.error_handler(e)

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
            self.uc.run()

    # ------------------------- #
    # Firmware handling methods #
    # ------------------------- #

    def fw_check_handler(self):
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
        fw_file = QFileDialog.getOpenFileName(self, caption='Open Firmware File', filter='OpenCore Firwmare File (*.hex)')[0]
        if fw_file:
            try:
                firmware.upload_firmware(fw_file, self)
            except Exception as e:
                error_handler(e, parent=self)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainwindow = Main_Window()

    app.exec()
