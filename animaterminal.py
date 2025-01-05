import asyncio
import logging
import sys

from PySide6 import QtAsyncio
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QApplication, QDialog, QWidget

from py2saber import Saber_Controller
from ui_animaterminal import Ui_AnimaTerminalWindow


class AnimaTerminalWindow(Ui_AnimaTerminalWindow, QDialog):
    def __init__(self, sc: Saber_Controller, parent: QWidget = None):
        super().__init__(parent)
        self.setupUi(self)
        self.sendButton.clicked.connect(
            lambda: asyncio.ensure_future(self.send_action())
        )
        self.sc = sc
        self.default_format = self.terminalDisplay.currentCharFormat()
        self.reader_task = asyncio.create_task(self.reader())

    def closeEvent(self, event):
        self.reader_task.cancel()
        event.accept()

    async def reader(self):
        while True:
            r = await self.sc._ser.read_async()
            if r:
                await self._append_text(r.decode())

    async def _append_text(self, text: str):
        cursor = self.terminalDisplay.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.setCharFormat(self.default_format)
        cursor.insertText(text)
        self.terminalDisplay.ensureCursorVisible()

    async def send_action(self):
        cmd = self.commandTextBox.text()
        await self.sc.send_command(cmd.encode("utf-8"))
        self.terminalDisplay.appendHtml(
            f'<p style="color:yellow;">&gt; {cmd}<br /></p>'
        )
        self.commandTextBox.clear()


async def main():
    log = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    log.addHandler(handler)
    sc = await Saber_Controller.create()
    sc.log.addHandler(handler)
    mainwindow = AnimaTerminalWindow(sc)
    mainwindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QtAsyncio.run(main(), handle_sigint=True)
