# This Python file uses the following encoding: utf-8
import sys
import os

# ========== KOMMENTOI POIS WINDOWSISSA, PALAUTA RASPILLA ==========
# Lisää oikea polku moduulille
# sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mpx5700"))
# tai jos testi1 ja mpx5700 ovat rinnakkaiset kansiot:
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mpx5700"))
# ===============================================================

# ========== KOMMENTOI POIS WINDOWSISSA, PALAUTA RASPILLA ==========
# from DFROBOT_MPX5700 import DFRobot_MPX5700_I2C
# ===============================================================

# ========== KÄYTÄ VAIN WINDOWSISSA, KOMMENTOI POIS RASPILLA ==========
# Simuloitu anturi Windows-kehitystä varten
class MockSensor:
    def __init__(self, bus=None, addr=None):
        pass
        
    def get_pressure_value_kpa(self, samples=1):
        import random
        return random.uniform(90, 110)  # Simuloi painelukemia välillä 90-110 kPa
        
    def set_mean_sample_size(self, size):
        pass
# ===============================================================

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QKeyEvent

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyuic5 form.ui -o ui_form.py
from ui_form import Ui_Widget

# Lisää Widget-luokkaan erillinen säie paineanturin lukemiseen
class PressureReaderThread(QThread):
    pressureUpdated = pyqtSignal(float)
    
    def __init__(self, sensor):
        super().__init__()
        self.sensor = sensor
        self.running = True
        
    def run(self):
        while self.running:
            try:
                import time
                start_time = time.time()
                pressure = self.sensor.get_pressure_value_kpa(1)
                end_time = time.time()
                print(f"Lukemisaika: {(end_time-start_time)*1000:.1f}ms")
                self.pressureUpdated.emit(pressure)
            except Exception as e:
                print(f"Virhe paineanturin lukemisessa: {e}")
            self.msleep(100)
            
    def stop(self):
        self.running = False


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        
        # Configure main window
        self.setWindowTitle("Painetestaus")
        
        # Set up fonts
        self.title_font = QFont()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        
        self.subtitle_font = QFont()
        self.subtitle_font.setPointSize(28)
        
        # ========== KÄYTÄ VAIN WINDOWSISSA, KOMMENTOI POIS RASPILLA ==========
        # Käytetään simuloitua anturia Windows-kehityksessä
        self.mpx5700 = MockSensor()
        print("Simuloitu paineanturi käytössä")
        # ===============================================================
        
        # ========== KOMMENTOI POIS WINDOWSISSA, PALAUTA RASPILLA ==========
        # Alustetaan paineanturi
        # try:
        #     self.mpx5700 = DFRobot_MPX5700_I2C(1, 0x16)
        #     self.mpx5700.set_mean_sample_size(1)
        #     print("Paineanturi alustettu onnistuneesti")
        # except Exception as e:
        #     print(f"Paineanturin alustusvirhe: {e}")
        #     self.mpx5700 = None
        # ===============================================================

        # Create stacked widget for content pages
        self.stacked_widget = QStackedWidget(self)
        self.stacked_widget.setGeometry(0, 0, 1280, 650)
        
        # Create pages
        self.create_home_page()
        self.create_program_page()
        self.create_testing_page()
        self.create_manual_page()
        self.create_modbus_page()
        
        # Create navbar
        self.create_navbar()
        
        # Create close button
        self.close_btn = QPushButton("X", self)
        self.close_btn.setGeometry(1240, 10, 30, 30)
        self.close_btn.setStyleSheet("background-color: red; color: white; border-radius: 15px;")
        self.close_btn.clicked.connect(self.close)
        
        # Start in fullscreen mode
        self.showFullScreen()
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()  # Close application with ESC key
        super().keyPressEvent(event)
    
    def create_home_page(self):
        # Home page (similar to original design)
        home_page = QFrame()
        home_page.setStyleSheet("background-color: white;")
        
        # Create title
        main_title = QLabel("-PAINETESTAUS-", home_page)
        main_title.setFont(self.title_font)
        main_title.setAlignment(Qt.AlignCenter)
        main_title.setGeometry(0, 240, 1280, 100)
        
        # Create subtitle
        subtitle = QLabel("VALMIUSTILASSA", home_page)
        subtitle.setFont(self.subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setGeometry(0, 360, 1280, 60)
        
        self.stacked_widget.addWidget(home_page)
    
    def create_program_page(self):
        # Program page 
        program_page = QFrame()
        program_page.setStyleSheet("background-color: white;")
        
        # Page title
        title = QLabel("OHJELMA", program_page)
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(0, 50, 1280, 100)
        
        # Page content placeholder
        content = QLabel("Ohjelman asetukset tulevat tähän", program_page)
        content.setFont(self.subtitle_font)
        content.setAlignment(Qt.AlignCenter)
        content.setGeometry(0, 200, 1280, 60)
        
        self.stacked_widget.addWidget(program_page)
    
    def create_testing_page(self):
        # Testing page
        testing_page = QFrame()
        testing_page.setStyleSheet("background-color: white;")
        
        # Page title
        title = QLabel("TESTAUS", testing_page)
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(0, 50, 1280, 100)
        
        # Lisää LCD-näyttö painelukemalle
        from PyQt5.QtWidgets import QLCDNumber
        self.pressure_lcd = QLCDNumber(testing_page)
        self.pressure_lcd.setDigitCount(6)
        self.pressure_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.pressure_lcd.setStyleSheet("background-color: black; color: white;")
        self.pressure_lcd.setGeometry(440, 200, 400, 150)
        
        # Paineanturin yksikkö ja selite
        pressure_label = QLabel("Ilmanpaine (kPa)", testing_page)
        pressure_label.setFont(self.subtitle_font)
        pressure_label.setAlignment(Qt.AlignCenter)
        pressure_label.setGeometry(0, 370, 1280, 60)
        
        self.stacked_widget.addWidget(testing_page)
        
        # Käynnistä paineen lukeminen erillisessä säikeessä
        if hasattr(self, 'mpx5700') and self.mpx5700:
            self.pressure_thread = PressureReaderThread(self.mpx5700)
            self.pressure_thread.pressureUpdated.connect(self.pressure_lcd.display)
            self.pressure_thread.start()

    def create_manual_page(self):
        # Manual control page
        manual_page = QFrame()
        manual_page.setStyleSheet("background-color: white;")
        
        # Page title
        title = QLabel("KÄSIKÄYTTÖ", manual_page)
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(0, 50, 1280, 100)
        
        # Page content placeholder
        content = QLabel("Käsikäyttöasetukset tulevat tähän", manual_page)
        content.setFont(self.subtitle_font)
        content.setAlignment(Qt.AlignCenter)
        content.setGeometry(0, 200, 1280, 60)
        
        self.stacked_widget.addWidget(manual_page)
    
    def create_modbus_page(self):
        # Modbus page
        modbus_page = QFrame()
        modbus_page.setStyleSheet("background-color: white;")
        
        # Page title
        title = QLabel("MODBUS", modbus_page)
        title.setFont(self.title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setGeometry(0, 50, 1280, 100)
        
        # Page content placeholder
        content = QLabel("Modbus-asetukset tulevat tähän", modbus_page)
        content.setFont(self.subtitle_font)
        content.setAlignment(Qt.AlignCenter)
        content.setGeometry(0, 200, 1280, 60)
        
        self.stacked_widget.addWidget(modbus_page)
        
    def create_navbar(self):
        # Create navigation bar
        self.navbar = QFrame(self)
        self.navbar.setGeometry(0, 650, 1280, 70)
        self.navbar.setStyleSheet("background-color: white; border-top: 1px solid #dddddd;")
        
        # Button style
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
        
        # Create layout for navbar
        nav_layout = QHBoxLayout(self.navbar)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # Create navigation buttons
        button_labels = ["ETUSIVU", "OHJELMA", "TESTAUS", "KÄSIKÄYTTÖ", "MODBUS"]
        self.nav_buttons = []
        
        for i, label in enumerate(button_labels):
            btn = QPushButton(label)
            btn.setStyleSheet(self.inactive_style)
            btn.setMinimumSize(QSize(256, 70))  # 1280/5 = 256 pixels per button
            btn.clicked.connect(lambda checked, index=i: self.change_page(index))
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
        
        # Set ETUSIVU as active initially
        self.nav_buttons[0].setStyleSheet(self.active_style)
    
    def change_page(self, index):
        # Change to the selected page
        self.stacked_widget.setCurrentIndex(index)
        
        # Update button styles
        for i, btn in enumerate(self.nav_buttons):
            if i == index:
                btn.setStyleSheet(self.active_style)
            else:
                btn.setStyleSheet(self.inactive_style)

    def closeEvent(self, event):
        if hasattr(self, 'pressure_thread'):
            self.pressure_thread.stop()
            self.pressure_thread.wait()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())