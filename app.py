from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QProgressBar, QFileDialog
import PySide6.QtCore as QtCore
from ui_mainwindow import Ui_MainWindow
from py2saber import Saber_Controller, NoAnimaSaberException
from threadrunner import *
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

class Progress_Dialog(QDialog):
    '''Simple dialog to display progress of a task and activate a close button when complete.'''

    def __init__(self, parent=None, title: str = "Progress", message: str = "Task Progress:" ):
        super().__init__(parent)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Close)
        self.buttonBox.button(QDialogButtonBox.Close).setEnabled(False)
        self.buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.close)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.reportLabel = QLabel()
        self.progressBar = QProgressBar()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(message))
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.reportLabel)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.show()
    
    def report(self, msg: str):
        '''Display a message below the progress bar.'''
        self.reportLabel.setText(msg)

    def finished(self):
        '''Call this when action is finished and dialog can be closed.'''
        self.buttonBox.button(QDialogButtonBox.Close).setEnabled(True)

class File_Upload_Progress_Dialog(QDialog):
    halt = False # set to True to cancel after the curent file is finished uploading

    def __init__(self, parent = None, multifile=False):
        super().__init__(parent)
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Cancel)
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel_button_handler)
        self.setWindowTitle("Uploading Files")
        self.setModal(True)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint )

        self.layout = QVBoxLayout()
        
        self.fileNameLabel = QLabel("File: ")
        self.layout.addWidget(self.fileNameLabel)
        
        self.fileProgressBar = QProgressBar()
        self.fileProgressBar.setTextVisible(True)
        self.fileProgressBar.setFormat('Uploaded %v / %m bytes')
        self.layout.addWidget(self.fileProgressBar)
        
        self.totalProgressBar = QProgressBar()
        if multifile:
            self.totalProgressBar.setTextVisible(True)
            self.totalProgressBar.setValue(0)
            self.layout.addWidget(self.totalProgressBar)
        
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.show()
    
    def set_num_files(self, num_files: int):
        '''Set the number of fiiles to be uploaded in this batch.'''
        self.totalProgressBar.setMaximum(num_files)
        self.totalProgressBar.setFormat("Completed %v of %m files")
    
    def file_completed(self):
        '''Update file completed count in progress bar'''
        self.totalProgressBar.setValue(self.totalProgressBar.value() + 1)

    def set_file_size(self, size: int):
        '''Set the size of the current file being uploaded, in bytes'''
        self.fileProgressBar.setMaximum(size)
    
    def set_bytes_uploaded(self, b: int):
        '''Set the number of bytes uploaded for the current file'''
        self.fileProgressBar.setValue(b)
    
    def cancel_button_handler(self):
        self.halt = True
        self.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(False)
        logging.getLogger().info('Canceling file upload.')
    
    def upload_complete(self):
        '''Call this when all file uploads are completed and the window can be closed.'''
        self.buttonBox.button(QDialogButtonBox.Cancel).setEnabled(True)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText('Close')
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.disconnect()
        self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.close)
        self.fileNameLabel.setText('Upload complete!')
        logging.getLogger().info('Upload complete!')

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
    config_ini: dict = None
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
        self.erase_button.clicked.connect(self.erase_button_handler)
        self.upload_button.clicked.connect(self.upload_button_handler)
        self.show()

        # Search for connected sabers
        self.display_connection_status(SCStatus.SEARCHING)
        self.update_ports()

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

        self.config_ini = eval(self.sc.read_config_ini())
        self.log.debug(f'Retrieved config.ini:\n{self.config_ini}')
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
            
            # Create and run the upload controller
            self.uc = Upload_Controller(files, display, self.sc)
            self.uc.run()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainwindow = Main_Window()

    app.exec()
