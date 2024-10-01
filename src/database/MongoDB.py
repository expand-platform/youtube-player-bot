from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection

from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv

from src.users.students import STUDENTS


#! Нужно провести оптимизацию, чтобы мы каждый раз не подключались к базе данных
#! Или делали это как можно реже


class MongoDB:
    _mongoDB_instance = None
    
    # def __new__(cls, *args, **kwargs):
    #     if cls._mongoDB_instance is None:
    #         cls._mongoDB_instance = super(MongoDB, cls).__new__(cls)
    #     return cls._mongoDB_instance

    def __new__(cls, *args, **kwargs):
        DATABASE_NAME = "school-bot"
        MONGO_URI = Dotenv().mongodb_string
        
        if cls._mongoDB_instance is None:
            cls._mongoDB_instance = super().__new__(cls)
            cls._mongoDB_instance.client = MongoClient(MONGO_URI, maxPoolSize=1)
            cls._mongoDB_instance.database = cls._mongoDB_instance.client[DATABASE_NAME] 
            
            Logger().info(f"База данных {DATABASE_NAME} подключена!")
        
        return cls._mongoDB_instance


    
    def __init__(self, user_id: int = None) -> None:
        self.logger = Logger()
        
        
        self.users_collection: Collection = self.database['users']

        #? (возможно) это будет не нужно
        if user_id:
            self.user_id = user_id
        
        
    def show_users(self):        
        self.logger.info(f"Коллекция юзеров: {list(self.users_collection.find({}))}")
    
    
    def get_all_users(self):        
        self.show_users()
        return list(self.users_collection.find({}))
        
        
    def check_if_user_exists(self): 
        """ returns True if user is in the collection, False - if not """
        user = self.users_collection.find_one({ "user_id" : self.user_id })
        
        if user: 
            self.logger.info(f"Чувачок (чувиха) с id {self.user_id} уже зарегистрирован(а) в БД")
            return True
        else: 
            self.logger.info(f"Новенький юзер с id {self.user_id}! Сохраняю в базу данных... 😋")
            return False
        
        
    def save_user(self, new_user) -> None:
        self.users_collection.insert_one(new_user)
        
        self.logger.info(f"Пользователь {new_user["first_name"]} с id {new_user["user_id"]} сохранён в Монго! 🎯")
        
        
    def save_real_name(self, real_name: str):
        filter_by_id = {'user_id' : self.user_id}
        update_operation = { '$set': { 'real_name' : real_name } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    def update_user(self, key, new_value):
        filter_by_id = {'user_id' : self.user_id}
        update_operation = { '$set': { key : new_value } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    def get_real_name(self, id) -> str:
        filter_by_id = {'user_id' : self.user_id}
        user = self.users_collection.find_one(filter=filter_by_id)
        
        return user["real_name"]
    
    
    def get_payment_data(self) -> int:
        filter_by_id = {'user_id' : self.user_id}
        user = self.users_collection.find_one(filter=filter_by_id)
        
        self.logger.info(f"payment amount: {user["payment_amount"]}")
        
        return user["payment_amount"]
        
        
    def clean_users(self):
        self.users_collection.delete_many({})
        self.logger.info(f"База данных пользователей очищена! 🧹")
        

    def save_users(self, users: list):
        self.users_collection.insert_many(users)
        self.logger.info(f"Пользователи сохранены в БД!")
        
    
    def save_students(self):
        self.logger.info("Записываю студентов в базу данных... 👩‍🎓")
        
        all_students = []
        
        for student in STUDENTS:
            new_student = {
                "real_name": student["real_name"],
                "last_name": student["last_name"],
                
                "user_id": student["user_id"],
                "chat_id": student["user_id"],
                
                "access_level": "student",
                
                "first_name": "",
                "username": "",
                
                "language": "ru", 
                
                "payment_amount": student["payment_amount"],
                "payment_status": False,

                "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                
                "stats": {}, 
            }
            
            all_students.append(new_student)
        
        self.logger.info(f"all students: {all_students}")
            
        
        # сохраняем студентов балком
        self.save_users(all_students)




""" 
    Actions to save in DB:
    - registration 
    - command used 
    - leave chat (idle for 10s-15s) 
    - filled in some data
    - press a button
    - choose a menu link / (or go to specific menu option)

    Structure: 
    [
        "Дамир": [
            {
                "time": "18:09:23 28-12-2023",
                "comment": "зашёл в бота", 
                "action_type": "login", 
                "command": "/start", 
            },
            {
                "time": "18:10:01 28-12-2023",
                "comment": "нажал /start", 
                "action_type": "login", 
                "command": "/start", 
            },
            {
                "time": "18:11:20 28-12-2023",
                "comment": "вышел из бота", 
                "action_type": "logout", 
                "command": "", 
            },
        ]
    ]
"""
