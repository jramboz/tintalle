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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from qtexteditlogger import QTextEditLogger

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(859, 616)
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
        self.color_tab = QWidget()
        self.color_tab.setObjectName(u"color_tab")
        self.gridLayout_3 = QGridLayout(self.color_tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.color_groupbox = QGroupBox(self.color_tab)
        self.color_groupbox.setObjectName(u"color_groupbox")
        self.gridLayout = QGridLayout(self.color_groupbox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.g_slider = QSlider(self.color_groupbox)
        self.g_slider.setObjectName(u"g_slider")
        self.g_slider.setMaximum(255)
        self.g_slider.setOrientation(Qt.Horizontal)
        self.g_slider.setTickPosition(QSlider.TicksAbove)
        self.g_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.g_slider, 1, 2, 1, 1)

        self.label_6 = QLabel(self.color_groupbox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.w_spinbox = QSpinBox(self.color_groupbox)
        self.w_spinbox.setObjectName(u"w_spinbox")
        self.w_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.w_spinbox, 3, 1, 1, 1)

        self.b_slider = QSlider(self.color_groupbox)
        self.b_slider.setObjectName(u"b_slider")
        self.b_slider.setMaximum(255)
        self.b_slider.setOrientation(Qt.Horizontal)
        self.b_slider.setTickPosition(QSlider.TicksAbove)
        self.b_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.b_slider, 2, 2, 1, 1)

        self.label_5 = QLabel(self.color_groupbox)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)

        self.label_4 = QLabel(self.color_groupbox)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)

        self.w_slider = QSlider(self.color_groupbox)
        self.w_slider.setObjectName(u"w_slider")
        self.w_slider.setMaximum(255)
        self.w_slider.setOrientation(Qt.Horizontal)
        self.w_slider.setTickPosition(QSlider.TicksAbove)
        self.w_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.w_slider, 3, 2, 1, 1)

        self.g_spinbox = QSpinBox(self.color_groupbox)
        self.g_spinbox.setObjectName(u"g_spinbox")
        self.g_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.g_spinbox, 1, 1, 1, 1)

        self.r_slider = QSlider(self.color_groupbox)
        self.r_slider.setObjectName(u"r_slider")
        self.r_slider.setMaximum(255)
        self.r_slider.setOrientation(Qt.Horizontal)
        self.r_slider.setTickPosition(QSlider.TicksAbove)
        self.r_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.r_slider, 0, 2, 1, 1)

        self.r_spinbox = QSpinBox(self.color_groupbox)
        self.r_spinbox.setObjectName(u"r_spinbox")
        self.r_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.r_spinbox, 0, 1, 1, 1)

        self.b_spinbox = QSpinBox(self.color_groupbox)
        self.b_spinbox.setObjectName(u"b_spinbox")
        self.b_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.b_spinbox, 2, 1, 1, 1)

        self.label_3 = QLabel(self.color_groupbox)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(2, 1)

        self.gridLayout_3.addWidget(self.color_groupbox, 0, 0, 1, 1)

        self.controls_groupbox = QGroupBox(self.color_tab)
        self.controls_groupbox.setObjectName(u"controls_groupbox")
        self.verticalLayout = QVBoxLayout(self.controls_groupbox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.color_bank_select_box = QComboBox(self.controls_groupbox)
        self.color_bank_select_box.setObjectName(u"color_bank_select_box")

        self.verticalLayout.addWidget(self.color_bank_select_box)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.reset_changes_button = QPushButton(self.controls_groupbox)
        self.reset_changes_button.setObjectName(u"reset_changes_button")

        self.verticalLayout.addWidget(self.reset_changes_button)

        self.color_save_button = QPushButton(self.controls_groupbox)
        self.color_save_button.setObjectName(u"color_save_button")

        self.verticalLayout.addWidget(self.color_save_button)

        self.preview_button = QPushButton(self.controls_groupbox)
        self.preview_button.setObjectName(u"preview_button")

        self.verticalLayout.addWidget(self.preview_button)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.gridLayout_3.addWidget(self.controls_groupbox, 0, 1, 1, 1)

        self.effect_groupbox = QGroupBox(self.color_tab)
        self.effect_groupbox.setObjectName(u"effect_groupbox")
        self.gridLayout_2 = QGridLayout(self.effect_groupbox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.main_radioButton = QRadioButton(self.effect_groupbox)
        self.main_radioButton.setObjectName(u"main_radioButton")
        self.main_radioButton.setChecked(True)

        self.gridLayout_2.addWidget(self.main_radioButton, 0, 0, 1, 1)

        self.clash_radioButton = QRadioButton(self.effect_groupbox)
        self.clash_radioButton.setObjectName(u"clash_radioButton")

        self.gridLayout_2.addWidget(self.clash_radioButton, 0, 1, 1, 1)

        self.swing_radioButton = QRadioButton(self.effect_groupbox)
        self.swing_radioButton.setObjectName(u"swing_radioButton")

        self.gridLayout_2.addWidget(self.swing_radioButton, 0, 2, 1, 1)

        self.main_color_label = QLabel(self.effect_groupbox)
        self.main_color_label.setObjectName(u"main_color_label")
        self.main_color_label.setAutoFillBackground(True)

        self.gridLayout_2.addWidget(self.main_color_label, 1, 0, 1, 1)

        self.clash_color_label = QLabel(self.effect_groupbox)
        self.clash_color_label.setObjectName(u"clash_color_label")
        self.clash_color_label.setAutoFillBackground(True)

        self.gridLayout_2.addWidget(self.clash_color_label, 1, 1, 1, 1)

        self.swing_color_label = QLabel(self.effect_groupbox)
        self.swing_color_label.setObjectName(u"swing_color_label")
        self.swing_color_label.setAutoFillBackground(True)

        self.gridLayout_2.addWidget(self.swing_color_label, 1, 2, 1, 1)

        self.gridLayout_2.setRowStretch(1, 1)

        self.gridLayout_3.addWidget(self.effect_groupbox, 1, 0, 1, 2)

        self.gridLayout_3.setRowStretch(0, 2)
        self.gridLayout_3.setRowStretch(1, 1)
        self.gridLayout_3.setColumnStretch(0, 1)
        self.content_tabWidget.addTab(self.color_tab, "")
        self.sound_tab = QWidget()
        self.sound_tab.setObjectName(u"sound_tab")
        self.erase_button = QPushButton(self.sound_tab)
        self.erase_button.setObjectName(u"erase_button")
        self.erase_button.setGeometry(QRect(210, 10, 100, 32))
        self.upload_button = QPushButton(self.sound_tab)
        self.upload_button.setObjectName(u"upload_button")
        self.upload_button.setGeometry(QRect(210, 140, 100, 32))
        self.content_tabWidget.addTab(self.sound_tab, "")

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
        self.menubar.setGeometry(QRect(0, 0, 859, 24))
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
        self.color_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Color Select", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"White", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Blue", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Green", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Red", None))
        self.controls_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.color_bank_select_box.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Color Bank", None))
        self.reset_changes_button.setText(QCoreApplication.translate("MainWindow", u"Reset Changes", None))
        self.color_save_button.setText(QCoreApplication.translate("MainWindow", u"Save Bank to Saber", None))
        self.preview_button.setText(QCoreApplication.translate("MainWindow", u"Preview Color on Saber", None))
        self.effect_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Effect Select", None))
        self.main_radioButton.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.clash_radioButton.setText(QCoreApplication.translate("MainWindow", u"Clash", None))
        self.swing_radioButton.setText(QCoreApplication.translate("MainWindow", u"Swing", None))
        self.main_color_label.setText("")
        self.clash_color_label.setText("")
        self.swing_color_label.setText("")
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.color_tab), QCoreApplication.translate("MainWindow", u"Color", None))
        self.erase_button.setText(QCoreApplication.translate("MainWindow", u"Erase Sounds", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.sound_tab), QCoreApplication.translate("MainWindow", u"Sound", None))
        self.logTextBox.setPlaceholderText("")
        self.menuConnection.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.menuTroubleshooting.setTitle(QCoreApplication.translate("MainWindow", u"Troubleshooting", None))
        self.menuFirmware.setTitle(QCoreApplication.translate("MainWindow", u"Firmware", None))
    # retranslateUi

