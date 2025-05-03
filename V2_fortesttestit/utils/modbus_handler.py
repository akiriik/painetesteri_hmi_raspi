# Modbus-luokka releiden ohjausta varten
class ModbusHandler:
    def __init__(self, port='/dev/ttyUSB0', baudrate=19200):
        self.port = port
        self.baudrate = baudrate
        self.client = None
        self.connected = False
        self.setup_modbus()
        
    def setup_modbus(self):
        try:
            from pymodbus.client import ModbusSerialClient
            self.client = ModbusSerialClient(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=0.5
            )
            self.connected = self.client.connect()
            print(f"Modbus-yhteys: {'Onnistui' if self.connected else 'Epäonnistui'}")
        except Exception as e:
            self.connected = False
            print(f"Modbus-virhe: {e}")
            
    def toggle_relay(self, relay_num, state):
        if not self.connected:
            print("Modbus-yhteys ei ole päällä")
            return False
            
        try:
            # Käytä rekistereitä 18099-18106 releille 1-8
            register = 18098 + relay_num
            print(f"Ohjataan relettä {relay_num}, rekisteri {register}, tila {state}")
            result = self.client.write_register(register, state, slave=1)
            return bool(result)
        except Exception as e:
            print(f"Releen {relay_num} ohjausvirhe: {e}")
            return False
    
    def close(self):
        if self.client:
            self.client.close()