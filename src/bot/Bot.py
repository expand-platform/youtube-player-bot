from telebot import TeleBot
from telebot.states.sync.middleware import StateMiddleware
from telebot.custom_filters import StateFilter, IsDigitFilter, TextMatchFilter

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger


class Bot:
    """class to connect and run bot"""

    def __init__(self):
        self.bot_token = Dotenv().bot_token
        self.admin_id = Dotenv().admin_id
        
        self.logger = Logger()

        self.bot = None
        self.username = None
        
        self.connect_telegram()
        

    def connect_telegram(self) -> TeleBot:
        self.bot = TeleBot(token=self.bot_token, use_class_middlewares=True)
        
        bot_name = self.get_bot_data(bot=self.bot, requested_data="first_name")
        if self.bot:
            self.logger.info(f"Подключаюсь к боту '{bot_name}'...")
            self.tell_admin("Начинаю работу...")
            self.tell_admin("/start")
            
        self.username = self.get_bot_data(bot=self.bot, requested_data="username")
        
        
    # enable bot to listening for commands
    def connect_bot(self) -> None:
        bot_username = self.get_bot_data(bot=self.bot, requested_data="username")
        self.logger.info(f"Бот @{bot_username} подключён! Нажми /start для начала")
        
        self.bot.infinity_polling(timeout=5, skip_pending=True, long_polling_timeout=20)


    def get_bot_data(self, bot: TeleBot, requested_data: str) -> str:
        """gets bot's name, @username etc"""
        
        all_bot_info = bot.get_me()

        desired_info = getattr(all_bot_info, requested_data)
        return desired_info
    
    
    def tell_admin(self, message):
        self.bot.send_message(chat_id=self.admin_id, text=message)
        
        
    def send_messages(self, chat_id, messages: list):
        for message in messages:
            self.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        
    
    def start_bot(self) -> None:
        self.bot.add_custom_filter(StateFilter(self.bot))
        self.bot.add_custom_filter(IsDigitFilter())
        self.bot.add_custom_filter(TextMatchFilter())
        
        self.bot.setup_middleware(StateMiddleware(self.bot))
        
        self.tell_admin(message="/start")
        
        self.connect_bot()
        
        
    def disconnect_bot(self) -> None:
        """ kills the active bot instance, drops connection """
        self.bot.stop_bot()
        self.logger.info('бот выключен ❌')

            
        
class AdsBot(Bot):
    pass


class SchoolBot(Bot):
    pass


class NotificatorBot(Bot):
    def __init__(self):
        super().__init__()
        self.bot_token = Dotenv().notificator_bot_token