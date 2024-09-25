from pymongo import MongoClient
from pymongo.collection import Collection
from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv


class MongoDB:
    def __init__(self, user_id) -> None:
        self.logger = Logger()
        
        MONGO_URI = Dotenv().mongodb_string
        DATABASE_NAME = "school-bot"
        
        # database
        self.client = MongoClient(MONGO_URI)
        self.database = self.client[DATABASE_NAME]
        self.logger.info(f"База данных {DATABASE_NAME} подключена!")

        # user_info
        self.user_id = user_id
        
        # collections
        self.users_collection = self.database['users']
        self.stats = self.database['stats']


    def show_users(self) -> None:        
        self.logger.info(f"Коллекция юзеров: {self.users_collection}")
        
        
    def check_if_user_exists(self): 
        """ returns True if user is in the collection, False - if not """
        user = self.users_collection.find_one({ "id" : self.user_id })
        
        if user: 
            self.logger.info(f"Чувачок (чувиха) с id {self.user_id} уже зарегистрирован(а) в БД")
            return True
        else: 
            self.logger.info(f"Новенький юзер с id {self.user_id}! Сохраняю в базу данных... 😋")
            return False
        
        
    def save_user(self, new_user) -> None:
        self.users_collection.insert_one(new_user)
        
        self.logger.info(f"Пользователь {new_user["first_name"]} с id {new_user["id"]} сохранён в Монго! 🎯")
        
        
    def save_real_name(self, real_name: str):
        filter_by_id = {'id' : self.user_id}
        update_operation = { '$set': { 'real_name' : real_name } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    def update_user(self, key, new_value):
        filter_by_id = {'id' : self.user_id}
        update_operation = { '$set': { key : new_value } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
    def get_real_name(self, id) -> str:
        filter_by_id = {'id' : self.user_id}
        user = self.users_collection.find_one(filter=filter_by_id)
        
        return user["real_name"]
    
    
    def get_payment_data(self) -> int:
        filter_by_id = {'id' : self.user_id}
        user = self.users_collection.find_one(filter=filter_by_id)
        
        self.logger.info(f"payment amount: {user["payment_amount"]}")
        
        return user["payment_amount"]
        
        
    def clean_users(self):
        self.users_collection.delete_many({})
        self.logger.info(f"База данных пользователей очищена! 🧹")


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
