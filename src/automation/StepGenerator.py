from typing import Any
from telebot.types import Message

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS, ADMIN_SLASH_COMMANDS

from src.bot.Bot import Bot
from src.users.Users import Users
from src.database.MongoDB import MongoDB







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
    

    #* generate other /slash commands 
    def set_command(self,
                command_name = "start",
                access_level = ["student", "admin"], 
                
                set_slash_command: bool = False,
                
                message_text: str = None,
                format_message: str = None, 
                format_variable: str = None,
                multiple_messages: list = None,
                
                mongo_method: str = None,
                
                # message options
                disable_preview = False,
                parse_mode = "Markdown",
                ):
        
        
        @self.bot.message_handler(commands=[command_name], access_level=access_level)
        def handle_command(message: Message):
            user = Users(message=message, bot=self.bot)
            user = user.get_active_user()
            self.logger.info(f"Текущий пользователь (/start): { user }")
            
            if set_slash_command:
                self.set_slash_commands(user)
            
            
            if format_message:
                data_for_formatting = self.get_format_variable(format_variable, user)
                
                self.send_formatted_message(chat_id=user["user_id"], message=format_message, format_variable=data_for_formatting)
                
            if multiple_messages:
                self.send_multiple_messages(chat_id=user["user_id"], messages=multiple_messages)
                
            if message_text:
                self.bot.send_message(chat_id=user["user_id"], text=message_text)
                
            #? Ну а дальше уже потом придумаю. 
            #? Думаю тут просто будут захардкожены разные варианты событий
            #? Типа, если оплата, сделать 1,2,3 и вывести это туда-то
            #? Если обновить имя, то А,Б и т.д
            if mongo_method:
                database_method = self.choose_mongo_method()
                database_method()
                
            
            self.notify_admin(user, command_name)
            
    
    
    #* HELPERS
    def set_slash_commands(self, user):
        if user["access_level"] == "guest":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)
        
        elif user["access_level"] == "student":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
            
        elif user["access_level"] == "admin":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=ADMIN_SLASH_COMMANDS)
        
        self.logger.info('slash commands with rights set')
    
    
    def get_format_variable(self, variable_name: Any, user: Users):
        match variable_name:
            case "user.first_name":
                return user["first_name"]
            case "user.real_name":
                return user["real_name"]
            case "user.payment":
                return user["payment_amount"]
    
            
    def notify_admin(self, user, command_name):
        self.tell_admin(f"{ user["real_name"] } { user["last_name"] } { user["first_name"] } @{ user["username"] } зашёл в раздел /{command_name} ✅")
        self.logger.info(f"{ user["first_name"] } зашёл в раздел /{command_name} ✅")
    
    
    def choose_mongo_method(self, method_name: Any):
        match method_name:
            case "payment":
                return MongoDB.get_payment_data


    
    #* MESSAGE TYPES
    # helpers (type of step)
    def inline_buttons_step(self):
        pass
    
    # helpers (type of step)
    def text_input_step(self):
        pass
    
    
    
    