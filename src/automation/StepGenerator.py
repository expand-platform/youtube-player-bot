from typing import Any
from telebot.types import Message

from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS

from src.bot.Bot import Bot
from database.Cache import Cache
from src.users.NewUser import NewGuest
from src.database.MongoDB import MongoDB

from src.languages.Language import Language



class StepGenerator:
    def __init__(self, bot: Bot):
        self.logger = Logger()
        
        self.environment = Dotenv().environment
        self.bot = bot.bot_instance
        
        self.send_multiple_messages = bot.send_multiple_messages
        self.send_message_with_variable = bot.send_message_with_variable
        self.tell_admin = bot.tell_admin
    

    #* generate other /slash commands 
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
            active_user = Cache().get_user(message.from_user.id)
            
            #? Чтобы избежать таких постоянных проверок, можно 
            #? сделать класс Mongo - супер классом
            #? В ней будет раздел кешированых юзеров и возможность ими манипулировать
            
            #? Вот эту логику перенести в базу данных
            if not active_user:
                active_user = NewGuest(message).create_new_guest()
                MongoDB().save_user_to_db(active_user)
                Cache().cache_user(active_user)
            
            
            # user = Users(message=message)
            user = user.get_active_user()
            self.logger.info(f"Текущий пользователь (/start): { user }")
            
            #? Я забыл тут обновить данные тут, надо добавить вытяжки из кеша
            #? И каким-то образом достать здесь данные
            
            # run custom functions
            # if custom_command_position == 1 and custom_function_name:
                # self.run_custom_functions(method_name="update_lessons")
                
            
            if set_slash_command:
                self.set_slash_commands(user)
            
            
            if format_message:
                self.send_formatted_message(message_to_format=format_message, formatting_variable=format_variable, user=user)
                
            # multiple formatting messages
            if messages_for_formatting and variables_for_formatting:
                self.send_multiple_formatted_messages(messages=messages_for_formatting, formatting_variables=variables_for_formatting, user=user)
                
                
            if multiple_messages:
                self.send_multiple_messages(chat_id=user["user_id"], messages=multiple_messages)
                
                
            if message_text:
                self.bot.send_message(chat_id=user["user_id"], text=message_text, parse_mode="Markdown")
                
            if mongodb_activation_position == "after_messages" and mongodb_method_name:
                self.choose_mongo_method(method_name=mongodb_method_name, message=message)
            
            self.notify_admin(user, command_name)
    
    
    
    #? ADMIN COMMANDS 
    def set_admin_command(self, 
                        command_name: str = None,
                        message_suffix: str = "_success", 
                        # нужно называть сообщения в стиле "fill_success, clean_success" 
                        ):
        @self.bot.message_handler(commands=[command_name], access_level=["admin"])
        def set_admin_command(message: Message):
            self.choose_mongo_method(method_name=command_name, message=message)
            
            messages = Language().messages
            self.tell_admin(message=messages[command_name + message_suffix])
            
            
    
    #* HELPERS
    def notify_admin(self, user, command_name):
        self.tell_admin(f"{ user["real_name"] } { user["last_name"] } { user["first_name"] } @{ user["username"] } зашёл в раздел /{command_name} ✅")
        self.logger.info(f"{ user["first_name"] } зашёл в раздел /{command_name} ✅")
    
    
    def set_slash_commands(self, user):
        if user["access_level"] == "guest":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)
        
        # if "student" or "admin"
        else:
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
            
        
        self.logger.info('slash commands set: /')
    
    
    
    def get_format_variable(self, variable_name: Any, user: Users):
        match variable_name:
            case "user.real_name":
                return user["real_name"]
            
            case "user.first_name":
                return user["first_name"]
            
            case "user.payment_amount":
                return user["payment_amount"]
            
            case "user.lessons_left":
                return user["lessons_left"]
                
            case "user.done":
                if user["lessons_left"] > 0:
                    return user["lessons_left"] - 1
                
                else: return 0  # when zero lessons left
            
    
    def send_formatted_message(self, message_to_format, formatting_variable, user):
        data_for_formatting = self.get_format_variable(formatting_variable, user)
                
        self.send_message_with_variable(chat_id=user["user_id"], message=message_to_format, format_variable=data_for_formatting)


    def send_multiple_formatted_messages(self, messages, formatting_variables, user):
        #* Для каждой переменной вызывать функцию get_format_variable, результаты сохранять в массив
        #* Затем вызывать функцию send_formatted_message столько раз, сколько элементов в массиве
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
        
    
    def choose_mongo_method(self, method_name: str, message: Message):
        match method_name:
            case "clean":
                MongoDB().clean_users()
                Users(message)
            
            case "fill":
                MongoDB().save_students()
                Users(message)
                
            case "update_lessons":
                #* Процесс состоит из 3 этапов:
                    #* Сначала поработать с кешем (+1 к done_lessons, но не больше, чем max_lessons)
                    #* А затем отправить изменения в БД 
                    #* И затем закешировать новые данные из БД локально 
                
                self.logger.info(f"updating_lessons...")
                
                [lessons_left, done_lessons] = Users(message).get_lessons_left_from_cache()
                self.logger.info(f"lessons_left: { lessons_left }")
                self.logger.info(f"done_lessons: { done_lessons }")
                
                MongoDB(message.from_user.id).update_user_in_db(key="lessons_left", new_value=lessons_left)
                MongoDB(message.from_user.id).update_user_in_db(key="done_lessons", new_value=done_lessons)
                
                self.logger.info(f"mongoDB updated with new lessons! ✅")
                
                Users(message)
                
                self.logger.info(f"Cached users updated! ✅")
                

    def run_custom_functions(self, method_name: str, message: Message, user):
        match method_name:
            case "update_lessons":
                #* Процесс состоит из 3 этапов:
                    #* Сначала поработать с кешем (+1 к done_lessons, но не больше, чем max_lessons)
                    #* А затем отправить изменения в БД 
                    #* И затем закешировать новые данные из БД локально 
                
                [lessons_left, done_lessons] = Users(message).get_lessons_left_from_cache()
                
                MongoDB(message.from_user.id).update_user_in_db(key="lessons_left", new_value=lessons_left)
                MongoDB(message.from_user.id).update_user_in_db(key="done_lessons", new_value=done_lessons)
                
                Users(message)


    
    #* MESSAGE TYPES
    # helpers (type of step)
    def inline_buttons_step(self):
        pass
    
    # helpers (type of step)
    def text_input_step(self):
        pass
    
    
    
    