# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'animaterminal.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLineEdit,
    QPlainTextEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_AnimaTerminalWindow(object):
    def setupUi(self, AnimaTerminalWindow):
        if not AnimaTerminalWindow.objectName():
            AnimaTerminalWindow.setObjectName(u"AnimaTerminalWindow")
        AnimaTerminalWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        AnimaTerminalWindow.resize(640, 480)
        AnimaTerminalWindow.setSizeGripEnabled(False)
        self.verticalLayout = QVBoxLayout(AnimaTerminalWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.terminalDisplay = QPlainTextEdit(AnimaTerminalWindow)
        self.terminalDisplay.setObjectName(u"terminalDisplay")
        self.terminalDisplay.setStyleSheet(u"background: black;\n"
"color: white;")

        self.verticalLayout.addWidget(self.terminalDisplay)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.commandTextBox = QLineEdit(AnimaTerminalWindow)
        self.commandTextBox.setObjectName(u"commandTextBox")
        self.commandTextBox.setClearButtonEnabled(True)

        self.horizontalLayout.addWidget(self.commandTextBox)

        self.sendButton = QPushButton(AnimaTerminalWindow)
        self.sendButton.setObjectName(u"sendButton")

        self.horizontalLayout.addWidget(self.sendButton)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AnimaTerminalWindow)

        QMetaObject.connectSlotsByName(AnimaTerminalWindow)
    # setupUi

    def retranslateUi(self, AnimaTerminalWindow):
        AnimaTerminalWindow.setWindowTitle(QCoreApplication.translate("AnimaTerminalWindow", u"Anima Terminal", None))
        self.sendButton.setText(QCoreApplication.translate("AnimaTerminalWindow", u"Send", None))
    # retranslateUi

