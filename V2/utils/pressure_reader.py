import time
from PyQt5.QtCore import QThread, pyqtSignal

class PressureReaderThread(QThread):
    pressureUpdated = pyqtSignal(float)
    
    def __init__(self, sensor):
        super().__init__()
        self.sensor = sensor
        self.running = True
        
    def run(self):
        while self.running:
            try:
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