import sys
import os
from PyQt5.QtWidgets import QLCDNumber, QLabel, QPushButton, QFrame
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor
from ui.screens.base_screen import BaseScreen
from utils.pressure_reader import PressureReaderThread

# Yritä tuoda anturimoduuli
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
        
        # Alusta paineanturi
        self.init_pressure_sensor()
    
    def init_ui(self):
        # Sivun otsikko
        self.title = self.create_title("TESTAUS")
        
        # Luo taustakenttä mittarille
        self.display_panel = QFrame(self)
        self.display_panel.setGeometry(290, 150, 700, 320)
        self.display_panel.setStyleSheet("""
            background-color: #f0f0f0;
            border-radius: 15px;
            border: 2px solid #dddddd;
        """)
        
        # Luo QLabel-näyttö painelukemalle
        self.pressure_label = QLabel("0.00", self.display_panel)
        self.pressure_label.setStyleSheet("""
            background-color: black;
            color: #33FF33;
            font-family: 'Consolas', 'Courier', monospace;
            font-size: 80px;
            font-weight: bold;
            border: 2px solid #444444;
            border-radius: 10px;
        """)
        self.pressure_label.setAlignment(Qt.AlignCenter)
        self.pressure_label.setGeometry(150, 70, 400, 150)
        
        # Paineen yksikkö ja kuvaus
        self.unit_label = QLabel("kPa", self.display_panel)
        self.unit_label.setStyleSheet("""
            color: #333333;
            font-family: 'Arial', sans-serif;
            font-size: 50px;
            font-weight: bold;
        """)
        self.unit_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.unit_label.setGeometry(560, 70, 100, 150)
        
        # Alaotsikko
        self.info_label = QLabel("Ilmanpaine", self.display_panel)
        self.info_label.setStyleSheet("""
            color: #555555;
            font-family: 'Arial', sans-serif;
            font-size: 24px;
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setGeometry(150, 230, 400, 40)
        
        # Tilan indikaattori
        self.status_indicator = QFrame(self.display_panel)
        self.status_indicator.setGeometry(50, 50, 30, 30)
        self.status_indicator.setStyleSheet("""
            background-color: #4CAF50; 
            border-radius: 15px;
            border: 2px solid #388E3C;
        """)
        
        # Mittarin nollausnappi
        self.reset_button = QPushButton("NOLLAA", self)
        self.reset_button.setGeometry(550, 500, 180, 60)
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border-radius: 10px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        
        # Liitä painikkeen signaali anturin kalibrointiin
        if DFRobot_MPX5700_I2C is not None:
            self.reset_button.clicked.connect(self.calibrate_sensor)
        else:
            self.reset_button.setEnabled(False)

    def init_pressure_sensor(self):
        if DFRobot_MPX5700_I2C is not None:
            try:
                self.sensor = DFRobot_MPX5700_I2C(1, 0x16)
                self.sensor.set_mean_sample_size(5)  # Kasvatettu tasaisuuden parantamiseksi
                print("Paineanturi alustettu onnistuneesti")
                
                # Aloita paineen lukeminen erillisessä säikeessä
                self.pressure_thread = PressureReaderThread(self.sensor)
                self.pressure_thread.pressureUpdated.connect(self.update_pressure)
                self.pressure_thread.start()
            except Exception as e:
                print(f"Paineanturin alustusvirhe: {e}")
                self.sensor = None
                if hasattr(self, 'status_indicator'):
                    self.status_indicator.setStyleSheet("""
                        background-color: #F44336; 
                        border-radius: 15px;
                        border: 2px solid #D32F2F;
                    """)
    
    def update_pressure(self, value):
        """Päivitä painelukema näytölle"""
        # Päivitä arvo digitaalinäyttöön
        self.pressure_label.setText(f"{value:.2f}")
        
        # Muuta väri paineen mukaan (vihreä=normaali, keltainen=korkea, punainen=kriittinen)
        if value > 500:
            color = "#F44336"  # Punainen
        elif value > 300:
            color = "#FFC107"  # Keltainen
        else:
            color = "#33FF33"  # Vihreä
            
        self.pressure_label.setStyleSheet(f"""
            background-color: black;
            color: {color};
            font-family: 'Consolas', 'Courier', monospace;
            font-size: 80px;
            font-weight: bold;
            border: 2px solid #444444;
            border-radius: 10px;
        """)
    
    def calibrate_sensor(self):
        """Kalibroi paineanturi näyttämään 0 kPa"""
        if self.sensor is not None:
            try:
                # Aseta paine arvoon 0 kPa nykyisen paineen sijaan
                self.sensor.calibration_kpa(0)
                
                # Päivitä näyttö
                self.info_label.setText("Anturi nollattu")
                
                # Palauta teksti takaisin normaaliksi hetken kuluttua
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(3000, lambda: self.info_label.setText("Ilmanpaine"))
                
            except Exception as e:
                print(f"Kalibrointivirhe: {e}")
                self.info_label.setText("Virhe nollauksessa")
    
    def cleanup(self):
        # Pysäytä säie jos se on käynnissä
        if self.pressure_thread is not None:
            self.pressure_thread.stop()
            self.pressure_thread.wait()
            self.pressure_thread = None