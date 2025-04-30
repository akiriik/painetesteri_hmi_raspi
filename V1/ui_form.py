# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QPushButton, QSizePolicy,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1280, 720)
        Widget.setWindowTitle(u"Painetestaus")
        Widget.setStyleSheet(u"background-color: white;")
        
        # Main content area
        self.contentFrame = QFrame(Widget)
        self.contentFrame.setObjectName(u"contentFrame")
        self.contentFrame.setGeometry(QRect(0, 0, 1280, 650))
        self.contentFrame.setFrameShape(QFrame.NoFrame)
        self.contentFrame.setFrameShadow(QFrame.Raised)
        
        # Main title
        self.mainTitle = QLabel(self.contentFrame)
        self.mainTitle.setObjectName(u"mainTitle")
        self.mainTitle.setGeometry(QRect(0, 240, 1280, 100))
        font = QFont()
        font.setPointSize(42)
        font.setBold(True)
        self.mainTitle.setFont(font)
        self.mainTitle.setAlignment(Qt.AlignCenter)
        self.mainTitle.setText(u"-PAINETESTAUS-")
        
        # Subtitle
        self.subtitle = QLabel(self.contentFrame)
        self.subtitle.setObjectName(u"subtitle")
        self.subtitle.setGeometry(QRect(0, 360, 1280, 60))
        font1 = QFont()
        font1.setPointSize(28)
        self.subtitle.setFont(font1)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setText(u"VALMIUSTILASSA")
        
        # Navigation bar
        self.navBar = QFrame(Widget)
        self.navBar.setObjectName(u"navBar")
        self.navBar.setGeometry(QRect(0, 650, 1280, 70))
        self.navBar.setStyleSheet(u"background-color: white; border-top: 1px solid #dddddd;")
        self.navBar.setFrameShape(QFrame.NoFrame)
        self.navBar.setFrameShadow(QFrame.Raised)
        
        # Navigation buttons
        buttonWidth = 256  # 1280/5 = 256 pixels per button
        buttonLabels = ["ETUSIVU", "OHJELMA", "TESTAUS", "KÄSIKAYTTO", "MODBUS"]
        
        for i, label in enumerate(buttonLabels):
            button = QPushButton(self.navBar)
            button.setObjectName(f"navButton{i}")
            button.setGeometry(QRect(i * buttonWidth, 0, buttonWidth, 70))
            button.setText(label)
            
            # Apply different style for first button (active)
            if i == 0:
                button.setStyleSheet(u"background-color: #2196F3; color: white; border: none; font-weight: bold; font-size: 18px;")
            else:
                button.setStyleSheet(u"background-color: white; color: #555555; border: none; font-weight: bold; font-size: 18px;")

        QMetaObject.connectSlotsByName(Widget)