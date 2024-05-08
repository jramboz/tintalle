# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'about_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        if not AboutDialog.objectName():
            AboutDialog.setObjectName(u"AboutDialog")
        AboutDialog.resize(576, 423)
        icon = QIcon()
        icon.addFile(u":/img/tintalle.png", QSize(), QIcon.Normal, QIcon.Off)
        AboutDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AboutDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.icon_label = QLabel(AboutDialog)
        self.icon_label.setObjectName(u"icon_label")
        self.icon_label.setMaximumSize(QSize(100, 100))
        self.icon_label.setPixmap(QPixmap(u":/img/tintalle.png"))
        self.icon_label.setScaledContents(True)

        self.horizontalLayout_2.addWidget(self.icon_label, 0, Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(AboutDialog)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(64)
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3, 0, Qt.AlignmentFlag.AlignTop)

        self.version_label = QLabel(AboutDialog)
        self.version_label.setObjectName(u"version_label")
        font1 = QFont()
        font1.setPointSize(24)
        self.version_label.setFont(font1)

        self.verticalLayout_2.addWidget(self.version_label)

        self.desc_label = QLabel(AboutDialog)
        self.desc_label.setObjectName(u"desc_label")
        self.desc_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.desc_label, 0, Qt.AlignmentFlag.AlignTop)

        self.authors_label = QLabel(AboutDialog)
        self.authors_label.setObjectName(u"authors_label")

        self.verticalLayout_2.addWidget(self.authors_label)

        self.homepage_label = QLabel(AboutDialog)
        self.homepage_label.setObjectName(u"homepage_label")
        self.homepage_label.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.homepage_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.label = QLabel(AboutDialog)
        self.label.setObjectName(u"label")
        self.label.setWordWrap(True)
        self.label.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(AboutDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setWordWrap(True)
        self.label_2.setOpenExternalLinks(True)

        self.verticalLayout_2.addWidget(self.label_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.buttonBox = QDialogButtonBox(AboutDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(AboutDialog)
        self.buttonBox.accepted.connect(AboutDialog.accept)
        self.buttonBox.rejected.connect(AboutDialog.reject)

        QMetaObject.connectSlotsByName(AboutDialog)
    # setupUi

    def retranslateUi(self, AboutDialog):
        AboutDialog.setWindowTitle(QCoreApplication.translate("AboutDialog", u"About Tintall\u00eb", None))
        self.icon_label.setText("")
        self.label_3.setText(QCoreApplication.translate("AboutDialog", u"Tintall\u00eb", None))
        self.version_label.setText(QCoreApplication.translate("AboutDialog", u"Version ", None))
        self.desc_label.setText(QCoreApplication.translate("AboutDialog", u"Python/Qt-based application for managing OpenCore-based lightsabers.", None))
        self.authors_label.setText(QCoreApplication.translate("AboutDialog", u"Developed by: ", None))
        self.homepage_label.setText(QCoreApplication.translate("AboutDialog", u"Homepage: ", None))
        self.label.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p><a href=\"https://www.flaticon.com/free-icons/lightsaber\"><span style=\" text-decoration: underline; color:#3586ff;\">Lightsaber icons created by Nhor Phai - Flaticon</span></a></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("AboutDialog", u"<html><head/><body><p>This program is free software: you can redistribute it and/or modify it under the terms of the <a href=\"https://www.gnu.org/licenses/\"><span style=\" text-decoration: underline; color:#3586ff;\">GNU General Public License</span></a> as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p></body></html>", None))
    # retranslateUi

