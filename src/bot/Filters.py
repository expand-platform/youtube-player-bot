from typing import Union
from mailbox import Message
from telebot.custom_filters import AdvancedCustomFilter

from telebot.types import Message, CallbackQuery

from src.utils.Logger import Logger
from src.database.Database import Database


class AccessLevelFilter(AdvancedCustomFilter):
    key = 'access_level'

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger()
        

    def check(self, message: Union[Message, CallbackQuery], access_level: str):
        self.logger.info(f"Filters (check)")
        # self.logger.info(f"message: { message }")
        # self.logger.info(f"message.from_user.id: { message.from_user.id }")
        # self.logger.info(f"message.chat.id: { message.chat.id }")
        
        #? keyboard reply
        if not hasattr(message, 'chat'):
            self.logger.info(f"no message.chat found: { message.message.chat.id }")
            message = message.message
            
        
        # self.logger.info(f"message.message.chat.id: { message.message.chat.id }")
        
        active_user = Database().detect_active_user(message)
        
        # user_name = Database().get_real_name(active_user)
        # self.logger.info(f"Бот использует (Filter.py): { user_name }")

        # if a list...
        if isinstance(access_level, list):
            return active_user["access_level"] in access_level
       

