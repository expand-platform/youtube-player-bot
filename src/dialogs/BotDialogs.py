from src.utils.Logger import Logger
from src.languages.Language import Language

from src.bot.Bot import Bot
from src.automation.StepGenerator import StepGenerator

from src.dialogs.AdminDialogs import AdminDialogs
from src.dialogs.UserDialogs import UserDialogs


class BotDialogs:
    def __init__(self):
        self.log = Logger().info
        self.step_generator = StepGenerator()
   
        
    def enable_dialogs(self):
        #? Включаем команды и диалоги админа и пользователей 
        UserDialogs().set_user_dialogs()
        AdminDialogs().set_admin_dialogs()
    
        self.log('Все команды и диалоги подключены ✅')


