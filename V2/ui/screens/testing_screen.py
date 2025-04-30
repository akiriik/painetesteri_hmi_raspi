import sys
import os
from PyQt5.QtWidgets import QLCDNumber, QLabel
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from ui.screens.base_screen import BaseScreen
from utils.pressure_reader import PressureReaderThread

# Add path for the sensor module
from utils.mpx5700.DFROBOT_MPX5700 import DFRobot_MPX5700_I2C

# Try to import the sensor module
try:
    from utils.mpx5700.DFROBOT_MPX5700 import DFRobot_MPX5700_I2C
except ImportError:
    print("Varoitus: DFRobot_MPX5700_I2C-moduulia ei löydy")
    DFRobot_MPX5700_I2C = None

class TestingScreen(BaseScreen):
    def __init__(self, parent=None):
        self.sensor = None
        self.pressure_thread = None
        super().__init__(parent)
        
        # Initialize pressure sensor
        self.init_pressure_sensor()
    
    def init_ui(self):
        # Page title
        self.title = self.create_title("TESTAUS")
        
        # Create LCD display for pressure reading
        self.pressure_lcd = QLCDNumber(self)
        self.pressure_lcd.setDigitCount(6)
        self.pressure_lcd.setSegmentStyle(QLCDNumber.Flat)
        self.pressure_lcd.setStyleSheet("background-color: black; color: white;")
        self.pressure_lcd.setGeometry(440, 200, 400, 150)
        
        # Pressure unit and description
        self.pressure_label = QLabel("Ilmanpaine (kPa)", self)
        self.pressure_label.setFont(self.subtitle_font)
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setGeometry(0, 370, 1280, 60)
    
    def init_pressure_sensor(self):
        if DFRobot_MPX5700_I2C is not None:
            try:
                self.sensor = DFRobot_MPX5700_I2C(1, 0x16)
                self.sensor.set_mean_sample_size(1)
                print("Paineanturi alustettu onnistuneesti")
                
                # Start pressure reading in a separate thread
                self.pressure_thread = PressureReaderThread(self.sensor)
                self.pressure_thread.pressureUpdated.connect(self.pressure_lcd.display)
                self.pressure_thread.start()
            except Exception as e:
                print(f"Paineanturin alustusvirhe: {e}")
                self.sensor = None
    
    def cleanup(self):
        # Stop the pressure thread if it's running
        if self.pressure_thread is not None:
            self.pressure_thread.stop()
            self.pressure_thread.wait()
            self.pressure_thread = None