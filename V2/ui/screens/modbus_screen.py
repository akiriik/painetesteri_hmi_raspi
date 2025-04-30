from ui.screens.base_screen import BaseScreen

class ModbusScreen(BaseScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def init_ui(self):
        # Page title
        self.title = self.create_title("MODBUS")
        
        # Page content placeholder
        self.content = self.create_subtitle("Modbus-asetukset tulevat tähän")