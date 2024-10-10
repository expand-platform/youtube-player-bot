from typing import Any
from telebot.types import Message

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS

from src.bot.Bot import Bot

from src.database.Database import Database

from src.languages.Language import Language



class StepGenerator:
    def __init__(self, bot: Bot):
        self.logger = Logger()
        
        self.environment = Dotenv().environment
        self.bot = bot.bot_instance
        
        self.send_multiple_messages = bot.send_multiple_messages
        self.send_message_with_variable = bot.send_message_with_variable
        self.tell_admin = bot.tell_admin
    

    #* generate any /slash commands 
    def set_command(self,
                command_name = "start",
                access_level = ["student", "admin"], 
                
                set_slash_command: bool = False,
                
                message_text: str = None,
                multiple_messages: list = None,
                
                format_message: str = None, 
                format_variable: str = None,
                
                messages_for_formatting: list = None,
                variables_for_formatting: list = None,
                
                mongodb_method_name: str = None,
                mongodb_activation_position: str = None,  # "before_messages", "after_messages"
                
                ):

        
        @self.bot.message_handler(commands=[command_name], access_level=access_level)
        def handle_command(message: Message):
            self.logger.info(f"(/{command_name}) работает ")
            active_user = Database().set_active_user(message)
            # user_name = Database().get_real_name(active_user, message)

            # self.logger.info(f"Бот использует (/{command_name}): { user_name }")
            
            
            if set_slash_command:
                self.set_slash_commands(active_user)
            
            if format_message:
                self.send_formatted_message(message_to_format=format_message, formatting_variable=format_variable, user=active_user)
                
            # multiple formatting messages
            if messages_for_formatting and variables_for_formatting:
                self.send_multiple_formatted_messages(messages=messages_for_formatting, formatting_variables=variables_for_formatting, user=active_user)
                
                
            if multiple_messages:
                self.send_multiple_messages(chat_id=active_user["user_id"], messages=multiple_messages)
                
            if message_text:
                self.bot.send_message(chat_id=active_user["user_id"], text=message_text, parse_mode="Markdown")
                
            if mongodb_activation_position == "after_messages" and mongodb_method_name:
                self.choose_database_method(method_name=mongodb_method_name, message=message)
            
            self.notify_admin(active_user=active_user, command_name=command_name)
    
    
    
    #? ADMIN COMMANDS 
    def set_admin_command(self, 
                        command_name: str = None,
                        message_suffix: str = "_success", 
                        # нужно называть сообщения в стиле "fill_success, clean_success" 
                        # для полной автоматизации
                        ):
        @self.bot.message_handler(commands=[command_name], access_level=["admin"])
        def set_admin_command(message: Message):
            self.choose_database_method(method_name=command_name, message=message)
            
            messages = Language().messages
            self.tell_admin(message=messages[command_name + message_suffix])
            
            
    
    #* HELPERS
    def notify_admin(self, active_user: dict, command_name):
        # check if user is admin
        if active_user["user_id"] in Database().admin_ids:
            self.logger.info(f"⚠ Admin here, don't sending notification: { active_user["real_name"] }")
            return
        
        real_name = active_user.get("real_name", active_user["first_name"]) 
        last_name = active_user.get("last_name", "")
        username = active_user["username"]
        
        self.tell_admin(message=f"{ real_name } { last_name } @{ username } зашёл в раздел /{command_name} ✅")
        self.logger.info(f"{ real_name } зашёл в раздел /{command_name} ✅")
    
    
    def set_slash_commands(self, active_user):
        if active_user["access_level"] == "guest":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)
        
        # if "student" or "admin"
        else:
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
            
        self.logger.info('😎 slash commands set')
    
    
    
    def get_format_variable(self, variable_name: Any, active_user: dict):
        match variable_name:
            case "user.real_name":
                return active_user["real_name"]
            
            case "user.first_name":
                return active_user["first_name"]
            
            case "user.payment_amount":
                return active_user["payment_amount"]
            
            case "user.lessons_left":
                return active_user["lessons_left"]
                
            case "user.done":
                if active_user["lessons_left"] > 0:
                    return active_user["lessons_left"] - 1
                
                else: return 0  # when zero lessons left
            
    
    def send_formatted_message(self, message_to_format, formatting_variable, user):
        data_for_formatting = self.get_format_variable(formatting_variable, user)
                
        self.send_message_with_variable(chat_id=user["user_id"], message=message_to_format, format_variable=data_for_formatting)


    def send_multiple_formatted_messages(self, messages, formatting_variables, user):
        formatting_data = []
        
        for variable in formatting_variables:
            data = self.get_format_variable(variable, user)
            formatting_data.append(data)
        
        self.logger.info(f"formatting_data: { formatting_data }")
        
        for message, format_data in zip(messages, formatting_data):
            # self.logger.info(f"message: { message }")
            # self.logger.info(f"format_data: { format_data }")
            self.send_message_with_variable(chat_id=user["user_id"], message=message, format_variable=format_data)
            
        self.logger.info(f"send_multiple_formatted_messages done 🥙")
        
    
    def choose_database_method(self, method_name: str, message: Message):
        match method_name:
            case "clean":
                Database().clean_users()
            
            case "fill":
                # Database().fill_database_from_scratch()
                Database().sync_cache_and_remote_users()
                
            case "update_lessons":
                self.logger.info(f"updating_lessons...")
                Database().update_lessons(message)
                
                


    
    #* MESSAGE TYPES
    # helpers (type of step)
    def inline_buttons_step(self):
        pass
    
    # helpers (type of step)
    def text_input_step(self):
        pass
    
    
    
    