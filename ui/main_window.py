import sys
import os
from PyQt5.QtWidgets import QWidget, QPushButton, QStackedWidget
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QKeyEvent

# Import screens
from ui.screens.home_screen import HomeScreen
from ui.screens.program_screen import ProgramScreen
from ui.screens.testing_screen import TestingScreen
from ui.screens.manual_screen import ManualScreen
from ui.screens.modbus_screen import ModbusScreen

# Import components
from ui.components.navbar import NavigationBar

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Configure main window
        self.setWindowTitle("Painetestaus")
        self.setGeometry(0, 0, 1280, 720)
        self.setStyleSheet("background-color: white;")
        
        # Create stacked widget for content pages
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(0, 0, 1280, 650)
        
        # Create screens
        self.screens = [
            HomeScreen(self),
            ProgramScreen(self),
            TestingScreen(self),
            ManualScreen(self),
            ModbusScreen(self)
        ]
        
        # Add screens to stacked widget
        for screen in self.screens:
            self.stacked_widget.addWidget(screen)
        
        # Create navigation bar
        self.navbar = NavigationBar(self)
        self.navbar.setGeometry(0, 650, 1280, 70)
        
        # Connect navigation signals
        self.navbar.screen_changed.connect(self.change_screen)
        
        # Create close button
        self.close_btn = QPushButton("X", self)
        self.close_btn.setGeometry(1240, 10, 30, 30)
        self.close_btn.setStyleSheet("background-color: red; color: white; border-radius: 15px;")
        self.close_btn.clicked.connect(self.close)
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()  # Close application with ESC key
        super().keyPressEvent(event)
    
    def change_screen(self, index):
        # Change to the selected screen
        self.stacked_widget.setCurrentIndex(index)
    
    def show(self):
        # Start in fullscreen mode
        self.showFullScreen()
    
    def closeEvent(self, event):
        # Clean up all screens before closing
        for screen in self.screens:
            screen.cleanup()
        super().closeEvent(event)