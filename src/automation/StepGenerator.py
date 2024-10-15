from math import log
from typing import Any
from telebot import TeleBot
from telebot.types import Message
from telebot.states.sync.context import State, StateContext

from src.database.MongoDB import MongoDB
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
        self.notify_admins = bot.tell_admin
    

    #* generate any /slash commands 
    def set_command(self,
                command_name = "start",
                access_level = ["student", "admin"], 
                
                set_slash_command: bool = False,
                
                bot_before_message: str = None,
                bot_after_message: str = None,
                
                bot_after_multiple_messages: list = None,
                bot_before_multiple_messages: list = None,
                
                formatted_messages: str = None, 
                formatted_variables: str = None,
                
                mongodb_method_name: str = None,
                mongodb_activation_position: str = None,  # "before_messages", "after_messages"
                ):

        
        @self.bot.message_handler(commands=[command_name], access_level=access_level)
        def handle_command(message: Message):
            active_user = Database().detect_active_user(message)
            
            if set_slash_command:
                self.set_slash_commands(active_user)
            
            #? MongoDB (before messages)
            if mongodb_activation_position == "before_messages" and mongodb_method_name:
                self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message, active_user=active_user)
                
            #? Messages (before)
            if bot_before_message:
                self.bot.send_message(chat_id=active_user["user_id"], text=bot_before_message, parse_mode="Markdown")
                             
            if bot_before_multiple_messages:
                self.send_multiple_messages(chat_id=active_user["user_id"], messages=bot_before_multiple_messages)
                
            #? Formatted messages
            if formatted_messages and formatted_variables:
                self.format_message(messages=formatted_messages, formatting_variables=formatted_variables, user=active_user)
                
            #? After messages
            if bot_after_message:
                self.bot.send_message(chat_id=active_user["user_id"], text=bot_after_message, parse_mode="Markdown")
                
            if bot_after_multiple_messages:
                self.send_multiple_messages(chat_id=active_user["user_id"], messages=bot_after_multiple_messages)
                
            if mongodb_activation_position == "after_messages" and mongodb_method_name:
                self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message, active_user=active_user)
            
            self.notify_admin(active_user=active_user, command_name=command_name)
    
    
    
    #? ADMIN COMMANDS 
    def simple_admin_command(self, 
                        command_name: str = None,
                        
                        bot_extra_message: str = None,

                        mongodb_method_name: str = None,
                        mongodb_activation_position: str = "after_messages",  # "before_messages", 
                        ):
        @self.bot.message_handler(commands=[command_name], access_level=["admin"])
        def set_admin_command(message: Message):
            
            active_user = Database().detect_active_user(message)
            messages = Language().messages
            
            if mongodb_activation_position == "before_messages" and mongodb_method_name:
                self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message)

            if bot_extra_message:
                self.bot.send_message(chat_id=active_user["user_id"], text=bot_extra_message, parse_mode="Markdown")
            
            if mongodb_activation_position == "after_messages" and mongodb_method_name:
                self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message)
            
            # self.notify_admins(message=messages[command_name + bot_message_suffix])
            
            
    #? ADMIN COMMANDS 
    def admin_command_with_state(self, 
                        handler_type: str = "state",
                        command_name: str = None,
                        
                        active_state: StateContext = None,
                        next_state: StateContext = None,
                        
                        state_variable: str = None,

                        use_state_data: bool = False,
                        requested_state_data: str = None,
                        
                        bot_message: str = None,
                        
                        formatted_messages: list = None, 
                        formatted_variables: list = None,
                        
                        mongodb_activation_position: str = "after_messages",
                        mongodb_method_name: str = None,
                        
                        bot_reply: str = None,
                        
                        ):
        
        
        def set_admin_command(message: Message, state: StateContext):
                #? initial data
                active_user = Database().detect_active_user(message)
                messages = Language().messages
                
                
                #? Save state's data or remove it
                state_data = {}

                if next_state:
                    state.set(state=next_state)
                
                if active_state:
                    self.logger.info(f"user's reply: { message.text }")
                    
                    self.save_data_in_state(variable_name=state_variable, data_to_save=message.text, state=state)
                
                if use_state_data and requested_state_data:
                    state_data = self.get_state_data(requested_data=requested_state_data, state=state)
                    print("🐍 state_data: ", state_data)
                    
                if not next_state:
                    state.delete()


                #? DB action (before messages)                
                if mongodb_activation_position == "before_messages" and mongodb_method_name:
                    self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message, data_from_state=state_data)
                    
                    
                #? Messages
                if bot_message:
                    self.bot.send_message(chat_id=active_user["user_id"], text=bot_message, parse_mode="Markdown")
                    
                    
                if formatted_messages and formatted_variables:
                    self.format_message(messages=formatted_messages, formatting_variables=formatted_variables, user=active_user)
                

                #? MongoDB (end)
                if mongodb_activation_position == "after_messages" and mongodb_method_name:
                    self.choose_database_method(mongodb_method_name=mongodb_method_name, message=message, data_from_state=state_data)
                
                
                if bot_reply:
                    self.bot.send_message(chat_id=active_user["user_id"], text=bot_reply, parse_mode="Markdown")
        
        
        if handler_type == "command":
            self.bot.register_message_handler(set_admin_command, commands=[command_name], access_level=["admin"])
            
        if handler_type == "state":
            self.bot.register_message_handler(set_admin_command, state=active_state, access_level=["admin"])
            

    
    #* HELPERS
    def notify_admin(self, active_user: dict, command_name):
        # check if user is admin
        if active_user["user_id"] in Database().admin_ids:
            self.logger.info(f"⚠ Admin here, don't sending notification: { active_user["real_name"] }")
            return
        
        real_name = active_user.get("real_name", active_user["first_name"]) 
        last_name = active_user.get("last_name", "")
        username = active_user["username"]
        
        self.notify_admins(message=f"{ real_name } { last_name } @{ username } зашёл в раздел /{command_name} ✅")
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
                return active_user["lessons_left"]
            
            
    def send_formatted_message(self, message_to_format, formatting_variable, user):
        data_for_formatting = self.get_format_variable(formatting_variable, user)
                
        self.send_message_with_variable(chat_id=user["user_id"], message=message_to_format, format_variable=data_for_formatting)


    def format_message(self, messages: list, formatting_variables: list, user: dict):
        # print("🐍 messages (format_message): ", messages, type(messages))
        # print("🐍 formatting_variables (format_message): ", formatting_variables)
        formatting_data = []
        
        for variable in formatting_variables:
            data = self.get_format_variable(variable, user)
            formatting_data.append(data)
        
        # self.logger.info(f"formatting_data (format_message): { formatting_data }")
        
        for message, format_data in zip(messages, formatting_data):
            # self.logger.info(f"message (format_message): { message }")
            # self.logger.info(f"format_data (format_message): { format_data }")
            
            self.send_message_with_variable(chat_id=user["user_id"], message=message, format_variable=format_data)
            
        self.logger.info(f"format messages with no errors 🦸‍♀️")
        
    
    def choose_database_method(self, 
                               mongodb_method_name: str, 
                               message: Message, 
                               
                               active_user=None, 
                               
                               data_from_state=None
                            ):
        match mongodb_method_name:
            case "clean":
                Database().clean_users()
            
            case "fill":
                Database().sync_cache_and_remote_users()
                
            case "update_lessons":
                # self.logger.info(f"updating_lessons...")
                messages = Language().messages
                
                is_report_allowed = Database().check_done_reports_limit(max_lessons=active_user["max_lessons"], done_lessons=active_user["done_lessons"])

                
                #? Сценарий #1: отчёт можно заполнить
                if is_report_allowed: 
                    formatted_messages=[ messages["done"], messages["lessons_left"] ]
                    formatted_variables=["user.real_name", "user.done"]
                    
                    Database().update_lessons(message)
                    
                    self.format_message(messages=formatted_messages, formatting_variables=formatted_variables, user=active_user)
                
                #? Сценарий #w: отчёт нельзя заполнить, лимит
                else:
                    formatted_messages=[messages["done_forbidden"]]
                    formatted_variables=["user.real_name"]
                    
                    self.format_message(messages=formatted_messages, formatting_variables=formatted_variables, user=active_user)
                                    
                
            case "update_version":
                MongoDB().send_new_version_update(version_number=data_from_state["version_number"], changelog=data_from_state["version_changelog"])
            
            case "get_latest_versions_info":
                latest_versions = MongoDB().get_latest_versions_info(versions_limit=3)
                print("🐍 latest_versions: ", latest_versions)
                
                prepared_version_messages = self.prepare_version_messages(mongoDB_objects=latest_versions)
                print("🐍 prepared_version_messages: ", prepared_version_messages)
                
                self.send_multiple_messages(chat_id=message.chat.id, messages=prepared_version_messages)

                    
    def save_data_in_state(self, 
                            variable_name: str, 
                            data_to_save = None, 
                            state: StateContext = None, 
                        ):
        match variable_name:
            case "version_number":
                state.add_data(version_number=data_to_save)
            
            case "version_changelog":
                state.add_data(version_changelog=data_to_save)
                
        
    def get_state_data(self, requested_data: str = None, state: StateContext = None):
        match requested_data:
            case "new_version":
                with state.data() as data:
                    version_number = data.get("version_number")
                    version_changelog = data.get("version_changelog")
                    
                    return {
                        "version_number": version_number,
                        "version_changelog": version_changelog,
                    }

    def prepare_version_messages(self, mongoDB_objects: list[dict]) -> list[dict]:
        prepared_version_messages = [] 
        
        for object in mongoDB_objects:
            version_message = f"*v{ object["version"] }* ({ object["date"] })\n\n{ object["changelog"] }"
            # print("🐍 new formatted object: ", version_message)
            
            prepared_version_messages.append(version_message)
        
        return prepared_version_messages

    
    #* MESSAGE TYPES
    # helpers (type of step)
    def inline_buttons_step(self):
        pass
    
    # helpers (type of step)
    def text_input_step(self):
        pass
    
    
    
    