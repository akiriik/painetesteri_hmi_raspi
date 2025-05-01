from PyQt5.QtWidgets import QFrame, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, pyqtSignal

class NavigationBar(QFrame):
    # Signal emitted when a screen is selected
    screen_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: white; border-top: 1px solid #dddddd;")
        
        # Button styles
        self.inactive_style = """
            QPushButton {
                background-color: white;
                color: #555555;
                border: none;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """
        
        self.active_style = """
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                font-weight: bold;
                font-size: 18px;
            }
        """
        
        # Initialize UI elements
        self.init_ui()
    
    def init_ui(self):
        # Create layout for navbar
        nav_layout = QHBoxLayout(self)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # Create navigation buttons
        button_labels = ["ETUSIVU", "OHJELMA", "TESTAUS", "KÄSIKÄYTTÖ", "MODBUS"]
        self.nav_buttons = []
        
        for i, label in enumerate(button_labels):
            btn = QPushButton(label)
            btn.setStyleSheet(self.inactive_style)
            btn.setMinimumSize(QSize(256, 70))  # 1280/5 = 256 pixels per button
            
            # Connect button to slot that emits the screen_changed signal
            btn.clicked.connect(lambda checked, index=i: self.change_screen(index))
            
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
        
        # Set ETUSIVU as active initially
        self.nav_buttons[0].setStyleSheet(self.active_style)
        self.current_index = 0
    
    def change_screen(self, index):
        # Update button styles
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet(self.active_style)
            else:
                btn.setStyleSheet(self.inactive_style)
        
        self.current_index = index
        
        # Emit signal to change screen
        self.screen_changed.emit(index)