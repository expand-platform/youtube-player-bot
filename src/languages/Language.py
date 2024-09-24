from src.languages.Ru import BOT_COMMANDS_RU, BOT_MESSAGES_RU
 

class Language:
    def __init__(self) -> None:
        # defaults
        self.active_lang = "ru"
        self.set_active_language_to(self.active_lang)
        
        
    def set_active_language_to(self, new_language="ru"):
        if new_language == "ru":
            self.commands = BOT_COMMANDS_RU
            self.messages = BOT_MESSAGES_RU

    
    def get_active_language(self):
        return self.active_lang
    
    
    def get_commands(self):
        return self.commands
    
    
    def get_messages(self):
        return self.messages
        
        