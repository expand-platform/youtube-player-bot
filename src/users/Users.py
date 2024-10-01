from datetime import datetime

from telebot import TeleBot
from telebot.types import Message


from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

from src.languages.Language import Language
from src.database.MongoDB import MongoDB

from src.users.students import STUDENTS


#! Давай реализуем кеширование пользователей:
    #! 1. Изначально мы загружаем всех пользователей из базы данных (у нас их не так уж и много, они не меняются)
    #! 2. Далее мы первым делом делаем поиск по пользователям (по id)
    #! 3. Если пользователя нет в массиве users, мы сохраняем его в БД и заново вытягиваем юзеров, дабы закешировать изменённые данные 


# Проводит проверку на старте (фильтры) + когда нажата команда (итого - 2 проверки как минимум)


class Users:
    """ manage all users in DB"""
    def __init__(self, message: Message = None, bot: TeleBot = None):
        self.logger = Logger()
        self.mongoDB: MongoDB = MongoDB()
        
        self.cached_users = self.cache_users()
        
        self.user_id = message.from_user.id
            
        self.logger.info(f"self.user_id: {self.user_id}")
        

        self.active_user = None
        
        
        
        # if user is in cache
        self.logger.info(f"len: {len(self.cached_users)}")
        if len(self.cached_users) > 0:
            self.active_user = self.find_user_in_cache()
            
            
            if self.find_user_in_cache() is None and message and bot:
                self.is_saved_once = False
                self.active_user = self.save_new_user(message=message, bot=bot)
                self.cached_users = self.cache_users()

        # if user isn't in cache
        if self.active_user is None and message and bot:
            self.is_saved_once = False
            self.active_user = self.save_new_user(message=message, bot=bot)
            self.cached_users = self.cache_users()
        
    
    def get_active_user(self) -> dict:
        """ returns active user dict {}"""
        self.logger.info(f"Users.active user: {self.active_user}")
        return self.active_user
            
    
    def cache_users(self):
        cached_users = self.mongoDB.get_all_users()
        self.logger.info(f"users saved in cache: {cached_users}")
        
        return cached_users
        
        
    def find_user_in_cache(self):
        self.logger.info(f"Users.find_user_in_cache")
        
        for user in self.cached_users:
            self.logger.info(f"user: {user}, {self.user_id}, {user["user_id"]}")
            
            if user["user_id"] == self.user_id:
                self.logger.info(f"user exists in cache: {user}")
                return user
            
        # else... (if user isn't found in cache)
        self.logger.info(f"user isn't in cache!")
        return None
            
        
    def save_new_user(self, message: Message, bot: TeleBot):
        self.logger.info(f"saving new user... (Users.save_new_user)")
        
        # bot.send_message(chat_id=self.user_id, text=Language().messages["create_account"])
        
        new_user = NewUser(message).new_user
        self.logger.info(f"новый юзер (Users.get_user): {new_user}")

        
        self.is_saved_once = True
        self.cached_users = self.cache_users()
        
        return new_user #* В идеале NewUser должен срабатывать только здесь, только один раз
        



class NewUser:
    """ stores info from /start message and collects data throughout the conversation """
    
    def __init__(self, message: Message):
        self.logger = Logger()        
        
        self.dotenv = Dotenv()
        self.admin_id = self.dotenv.admin_id
        self.student_ids = self.dotenv.student_ids

        self.user_id = message.from_user.id
        self.new_user = {}
        
        self.create_new_user(message)
        
        
    #? Функционал будет похожий, только функция будет строго перебирать студентов, принимать каждого user_id и генерировать данные на основе тех, что уже есть (без username, first_name, зато с last_name, payment_amount, payment_status)
     
    #? Эта компашка будет собираться в массив и балком грузиться в базу данных (insert_many)
     
    #? Функции self.set_real_name() и self.set_access_level() не нужны - я и так знаю их уровни  

    def create_new_user(self, message: Message):
        self.logger.info("Регистрируем этого парня (девушку) в базе данных... 💂‍♂️")
        self.access_level = self.set_access_level()
        self.real_name = self.set_real_name()
        
        self.new_user = {
            "real_name": self.real_name,
            "last_name": "",
            
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,

            "access_level": self.access_level,
            
            "first_name":  message.chat.first_name.encode().decode('utf-8'),
            "username": message.chat.username,
            
            "language": "ru", 

            "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            
            "stats": {},       
        }
        
        is_student = self.recognize_student()
        
        if is_student:
            self.new_user["payment_amount"] = is_student["payment_amount"]
            self.new_user["payment_status"] = False
        
        
        # сохраняем пользователя
        self.saveUserToDB()
        
        
        
    def saveUserToDB(self):        
        self.logger.info(f"🐍 new_user (Mongo.saveUserToDB): {self.new_user}")
        
        mongoDB = MongoDB(self.user_id)
        is_user_exits = mongoDB.check_if_user_exists()
        
        if not is_user_exits:
            MongoDB().save_user(self.new_user)


    def set_access_level(self):
        if self.user_id == self.admin_id:            
            self.logger.info("О, Дамир here... 🌟")
            return "admin"

        elif self.user_id in self.student_ids:
            self.logger.info("О, это наш студент... 👋")
            return "student"

        else: return "guest"
        
        
    def set_real_name(self):
        if self.user_id == self.admin_id: 
            return "Дамир"
        
        elif self.user_id in self.student_ids:
            student = self.recognize_student()
            return student["real_name"]
        
        
    def recognize_student(self):
        for student in STUDENTS:
            if self.user_id == student["user_id"]:
                return student

        # if no student found...
        return None
    
    


