from pymongo import MongoClient
from pymongo.collection import Collection
from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv


class MongoDB:
    def __init__(self, user_id) -> None:
        self.logger = Logger()
        
        MONGO_URI = Dotenv().mongodb_string
        DATABASE_NAME = "telegram"
        
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
            self.logger.info(f"Этот чувачок уже зарегистрирован в БД")
            return True
        else: 
            self.logger.info(f"Новенький юзер! Сейчас добавим")
            return False
        
        
    def save_user(self, new_user) -> None:
        self.users_collection.insert_one(new_user)
        
        self.logger.info(f"Пользователь {new_user["first_name"]} с id {new_user["id"]} сохранён в Монго! 🎯")
        
        
    def save_real_name(self, real_name):
        filter_by_id = {'id' : self.user_id}
        update_operation = { '$set': { 'real_name' : real_name } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    def update_user_info(self, key, new_value):
        filter_by_id = {'id' : self.user_id}
        update_operation = { '$set': { key : new_value } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        