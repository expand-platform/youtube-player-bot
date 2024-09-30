from typing import Any
from telebot.types import Message

from src.users.User import User 
from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS, ADMIN_SLASH_COMMANDS
from src.bot.Bot import Bot
from src.utils.Dotenv import Dotenv

from src.utils.Logger import Logger




# Генерируем шаги, исходя из заданных критериев (step generator factory)

#? Данные, которые понадобятся для шага:

#? - access_level (always exists, one or multiple [array])
#? - next step (if exists, [State] or [next_step] or [register_next_step_handler] (preferred))
#? - User information (for tell admin especially, [class User])
#? - notify admin (if needed [text message], [User info])
#? - database update (if exists, [class MongoDB] if exists, [MongoDB method to use] if needed)
#? - custom send_message methods: [format_message], [send_messages]


#? General approach is next: 
#? 1) Generate /slash-command
#? 2) generate next_handler of some type (if needed)  
#? 3) generate next_handler(s) (if needed) (multiple handlers)  

#* 3 types of users: "guest", "student", "admin" 


class StepGenerator:
    def __init__(self, bot: Bot):
        self.logger = Logger()
        
        #* get launched bot instance as a parameter
        self.environment = Dotenv().environment
        self.bot = bot.bot_instance
        
        #* helpers
        self.send_multiple_messages = bot.send_multiple_messages
        self.send_formatted_message = bot.send_formatted_message
        
        self.tell_admin = bot.tell_admin
    
    
    def set_start(self, 
                access_level=["student", "admin"], 
                
                format_message: str = None, 
                format_variable: str = None,
                multiple_messages: list = None,
                notification_text = "зашёл в раздел /start ✅",
                
                # message options
                disable_preview = False,
                parse_mode = "Markdown",
                ):
        
        
        @self.bot.message_handler(commands=["start"], access_level=access_level)
        def handle_start(message: Message):
            #? Надеюсь, в будущем не будет проблем из-за одинакового названия функции 
            #? Если что, напишу helper-fn-name-generator
            self.set_slash_commands(message)
            user = User(message)
            
            if format_message:
                data_for_formatting = self.get_format_variable(format_variable, user)
                
                self.send_formatted_message(chat_id=user.chat_id, message=format_message, format_variable=data_for_formatting)
                
            if multiple_messages:
                self.send_multiple_messages(chat_id=user.chat_id, messages=multiple_messages)
            
            if notification_text:
                self.tell_admin(f"{ user.first_name } @{ user.username } {notification_text}")
                
            self.logger.info(f"{ user.first_name } {notification_text}")
    

    
    
    #* generate other /slash commands 
    def set_command(self,
                command = [""],
                access_level = ["student", "admin"], 
                
                format_message: str = None, 
                format_variable: str = None,
                multiple_messages: list = None,
                notification_text = "зашёл в раздел /start ✅",
                
                # message options
                disable_preview = False,
                parse_mode = "Markdown",
                ):
        
        
        @self.bot.message_handler(commands=command, access_level=access_level)
        def handle_command(message: Message):
            #? Надеюсь, в будущем не будет проблем из-за одинакового названия функции 
            #? Если что, напишу helper-fn-name-generator
            # self.set_slash_commands(message)
            user = User(message)
            
            if format_message:
                data_for_formatting = self.get_format_variable(format_variable, user)
                
                self.send_formatted_message(chat_id=user.chat_id, message=format_message, format_variable=data_for_formatting)
                
            if multiple_messages:
                self.send_multiple_messages(chat_id=user.chat_id, messages=multiple_messages)
            
            if notification_text:
                self.tell_admin(f"{ user.first_name } @{ user.username } {notification_text}")
                
            self.logger.info(f"{ user.first_name } {notification_text}")
    
    
    

    
    
    #* HELPERS

    def set_slash_commands(self, message):
        user = User(message)
        
        if user.access_level == "guest":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)
        
        elif user.access_level == "student":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
            
        elif user.access_level == "admin":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=ADMIN_SLASH_COMMANDS)
        
        self.logger.info('slash commands with right set')
    
    
    def get_format_variable(self, variable_name: Any, user: User):
        match variable_name:
            case "user.first_name":
                return user.first_name
            case "user.real_name":
                return user.real_name
    
    
    
    
    
    #* MESSAGE TYPES
    # helpers (type of step)
    def inline_buttons_step(self):
        pass
    
    # helpers (type of step)
    def text_input_step(self):
        pass
    
    
    
    