import sys
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedWidget, QLabel, QFrame
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QRect
from PyQt5.QtGui import QKeyEvent, QFont

# Omat komponentit
from ui.screens.home_screen import HomeScreen
from ui.screens.program_screen import ProgramScreen
from ui.screens.testing_screen import TestingScreen
from ui.screens.manual_screen import ManualScreen
from ui.screens.modbus_screen import ModbusScreen
from ui.components.navbar import NavigationBar

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Konfiguroi pääikkuna
        self.setWindowTitle("Painetestaus")
        self.setGeometry(0, 0, 1280, 720)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333333;
            }
            QPushButton#closeButton {
                background-color: #F44336;
                color: white;
                border-radius: 15px;
                font-weight: bold;
            }
            QPushButton#closeButton:hover {
                background-color: #D32F2F;
            }
        """)
        
        # Luo header
        self.create_header()
        
        # Luo stacked widget sisältösivuille
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(0, 50, 1280, 600)
        
        # Luo näytöt
        self.screens = [
            HomeScreen(self),
            ProgramScreen(self),
            TestingScreen(self),
            ManualScreen(self),
            ModbusScreen(self)
        ]
        
        # Lisää näytöt stacked widgetiin
        for screen in self.screens:
            self.stacked_widget.addWidget(screen)
        
        # Luo navigointipalkki
        self.navbar = NavigationBar(self)
        self.navbar.setGeometry(0, 650, 1280, 70)
        
        # Yhdistä navigointisignaalit
        self.navbar.screen_changed.connect(self.change_screen)
        
        # Luo sulje-nappi
        self.close_btn = QPushButton("X", self)
        self.close_btn.setObjectName("closeButton")
        self.close_btn.setGeometry(1240, 10, 30, 30)
        self.close_btn.clicked.connect(self.close)
        
        # Nykyinen sivu
        self.current_index = 0
    
    def create_header(self):
        # Header-palkki
        self.header = QFrame(self)
        self.header.setGeometry(0, 0, 1280, 50)
        self.header.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        
        # Otsikko
        header_font = QFont()
        header_font.setPointSize(14)
        header_font.setBold(True)
        
        self.header_title = QLabel("PAINETESTAUSJÄRJESTELMÄ v2.0", self.header)
        self.header_title.setFont(header_font)
        self.header_title.setGeometry(20, 0, 500, 50)
        self.header_title.setStyleSheet("color: #2196F3;")
    
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()  # Sulje sovellus ESC-näppäimellä
        super().keyPressEvent(event)
    
    def change_screen(self, index):
        # Yksinkertaistettu näytön vaihto ilman animaatiota
        self.stacked_widget.setCurrentIndex(index)
        self.current_index = index
    
    def show(self):
        # Käynnistä kokoruututilassa
        self.showFullScreen()
    
    def closeEvent(self, event):
        # Siivoa kaikki näytöt ennen sulkemista
        for screen in self.screens:
            screen.cleanup()
        super().closeEvent(event)