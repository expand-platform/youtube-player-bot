from logging import log
from telebot.custom_filters import AdvancedCustomFilter

from src.utils.Logger import Logger
from src.database.Database import Database


class AccessLevelFilter(AdvancedCustomFilter):
    key = 'access_level'

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()
        

    def check(self, message, access_level):
        # self.logger.info(f"Filters (check)")
        active_user = Database().detect_active_user(message)
        
        # user_name = Database().get_real_name(active_user)
        # self.logger.info(f"Бот использует (Filter.py): { user_name }")

        # if a list...
        if isinstance(access_level, list):
            return active_user["access_level"] in access_level
       

