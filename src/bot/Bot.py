from telebot import TeleBot
from telebot.states.sync.middleware import StateMiddleware
from telebot.custom_filters import StateFilter, IsDigitFilter, TextMatchFilter

from src.bot.Filters import AccessLevelFilter

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.database.Cache import Cache
from src.database.Database import Database




class Bot:
    """class to connect and run bot"""

    _bot_instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._bot_instance is None:
            cls._bot_instance = super(Bot, cls).__new__(cls)
        return cls._bot_instance


    def __init__(self):
        self.dotenv = Dotenv()
        self.bot_token = self.dotenv.bot_token
        self.logger = Logger()

        self.bot_instance = None
        self.bot_username = None
        
        self.connect_telegram()
        

    def connect_telegram(self) -> TeleBot:
        self.bot_instance = TeleBot(token=self.bot_token, use_class_middlewares=True)
        
        bot_name = self.get_bot_data(bot=self.bot_instance, requested_data="first_name")
        
        if self.bot_instance:
            self.logger.info(f"Подключаюсь к боту '{bot_name}'...")
            self.tell_admin("Начинаю работу...")
            self.tell_admin("/start")
            
        self.bot_username = self.get_bot_data(bot=self.bot_instance, requested_data="username")
        
        
    # enable bot to listening for commands
    def connect_bot(self) -> None:
        bot_username = self.get_bot_data(bot=self.bot_instance, requested_data="username")
        self.logger.info(f"Бот @{bot_username} подключён! Нажми /start для начала")
        
        self.set_infinity_polling()
        

    def set_infinity_polling(self):
        """ change polling options based on environment """
        environment = self.dotenv.environment
        
        if environment == "development":
            self.bot_instance.infinity_polling(timeout=5, skip_pending=True, long_polling_timeout=20, restart_on_change=True)
            
        else:
            self.bot_instance.infinity_polling(timeout=5, skip_pending=True, long_polling_timeout=20)
            

    def get_bot_data(self, bot: TeleBot, requested_data: str) -> str:
        """gets bot's name, @username etc"""
        
        all_bot_info = bot.get_me()

        desired_info = getattr(all_bot_info, requested_data)
        return desired_info
    
    
    def start_bot(self) -> None:
        self.bot_instance.add_custom_filter(StateFilter(self.bot_instance))
        self.bot_instance.add_custom_filter(IsDigitFilter())
        self.bot_instance.add_custom_filter(TextMatchFilter())
        self.bot_instance.add_custom_filter(AccessLevelFilter(self.bot_instance))

        
        self.bot_instance.setup_middleware(StateMiddleware(self.bot_instance))
        
        self.connect_bot()
        
        
    def disconnect_bot(self) -> None:
        """ kills the active bot instance, drops connection """
        self.bot_instance.stop_bot()
        self.logger.info('бот выключен ❌')
        
        
    def tell_admin(self, message: str) -> None:
        admin_ids = Cache().admin_ids
        # self.logger.info(f"admin_ids (tell_admin): { admin_ids }")
        
        
        for admin_id in admin_ids:
            # self.logger.info(f"admin_id: {admin_id}")
            self.bot_instance.send_message(chat_id=admin_id, text=message)
        
        
    def send_multiple_messages(self, chat_id, messages: list, disable_preview=False, parse_mode="Markdown"):
        for message in messages:
            self.bot_instance.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode, disable_web_page_preview=disable_preview)
    
        
    def send_message_with_variable(self, chat_id, message: str, format_variable, parse_mode="Markdown"):
        formatted_message = message.format(format_variable)
        self.bot_instance.send_message(chat_id=chat_id, text=formatted_message, parse_mode=parse_mode)
