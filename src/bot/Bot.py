from typing import Union


from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot.states.sync.middleware import StateMiddleware
from telebot.custom_filters import StateFilter, IsDigitFilter, TextMatchFilter

from src.bot.Filters import AccessLevelFilter

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.database.Cache import Cache


class Bot:
    """class to connect and run bot"""

    _new_bot_instance = None
    _bot: TeleBot = None
    
    def __new__(cls, *args, **kwargs):
        if cls._new_bot_instance is None:
            cls._new_bot_instance = super(Bot, cls).__new__(cls)
            cls._new_bot_instance._bot = TeleBot(token=Dotenv().bot_token, use_class_middlewares=True)
            
        return cls._new_bot_instance


    def __init__(self):
        self.log = Logger().info
        self.environment = Dotenv().environment
        
    def get_bot_instance(self):
        return self._bot
        

    def start_bot(self) -> TeleBot:
        if self._bot:
            self.set_middleware()
            
            self.tell_admin("Начинаю работу...")
            self.tell_admin("/start")
            
        bot_username = self.get_bot_data(bot=self._bot, requested_data="username")
        self.log(f"Бот @{bot_username} подключён! Нажми /start для начала")
        
        if self.environment == "development":
            self._bot.infinity_polling(timeout=5, skip_pending=True, long_polling_timeout=20, restart_on_change=True)

        self._bot.infinity_polling(timeout=5, skip_pending=True, long_polling_timeout=20)
        


    def get_bot_data(self, bot: TeleBot, requested_data: str) -> str:
        """gets bot's name, @username etc"""
        
        all_bot_info = bot.get_me()

        desired_info = getattr(all_bot_info, requested_data)
        return desired_info
    
    
    def set_middleware(self) -> None:
        self._bot.add_custom_filter(StateFilter(self._bot))
        self._bot.add_custom_filter(IsDigitFilter())
        self._bot.add_custom_filter(TextMatchFilter())
        self._bot.add_custom_filter(AccessLevelFilter(self._bot))
        
        self._bot.setup_middleware(StateMiddleware(self._bot))
        
        
    def disconnect_bot(self) -> None:
        """ kills the active bot instance, drops connection """
        self._bot.stop_bot()
        self.log('бот выключен ❌')
        
        
    def tell_admin(self, message: str) -> None:
        admin_ids = Cache().admin_ids
        
        for admin_id in admin_ids:
            self._bot.send_message(chat_id=admin_id, text=message)
        
        
    def send_multiple_messages(self, chat_id, messages: list, disable_preview=False, parse_mode="Markdown"):
        for message in messages:
            self._bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode, disable_web_page_preview=disable_preview)
    
        
    def send_message_with_variable(self, chat_id: int, message: str, reply_markup: InlineKeyboardMarkup, format_variable: Union[str, int], parse_mode="Markdown"):
        # self.log(f"message (bot): { message }")
        # self.log(f"format_variable (bot): { format_variable }")
        
        formatted_message = message.format(format_variable)
        self._bot.send_message(chat_id=chat_id, text=formatted_message, reply_markup=reply_markup, parse_mode=parse_mode)
