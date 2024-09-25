from telebot import TeleBot, custom_filters
from telebot.custom_filters import AdvancedCustomFilter
from src.users.User import User

from src.utils.Logger import Logger


class AccessLevelFilter(AdvancedCustomFilter):
    key = 'access_level'

    def __init__(self, bot):
        self.bot = bot
        

    def check(self, message, access_level):
        user = User(message=message)

        # if a list...
        if isinstance(access_level, list):
            return user.access_level in access_level
       

