from PySide6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QProgressBar
import PySide6.QtCore as QtCore
import logging

class Progress_Dialog(QDialog):
    '''Simple dialog to display progress of a task and activate a close button when complete.'''

    def __init__(self, parent=None, title: str = "Progress", message: str = "Task Progress:", autoclose: bool = False ):
        super().__init__(parent)
        self.autoclose = autoclose
        if not autoclose:
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
        if not autoclose:
            self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.show()
    
    def report(self, msg: str):
        '''Display a message below the progress bar.'''
        self.reportLabel.setText(msg)

    def finished(self):
        '''Call this when action is finished and dialog can be closed.'''
        if self.autoclose:
            self.close()
        else:
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