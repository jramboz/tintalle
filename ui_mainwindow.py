# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QStatusBar, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from qtexteditlogger import QTextEditLogger
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(897, 697)
        icon = QIcon()
        icon.addFile(u":/img/tintalle.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.action_Refresh_Ports = QAction(MainWindow)
        self.action_Refresh_Ports.setObjectName(u"action_Refresh_Ports")
        self.action_Refresh_Ports.setIconVisibleInMenu(True)
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
        self.action_Reload_Config.setIconVisibleInMenu(True)
        self.action_Reload_Config.setShortcutVisibleInContextMenu(True)
        self.action_Check_for_Latest_Firwmare = QAction(MainWindow)
        self.action_Check_for_Latest_Firwmare.setObjectName(u"action_Check_for_Latest_Firwmare")
        self.action_Install_Firmware_from_File = QAction(MainWindow)
        self.action_Install_Firmware_from_File.setObjectName(u"action_Install_Firmware_from_File")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.action_about.setIcon(icon)
        self.action_Save_Log_to_File = QAction(MainWindow)
        self.action_Save_Log_to_File.setObjectName(u"action_Save_Log_to_File")
        icon1 = QIcon(QIcon.fromTheme(u"document-save"))
        self.action_Save_Log_to_File.setIcon(icon1)
        self.action_Export_Anima_config_ini = QAction(MainWindow)
        self.action_Export_Anima_config_ini.setObjectName(u"action_Export_Anima_config_ini")
        icon2 = QIcon(QIcon.fromTheme(u"document-page-setup"))
        self.action_Export_Anima_config_ini.setIcon(icon2)
        self.action_Save_Colors = QAction(MainWindow)
        self.action_Save_Colors.setObjectName(u"action_Save_Colors")
        self.action_Save_Colors.setEnabled(False)
        self.action_Save_Colors.setIcon(icon1)
        self.action_Load_Colors = QAction(MainWindow)
        self.action_Load_Colors.setObjectName(u"action_Load_Colors")
        self.action_Load_Colors.setEnabled(False)
        icon3 = QIcon(QIcon.fromTheme(u"document-open"))
        self.action_Load_Colors.setIcon(icon3)
        self.action_Export_current_config = QAction(MainWindow)
        self.action_Export_current_config.setObjectName(u"action_Export_current_config")
        self.action_Reset_Saber_to_Defaults = QAction(MainWindow)
        self.action_Reset_Saber_to_Defaults.setObjectName(u"action_Reset_Saber_to_Defaults")
        self.action_Reset_Saber_to_Defaults.setEnabled(False)
        self.action_Anima_Terminal = QAction(MainWindow)
        self.action_Anima_Terminal.setObjectName(u"action_Anima_Terminal")
        self.action_Anima_Terminal.setEnabled(False)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.connection_groupBox = QGroupBox(self.centralwidget)
        self.connection_groupBox.setObjectName(u"connection_groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
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

        self.refresh_ports_button = QPushButton(self.connection_groupBox)
        self.refresh_ports_button.setObjectName(u"refresh_ports_button")
        icon4 = QIcon(QIcon.fromTheme(u"view-refresh"))
        self.refresh_ports_button.setIcon(icon4)

        self.horizontalLayout.addWidget(self.refresh_ports_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label_2 = QLabel(self.connection_groupBox)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.status_label = QLabel(self.connection_groupBox)
        self.status_label.setObjectName(u"status_label")

        self.horizontalLayout.addWidget(self.status_label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.g_slider = QSlider(self.color_groupbox)
        self.g_slider.setObjectName(u"g_slider")
        self.g_slider.setMaximum(255)
        self.g_slider.setOrientation(Qt.Orientation.Horizontal)
        self.g_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.g_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.g_slider, 1, 2, 1, 1)

        self.label_6 = QLabel(self.color_groupbox)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)

        self.w_spinbox = QSpinBox(self.color_groupbox)
        self.w_spinbox.setObjectName(u"w_spinbox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.w_spinbox.sizePolicy().hasHeightForWidth())
        self.w_spinbox.setSizePolicy(sizePolicy1)
        self.w_spinbox.setMinimumSize(QSize(45, 0))
        self.w_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.w_spinbox, 3, 1, 1, 1)

        self.b_slider = QSlider(self.color_groupbox)
        self.b_slider.setObjectName(u"b_slider")
        self.b_slider.setMaximum(255)
        self.b_slider.setOrientation(Qt.Orientation.Horizontal)
        self.b_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
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
        self.w_slider.setOrientation(Qt.Orientation.Horizontal)
        self.w_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.w_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.w_slider, 3, 2, 1, 1)

        self.g_spinbox = QSpinBox(self.color_groupbox)
        self.g_spinbox.setObjectName(u"g_spinbox")
        sizePolicy1.setHeightForWidth(self.g_spinbox.sizePolicy().hasHeightForWidth())
        self.g_spinbox.setSizePolicy(sizePolicy1)
        self.g_spinbox.setMinimumSize(QSize(45, 0))
        self.g_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.g_spinbox, 1, 1, 1, 1)

        self.r_slider = QSlider(self.color_groupbox)
        self.r_slider.setObjectName(u"r_slider")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.r_slider.sizePolicy().hasHeightForWidth())
        self.r_slider.setSizePolicy(sizePolicy2)
        self.r_slider.setMaximum(255)
        self.r_slider.setOrientation(Qt.Orientation.Horizontal)
        self.r_slider.setTickPosition(QSlider.TickPosition.TicksAbove)
        self.r_slider.setTickInterval(50)

        self.gridLayout.addWidget(self.r_slider, 0, 2, 1, 1)

        self.r_spinbox = QSpinBox(self.color_groupbox)
        self.r_spinbox.setObjectName(u"r_spinbox")
        sizePolicy1.setHeightForWidth(self.r_spinbox.sizePolicy().hasHeightForWidth())
        self.r_spinbox.setSizePolicy(sizePolicy1)
        self.r_spinbox.setMinimumSize(QSize(75, 0))
        self.r_spinbox.setMaximum(255)

        self.gridLayout.addWidget(self.r_spinbox, 0, 1, 1, 1)

        self.b_spinbox = QSpinBox(self.color_groupbox)
        self.b_spinbox.setObjectName(u"b_spinbox")
        sizePolicy1.setHeightForWidth(self.b_spinbox.sizePolicy().hasHeightForWidth())
        self.b_spinbox.setSizePolicy(sizePolicy1)
        self.b_spinbox.setMinimumSize(QSize(45, 0))
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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.reset_color_changes_button = QPushButton(self.controls_groupbox)
        self.reset_color_changes_button.setObjectName(u"reset_color_changes_button")

        self.verticalLayout.addWidget(self.reset_color_changes_button)

        self.color_save_button = QPushButton(self.controls_groupbox)
        self.color_save_button.setObjectName(u"color_save_button")

        self.verticalLayout.addWidget(self.color_save_button)

        self.save_all_banks_button = QPushButton(self.controls_groupbox)
        self.save_all_banks_button.setObjectName(u"save_all_banks_button")

        self.verticalLayout.addWidget(self.save_all_banks_button)

        self.preview_color_button = QPushButton(self.controls_groupbox)
        self.preview_color_button.setObjectName(u"preview_color_button")

        self.verticalLayout.addWidget(self.preview_color_button)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

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
        self.gridLayout_4 = QGridLayout(self.sound_tab)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.effects_groupbox = QGroupBox(self.sound_tab)
        self.effects_groupbox.setObjectName(u"effects_groupbox")
        self.verticalLayout_4 = QVBoxLayout(self.effects_groupbox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.poweron_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup = QButtonGroup(MainWindow)
        self.effects_buttonGroup.setObjectName(u"effects_buttonGroup")
        self.effects_buttonGroup.setExclusive(False)
        self.effects_buttonGroup.addButton(self.poweron_checkBox)
        self.poweron_checkBox.setObjectName(u"poweron_checkBox")

        self.verticalLayout_4.addWidget(self.poweron_checkBox)

        self.poweroff_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.poweroff_checkBox)
        self.poweroff_checkBox.setObjectName(u"poweroff_checkBox")

        self.verticalLayout_4.addWidget(self.poweroff_checkBox)

        self.hum_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.hum_checkBox)
        self.hum_checkBox.setObjectName(u"hum_checkBox")

        self.verticalLayout_4.addWidget(self.hum_checkBox)

        self.clash_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.clash_checkBox)
        self.clash_checkBox.setObjectName(u"clash_checkBox")

        self.verticalLayout_4.addWidget(self.clash_checkBox)

        self.swing_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.swing_checkBox)
        self.swing_checkBox.setObjectName(u"swing_checkBox")

        self.verticalLayout_4.addWidget(self.swing_checkBox)

        self.smoothswingA_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.smoothswingA_checkBox)
        self.smoothswingA_checkBox.setObjectName(u"smoothswingA_checkBox")

        self.verticalLayout_4.addWidget(self.smoothswingA_checkBox)

        self.smoothswingB_checkBox = QCheckBox(self.effects_groupbox)
        self.effects_buttonGroup.addButton(self.smoothswingB_checkBox)
        self.smoothswingB_checkBox.setObjectName(u"smoothswingB_checkBox")

        self.verticalLayout_4.addWidget(self.smoothswingB_checkBox)


        self.gridLayout_4.addWidget(self.effects_groupbox, 0, 1, 1, 1)

        self.files_groupbox = QGroupBox(self.sound_tab)
        self.files_groupbox.setObjectName(u"files_groupbox")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.files_groupbox.sizePolicy().hasHeightForWidth())
        self.files_groupbox.setSizePolicy(sizePolicy3)
        self.verticalLayout_3 = QVBoxLayout(self.files_groupbox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.reset_sound_changes_button = QPushButton(self.files_groupbox)
        self.reset_sound_changes_button.setObjectName(u"reset_sound_changes_button")

        self.verticalLayout_3.addWidget(self.reset_sound_changes_button)

        self.sound_save_button = QPushButton(self.files_groupbox)
        self.sound_save_button.setObjectName(u"sound_save_button")

        self.verticalLayout_3.addWidget(self.sound_save_button)

        self.auto_assign_effects_button = QPushButton(self.files_groupbox)
        self.auto_assign_effects_button.setObjectName(u"auto_assign_effects_button")

        self.verticalLayout_3.addWidget(self.auto_assign_effects_button)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.erase_button = QPushButton(self.files_groupbox)
        self.erase_button.setObjectName(u"erase_button")

        self.verticalLayout_3.addWidget(self.erase_button)

        self.upload_button = QPushButton(self.files_groupbox)
        self.upload_button.setObjectName(u"upload_button")

        self.verticalLayout_3.addWidget(self.upload_button)


        self.gridLayout_4.addWidget(self.files_groupbox, 2, 1, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.freespace_label = QLabel(self.sound_tab)
        self.freespace_label.setObjectName(u"freespace_label")

        self.horizontalLayout_3.addWidget(self.freespace_label)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.usedspace_label = QLabel(self.sound_tab)
        self.usedspace_label.setObjectName(u"usedspace_label")

        self.horizontalLayout_3.addWidget(self.usedspace_label)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.totalspace_label = QLabel(self.sound_tab)
        self.totalspace_label.setObjectName(u"totalspace_label")

        self.horizontalLayout_3.addWidget(self.totalspace_label)


        self.gridLayout_4.addLayout(self.horizontalLayout_3, 3, 0, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_4, 1, 1, 1, 1)

        self.files_treeWidget = QTreeWidget(self.sound_tab)
        self.files_treeWidget.setObjectName(u"files_treeWidget")
        self.files_treeWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.files_treeWidget.setProperty(u"showDropIndicator", False)
        self.files_treeWidget.setUniformRowHeights(True)
        self.files_treeWidget.setSortingEnabled(True)
        self.files_treeWidget.setColumnCount(2)
        self.files_treeWidget.header().setProperty(u"showSortIndicator", True)

        self.gridLayout_4.addWidget(self.files_treeWidget, 0, 0, 3, 1)

        self.content_tabWidget.addTab(self.sound_tab, "")

        self.verticalLayout_2.addWidget(self.content_tabWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.logTextBox = QTextEditLogger(self.centralwidget)
        self.logTextBox.setObjectName(u"logTextBox")
        self.logTextBox.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.logTextBox.sizePolicy().hasHeightForWidth())
        self.logTextBox.setSizePolicy(sizePolicy4)
        self.logTextBox.setMaximumSize(QSize(500, 16777215))
        self.logTextBox.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.logTextBox)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 897, 42))
        self.menuConnection = QMenu(self.menubar)
        self.menuConnection.setObjectName(u"menuConnection")
        self.menuTroubleshooting = QMenu(self.menubar)
        self.menuTroubleshooting.setObjectName(u"menuTroubleshooting")
        self.menuFirmware = QMenu(self.menubar)
        self.menuFirmware.setObjectName(u"menuFirmware")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConnection.menuAction())
        self.menubar.addAction(self.menuFirmware.menuAction())
        self.menubar.addAction(self.menuTroubleshooting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuConnection.addAction(self.action_Refresh_Ports)
        self.menuConnection.addAction(self.action_Reload_Config)
        self.menuConnection.addAction(self.action_Anima_Terminal)
        self.menuTroubleshooting.addAction(self.action_Show_Hide_Log)
        self.menuTroubleshooting.addAction(self.action_Debug_Mode)
        self.menuTroubleshooting.addAction(self.action_Save_Log_to_File)
        self.menuTroubleshooting.addSeparator()
        self.menuTroubleshooting.addAction(self.action_Reset_Saber_to_Defaults)
        self.menuFirmware.addAction(self.action_Check_for_Latest_Firwmare)
        self.menuFirmware.addAction(self.action_Install_Firmware_from_File)
        self.menuHelp.addAction(self.action_about)
        self.menuFile.addAction(self.action_Export_Anima_config_ini)
        self.menuFile.addAction(self.action_Save_Colors)
        self.menuFile.addAction(self.action_Load_Colors)

        self.retranslateUi(MainWindow)
        self.refresh_ports_button.clicked.connect(self.action_Refresh_Ports.trigger)

        self.content_tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Tintall\u00eb", None))
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
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"&About Tintall\u00eb", None))
        self.action_Save_Log_to_File.setText(QCoreApplication.translate("MainWindow", u"Save Log to File...", None))
        self.action_Export_Anima_config_ini.setText(QCoreApplication.translate("MainWindow", u"Export Anima &config.ini...", None))
#if QT_CONFIG(tooltip)
        self.action_Export_Anima_config_ini.setToolTip(QCoreApplication.translate("MainWindow", u"Save a copy of the saber's current config.ini", None))
#endif // QT_CONFIG(tooltip)
        self.action_Save_Colors.setText(QCoreApplication.translate("MainWindow", u"Save Colors...", None))
#if QT_CONFIG(tooltip)
        self.action_Save_Colors.setToolTip(QCoreApplication.translate("MainWindow", u"Save color banks to a file for later use", None))
#endif // QT_CONFIG(tooltip)
        self.action_Load_Colors.setText(QCoreApplication.translate("MainWindow", u"Load Colors...", None))
#if QT_CONFIG(tooltip)
        self.action_Load_Colors.setToolTip(QCoreApplication.translate("MainWindow", u"Load color banks from file", None))
#endif // QT_CONFIG(tooltip)
        self.action_Export_current_config.setText(QCoreApplication.translate("MainWindow", u"Export current config", None))
        self.action_Reset_Saber_to_Defaults.setText(QCoreApplication.translate("MainWindow", u"&Reset Saber to Defaults", None))
#if QT_CONFIG(tooltip)
        self.action_Reset_Saber_to_Defaults.setToolTip(QCoreApplication.translate("MainWindow", u"Reset saber to original default settings and sounds", None))
#endif // QT_CONFIG(tooltip)
        self.action_Anima_Terminal.setText(QCoreApplication.translate("MainWindow", u"Anima &Terminal", None))
        self.connection_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
#if QT_CONFIG(tooltip)
        self.refresh_ports_button.setToolTip(QCoreApplication.translate("MainWindow", u"Refresh Ports List", None))
#endif // QT_CONFIG(tooltip)
        self.refresh_ports_button.setText("")
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
        self.reset_color_changes_button.setText(QCoreApplication.translate("MainWindow", u"Reset Changes", None))
#if QT_CONFIG(tooltip)
        self.color_save_button.setToolTip(QCoreApplication.translate("MainWindow", u"Save the currently displayed bank to the saber", None))
#endif // QT_CONFIG(tooltip)
        self.color_save_button.setText(QCoreApplication.translate("MainWindow", u"Save Bank to Saber", None))
#if QT_CONFIG(tooltip)
        self.save_all_banks_button.setToolTip(QCoreApplication.translate("MainWindow", u"Save all color banks to saber", None))
#endif // QT_CONFIG(tooltip)
        self.save_all_banks_button.setText(QCoreApplication.translate("MainWindow", u"Save All Banks to Saber", None))
        self.preview_color_button.setText(QCoreApplication.translate("MainWindow", u"Preview Color on Saber", None))
        self.effect_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Effect Select", None))
        self.main_radioButton.setText(QCoreApplication.translate("MainWindow", u"Main", None))
        self.clash_radioButton.setText(QCoreApplication.translate("MainWindow", u"Clash", None))
        self.swing_radioButton.setText(QCoreApplication.translate("MainWindow", u"Swing", None))
        self.main_color_label.setText("")
        self.clash_color_label.setText("")
        self.swing_color_label.setText("")
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.color_tab), QCoreApplication.translate("MainWindow", u"Color", None))
        self.effects_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Effects", None))
        self.poweron_checkBox.setText(QCoreApplication.translate("MainWindow", u"Power On", None))
        self.poweroff_checkBox.setText(QCoreApplication.translate("MainWindow", u"Power Off", None))
        self.hum_checkBox.setText(QCoreApplication.translate("MainWindow", u"Hum", None))
        self.clash_checkBox.setText(QCoreApplication.translate("MainWindow", u"Clash", None))
        self.swing_checkBox.setText(QCoreApplication.translate("MainWindow", u"Swing", None))
        self.smoothswingA_checkBox.setText(QCoreApplication.translate("MainWindow", u"SmoothSwing A", None))
        self.smoothswingB_checkBox.setText(QCoreApplication.translate("MainWindow", u"SmoothSwing B", None))
        self.files_groupbox.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.reset_sound_changes_button.setText(QCoreApplication.translate("MainWindow", u"Reset Changes", None))
        self.sound_save_button.setText(QCoreApplication.translate("MainWindow", u"Save Changes", None))
        self.auto_assign_effects_button.setText(QCoreApplication.translate("MainWindow", u"Auto Assign Effects", None))
        self.erase_button.setText(QCoreApplication.translate("MainWindow", u"Erase Sounds", None))
        self.upload_button.setText(QCoreApplication.translate("MainWindow", u"Upload Files", None))
        self.freespace_label.setText(QCoreApplication.translate("MainWindow", u"Free Space: --- MB", None))
        self.usedspace_label.setText(QCoreApplication.translate("MainWindow", u"Used Space: --- MB", None))
        self.totalspace_label.setText(QCoreApplication.translate("MainWindow", u"Total Space: --- MB", None))
        ___qtreewidgetitem = self.files_treeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Size", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"File Name", None));
        self.content_tabWidget.setTabText(self.content_tabWidget.indexOf(self.sound_tab), QCoreApplication.translate("MainWindow", u"Sound", None))
        self.logTextBox.setPlaceholderText("")
        self.menuConnection.setTitle(QCoreApplication.translate("MainWindow", u"Connection", None))
        self.menuTroubleshooting.setTitle(QCoreApplication.translate("MainWindow", u"Troubleshooting", None))
        self.menuFirmware.setTitle(QCoreApplication.translate("MainWindow", u"Firmware", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

