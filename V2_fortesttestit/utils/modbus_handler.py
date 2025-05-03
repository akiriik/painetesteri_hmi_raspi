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
            # Päivitetty syntaksi pymodbus 3.9.2:lle
            result = self.client.write_register(register, state)
            return not result.isError() if hasattr(result, 'isError') else bool(result)
        except Exception as e:
            print(f"Releen {relay_num} ohjausvirhe: {e}")
            return False
    
    def read_holding_registers(self, address, count):
        """Lukee holding-rekistereitä"""
        if not self.connected:
            print("Modbus-yhteys ei ole päällä")
            return None
            
        try:
            result = self.client.read_holding_registers(address, count)
            return result
        except Exception as e:
            print(f"Rekisterien lukuvirhe: {e}")
            return None
    
    def write_coil(self, address, value):
        """Kirjoittaa coil-rekisteriin"""
        if not self.connected:
            print("Modbus-yhteys ei ole päällä")
            return False
            
        try:
            result = self.client.write_coil(address, value)
            return not result.isError() if hasattr(result, 'isError') else bool(result)
        except Exception as e:
            print(f"Coil-kirjoitusvirhe: {e}")
            return False
    
    def close(self):
        if self.client:
            self.client.close()