from datetime import datetime

# from telebot import TeleBot
from telebot.types import Message


from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger

# from src.languages.Language import Language
from src.database.MongoDB import MongoDB
# from src.users.list.students import STUDENT_LIST
# USERS
# save admin
# save students
# handle guest and others (not explicitly)

class Users_: # 2
    """ #? Скорее всего, эту логику нужно поместить в MongoDB """
    
    
    def save_admin(self):
        pass
    def save_students(self):
        pass

        

class Students:
    def __init__(self):
        self.student_ids = Dotenv().student_ids
        
        self.link_id_to_students()
        
        
    def link_id_to_students(self):
        for id, student in zip(self.student_ids, STUDENT_LIST):
            self.logger.info(f"id {id} belongs to student: {student}")
            
            student["user_id"] = id
            
        
    def create_new_student(self):
        pass
            
    
            


class Users:
    """ manage all users in DB"""
    def __init__(self, message: Message = None):
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
            
            
            if self.find_user_in_cache() is None and message:
                self.is_saved_once = False
                self.active_user = self.save_new_user(message=message)
                self.cached_users = self.cache_users()

        # if user isn't in cache
        if self.active_user is None and message:
            self.is_saved_once = False
            self.active_user = self.save_new_user(message=message)
            self.cached_users = self.cache_users()
        
    
    def get_active_user(self) -> dict:
        """ returns active user dict {}"""
        self.logger.info(f"Users.active user: {self.active_user}")
        return self.active_user
            
    
    def cache_users(self):
        cached_users = self.mongoDB.get_all_users()
        # self.logger.info(f"users saved in cache: {cached_users}")
        
        return cached_users
        
        
    def find_user_in_cache(self):
        # self.logger.info(f"Users.find_user_in_cache")
        
        for user in self.cached_users:
            # self.logger.info(f"user: {user}, {self.user_id}, {user["user_id"]}")
            
            if user["user_id"] == self.user_id:
                self.logger.info(f"user exists in cache: {user}")
                return user

        # else... (if user isn't found in cache)
        self.logger.info(f"user isn't in cache!")
        return None
            
        
    def save_new_user(self, message: Message):
        self.logger.info(f"saving new user... (Users.save_new_user)")
        
        new_user = NewUser(message).new_user
        self.logger.info(f"новый юзер (Users.get_user): {new_user}")

        
        self.is_saved_once = True
        self.cached_users = self.cache_users()
        
        return new_user #* В идеале NewUser должен срабатывать только здесь, только один раз
        

    def get_lessons_left_from_cache(self):
        # self.logger.info(f"self.active_user (Users.get_lessons_left_from_cache): { self.active_user }")
        
        if self.active_user["done_lessons"] < self.active_user["max_lessons"]:
            self.active_user["done_lessons"] += 1
        
        if self.active_user["lessons_left"] > 0:
            self.active_user["lessons_left"] -= 1

        # self.logger.info(f"self.active_user (Users.get_lessons_left_from_cache): { self.active_user }")
        
        return [self.active_user["lessons_left"], self.active_user["done_lessons"]]


class NewUser:
    """ stores info from /start message and collects data throughout the conversation """
    
    def __init__(self, message: Message):
        self.logger = Logger()        
        
        self.dotenv = Dotenv()
        self.admin_id = self.dotenv.admin_ids
        self.student_ids = self.dotenv.student_ids

        self.user_id = message.from_user.id
        self.new_user = {}
        
        self.create_new_user(message)
        

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
            self.new_user["max_lessons"] = is_student["max_lessons"]
            
            self.new_user["done_lessons"] = 0
            self.new_user["payment_status"] = False
        
        
        # сохраняем пользователя
        self.saveUserToDB()
        
    
        
    def saveUserToDB(self):        
        self.logger.info(f"🐍 new_user (Mongo.saveUserToDB): {self.new_user}")
        
        mongoDB = MongoDB(self.user_id)
        is_user_exits = mongoDB.check_if_user_exists()
        
        if not is_user_exits:
            MongoDB().save_user_to_db(self.new_user)


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
        # код начинает ломаться на этом этапе...
        # ведь у студентов нет user_id
        for student in STUDENT_LIST:
            if self.user_id == student["user_id"]:
                return student

        # if no student found...
        return None
    
    


