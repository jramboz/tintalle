# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

from qtexteditlogger import QTextEditLogger

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 595)
        self.action_Refresh_Ports = QAction(MainWindow)
        self.action_Refresh_Ports.setObjectName(u"action_Refresh_Ports")
        self.action_Refresh_Ports.setShortcutVisibleInContextMenu(True)
        self.action_Show_Hide_Log = QAction(MainWindow)
        self.action_Show_Hide_Log.setObjectName(u"action_Show_Hide_Log")
        self.action_Show_Hide_Log.setCheckable(False)
        self.action_Debug_Mode = QAction(MainWindow)
        self.action_Debug_Mode.setObjectName(u"action_Debug_Mode")
        self.action_Debug_Mode.setCheckable(True)
        self.action_Reload_Config = QAction(MainWindow)
        self.action_Reload_Config.setObjectName(u"action_Reload_Config")
        self.action_Reload_Config.setEnabled(False)
        self.action_Reload_Config.setShortcutVisibleInContextMenu(True)
        self.action_Check_for_Latest_Firwmare = QAction(MainWindow)
        self.action_Check_for_Latest_Firwmare.setObjectName(u"action_Check_for_Latest_Firwmare")
        self.action_Install_Firmware_from_File = QAction(MainWindow)
        self.action_Install_Firmware_from_File.setObjectName(u"action_Install_Firmware_from_File")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.connection_groupBox = QGroupBox(self.centralwidget)
        self.connection_groupBox.setObjectName(u"connection_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connection_groupBox.sizePolicy().hasHeightForWidth())
        self.connection_groupBox.setSizePolicy(sizePolicy)
        self.connection_groupBox.setMinimumSize(QSize(295, 0))
        self.connection_groupBox.setFlat(True)
        self.horizontalLayout = QHBoxLayout(self.connection_groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.connection_groupBox)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.saber_select_box = QComboBox(self.connection_groupBox)
        self.saber_select_box.setObjectName(u"saber_select_box")

        self.horizontalLayout.addWidget(self.saber_select_box)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.connection_groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.status_label = QLabel(self.connection_groupBox)
        self.status_label.setObjectName(u"status_label")

        self.horizontalLayout.addWidget(self.status_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.connect_button = QPushButton(self.connection_groupBox)
        self.connect_button.setObjectName(u"connect_button")

        self.horizontalLayout.addWidget(self.connect_button)


        self.verticalLayout_2.addWidget(self.connection_groupBox)

        self.content_tabWidget = QTabWidget(self.centralwidget)
        self.content_tabWidget.setObjectName(u"content_tabWidget")
        self.content_tabWidget.setEnabled(False)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.erase_button = QPushButton(self.tab)
        self.erase_button.setObjectName(u"erase_button")
        self.erase_button.setGeometry(QRect(10, 10, 100, 32))
        self.upload_button = QPushButton(self.tab)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setGeometry(QRect(10, 40, 100, 32))
        self.content_tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.content_tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_2.addWidget(self.content_tabWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.logTextBox = QTextEditLogger(self.centralwidget)
        self.logTextBox.setObjectName(u"logTextBox")
        self.logTextBox.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.logTextBox.sizePolicy().hasHeightForWidth())
        self.logTextBox.setSizePolicy(sizePolicy1)
        self.logTextBox.setMaximumSize(QSize(500, 16777215))
        self.logTextBox.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.logTextBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 24))
        self.menuConnection = QMenu(self.menubar)
        self.menuConnection.setObjectName(u"menuConnection")
        self.menuTroubleshooting = QMenu(self.menubar)
        self.menuTroubleshooting.setObjectName(u"menuTroubleshooting")
        self.menuFirmware = QMenu(self.menubar)
        self.menuFirmware.setObjectName(u"menuFirmware")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuFirmware.menuAction())
        self.menubar.addAction(self.menuTroubleshooting.menuAction())
        self.menuConnection.addAction(self.action_Refresh_Ports)
        self.menuConnection.addAction(self.action_Reload_Config)
        self.menuTroubleshooting.addAction(self.action_Show_Hide_Log)
        self.menuTroubleshooting.addAction(self.action_Debug_Mode)
        self.menuFirmware.addAction(self.action_Check_for_Latest_Firwmare)
        self.menuFirmware.addAction(self.action_Install_Firmware_from_File)

        self.retranslateUi(MainWindow)

        self.content_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tintalle", None))
        self.action_Refresh_Ports.setText(QCoreApplication.translate("MainWindow", u"&Refresh Ports", None))
#if QT_CONFIG(shortcut)
        self.action_Refresh_Ports.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.action_Show_Hide_Log.setText(QCoreApplication.translate("MainWindow", u"Show/Hide &Log", None))
#if QT_CONFIG(shortcut)
        self.action_Show_Hide_Log.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+L", None))
#endif // QT_CONFIG(shortcut)
        self.action_Debug_Mode.setText(QCoreApplication.translate("MainWindow", u"&Debug Mode", None))
#if QT_CONFIG(shortcut)
        self.action_Debug_Mode.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+D", None))
#endif // QT_CONFIG(shortcut)
        self.action_Reload_Config.setText(QCoreApplication.translate("MainWindow", u"Reload &Config", None))
        self.action_Check_for_Latest_Firwmare.setText(QCoreApplication.translate("MainWindow", u"&Check for Latest Firwmare", None))
        self.action_Install_Firmware_from_File.setText(QCoreApplication.translate("MainWindow", u"&Install Firmware from File...", None))
        self.connection_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Status:", None))
        self.status_label.setText(QCoreApplication.translate("MainWindow", u"Searching...", None))
        self.connect_button.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.erase_button.setText(QCoreApplication.translate("MainWindow", u"Erase Sounds", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Tab 1", None))
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.logTextBox.setPlaceholderText("")
        self.menuConnection.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.menuTroubleshooting.setTitle(QCoreApplication.translate("MainWindow", u"Troubleshooting", None))
        self.menuFirmware.setTitle(QCoreApplication.translate("MainWindow", u"Firmware", None))
    # retranslateUi

