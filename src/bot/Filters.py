from telebot import TeleBot, custom_filters
from telebot.custom_filters import AdvancedCustomFilter
from src.users.Users import Users

from src.utils.Logger import Logger


class AccessLevelFilter(AdvancedCustomFilter):
    key = 'access_level'

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()
        

    def check(self, message, access_level):
        user = Users(message=message, bot=self.bot)
        self.logger.info(f"Текущий пользователь (Filter.py): { user }")
        self.logger.info(f"Текущий пользователь (Filter.py): { user.active_user }")

        # if a list...
        if isinstance(access_level, list):
            return user.active_user["access_level"] in access_level
       

