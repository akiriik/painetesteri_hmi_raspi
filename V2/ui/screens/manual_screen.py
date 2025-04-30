from ui.screens.base_screen import BaseScreen

class ManualScreen(BaseScreen):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def init_ui(self):
        # Page title
        self.title = self.create_title("KÄSIKÄYTTÖ")
        
        # Page content placeholder
        self.content = self.create_subtitle("Käsikäyttöasetukset tulevat tähän")