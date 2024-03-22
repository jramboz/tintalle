import os
from PySide6.QtCore import QProcess
import requests
from typing import Optional, Tuple
import logging
import wget
import shutil
from threadrunner import *
from dialogs import *
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox

# TODO: read this from a config file, and allow the user to set it in options somewhere.
EVO_FIRMWARE_RELEASE_URL = 'https://api.github.com/repos/LamaDiLuce/polaris-opencore/releases/latest'

def check_latest_fw_release(parent: QWidget = None) -> Tuple[str, str]:
    '''Checks for the latest Polaris OpenCore firmware release.
    Returns a tuple with the version number and download url as strings.'''
    try:
        response = requests.get(EVO_FIRMWARE_RELEASE_URL)
        if response.status_code == 200:
            data = response.json()
            return (data['tag_name'], data['assets'][0]['browser_download_url'])
        else:
            error_handler('An error occurred while checking for the latest firmware.', 'Try manually downloading the latest release from: ' + EVO_FIRMWARE_RELEASE_URL, parent)
            return None
    except:
        error_handler('Unable to retrieve latest version.', 'Check your internet connection and try again.', parent)
        return None

class Download_Controller():
    '''Holds GUI state and handles updating progress dialog.'''

    def __init__(self, url: str = None, parent: QWidget = None, outdir: str = None, autoclose: bool = True):
        self.url = url
        self.parent = parent
        self.outdir = outdir
        self.filename: str = None

        # set up progress dialog
        self.pd = Progress_Dialog(parent=self.parent, title='Downloading File', message='Download Progress:', autoclose=autoclose)

    def download(self) -> str:
        try:
            # run in a thread and pass back status from wget
            worker = Worker(wget.download, self.url, out=self.outdir, bar=self._gui_progress_handler, noprogress=True)
            worker.signals.finished.connect(lambda: self.pd.finished())
            worker.signals.result.connect(lambda r: setattr(self, 'filename', r))
            worker.signals.error.connect(error_handler)
            self.pd.show()
            worker.run()
            while not self.filename:
                pass
            return self.filename

        except Exception as e:
            error_handler(f'An error has occurred: {e}', self.parent)
            return None

    def _gui_progress_handler(self, current, total, width=80):
        # wget.download() has its own callback handler. Let's just work with it instead of trying to pass our own callback.
        '''Output wget progress info to Progress_Dialog'''
        self.pd.progressBar.setMaximum(total)
        self.pd.progressBar.setValue(current)

class Firmware_Update_Controller():
    '''Performs GUI updating for firmware upload'''

    def __init__(self, fw_file: str, parent: QWidget = None) -> None:
        self.fw_file = fw_file
        self.display = External_Process_Dialog(parent)
    
    def message(self, s):
        self.display.text.appendPlainText(s)
    
    def upload_firmware(self):
        if shutil.which('tycmd'):
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.readyReadStandardError.connect(self.handle_stderr)
            self.p.finished.connect(lambda: self.display.finished())
            self.display.show()
            self.p.start('tycmd', ['upload', self.fw_file])
        else:
            error_handler('TYCMD not found', 'Please install TYCMD.', self.display)
    
    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

def download_fw(parent: QWidget = None, outdir: str = None, autoclose: bool = True, url: str = None) -> str:
    '''Download the OpenCore firmware and save to current directory. 
    If url is specified, use that. Otherwise, check for the latest version and download.
    (This is to avoid having to ping GitHub twice in a row for the same url if possible.)'''
    try:
        if not url:
            url = check_latest_fw_release()[1]
        if url: # checking again to make sure one was retrieved
            dc = Download_Controller(url, parent, outdir, autoclose)
            return dc.download()

    except Exception as e:
        error_handler(e, parent)
        return None

def prompt_for_location_and_download_fw(parent: QWidget = None, autoclose: bool = False, url: str = None) -> str:
    '''Prompt user to select a download location, then download latest firmware to that directory.
    If url is specified, use that. Otherwise, check for the latest version and download.
    (This is to avoid having to ping GitHub twice in a row for the same url if possible.)'''
    if not url:
        url = check_latest_fw_release()[1]
    if url:
        filedir = QFileDialog.getExistingDirectory(parent, 'Choose Download Location', options=QFileDialog.ShowDirsOnly)
        if filedir:
            filename = download_fw(parent=parent, outdir=filedir, autoclose=autoclose, url=url)
            return os.path.join(filedir, filename)

def upload_firmware(fw_file: str, parent: QWidget = None):
    '''Upload firmware to saber using external tycmd command. fw_file is a string with the filename.'''
    try:
        fuc = Firmware_Update_Controller(fw_file, parent)
        fuc.upload_firmware()
    except Exception as e:
        error_handler(e, parent)


class TesterWindow(QMainWindow):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        button = QPushButton('Click me')
        button.clicked.connect(self._test)
        self.setCentralWidget(button)

    def _test(self):
        r = prompt_for_location_and_download_fw(self, autoclose=True)
        upload_firmware(r, self)
        

if __name__ == "__main__":
    app = QApplication()
    window = TesterWindow()
    window.show()
    app.exec()
