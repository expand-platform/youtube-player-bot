from datetime import datetime, timedelta

from telebot.types import Message

from pymongo import MongoClient
from pymongo.collection import Collection

from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv
from src.languages.Ru import MONTHS_RU
from src.users.InitialUsers import InitialUsers


#! Когда-нибудь руки дойдут до хеширования данных (как минимум: user_id, real_name)


class MongoDB:
    _mongoDB_instance = None
    
    def __new__(cls, *args, **kwargs):
        DATABASE_NAME = "school-bot"
        MONGO_URI = Dotenv().mongodb_string
        
        if cls._mongoDB_instance is None:
            cls._mongoDB_instance = super().__new__(cls)
            cls._mongoDB_instance.client = MongoClient(MONGO_URI, maxPoolSize=1)
            cls._mongoDB_instance.database = cls._mongoDB_instance.client[DATABASE_NAME] 
            
            Logger().info(f"База данных {DATABASE_NAME} подключена!")
        
        return cls._mongoDB_instance

    
    def __init__(self) -> None:
        self.logger = Logger()
        self.dotenv = Dotenv()
        
        self.users_collection: Collection = self.database['users']
        self.versions_collection: Collection = self.database['versions']

        
    def show_users(self):        
        self.logger.info(f"Коллекция юзеров: {list(self.users_collection.find({}))}")
        
    
    
    def get_all_users(self):        
        return list(self.users_collection.find({}))
        

    
        
    def check_if_user_exists(self): 
        """ returns True if user is in the collection, False - if not """
        user = self.users_collection.find_one({ "user_id" : self.user_id })
        
        if user: 
            # self.logger.info(f"Чувачок (чувиха) с id {self.user_id} уже зарегистрирован(а) в БД")
            return True
        else: 
            # self.logger.info(f"Новенький юзер с id {self.user_id}! Сохраняю в базу данных... 😋")
            return False
        
        
    def save_user(self, new_user: dict) -> None:
        self.users_collection.insert_one(new_user)
        # self.logger.info(f"before: { new_user }  ⏳ ")
        
        self.logger.info(f"Юзер с id { new_user["user_id"] } сохранён в БД ⏳ ")
        

        
    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        filter_by_id = { 'user_id' : user_id }
        update_operation = { '$set': { key : new_value } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
    #? Admin commands
        
    def clean_users(self):
        admin_ids = InitialUsers().admin_ids
        delete_filter = {"user_id": {"$nin": admin_ids}}
        
        self.users_collection.delete_many(filter=delete_filter)
        self.logger.info(f"Коллекция пользователей MongoDB очищена! 🧹")
        
        
    #? Versions
    def get_latest_versions_info(self, versions_limit: int = 3):
        self.versions_collection = self.database['versions']
        latest_versions = list(self.versions_collection.find({}).sort("id", -1).limit(versions_limit))
        
        latest_versions.reverse()
        print("🐍 latest_versions from mongo: ", latest_versions)

        return latest_versions    
    
    
    def send_new_version_update(self, version_number: int, changelog: str):
        now = datetime.now()
        
        if Dotenv().environment == "production":
            now = now + timedelta(hours=3) 
        
        current_time = now.strftime(f"%d {MONTHS_RU[now.month]}, %H:%M")
        
        versions_count = self.versions_collection.count_documents({})
        
        new_update = {
            "id": versions_count + 1,
            "date": current_time,
            "version": version_number,
            "changelog": changelog,
        }
        
        self.versions_collection.insert_one(new_update)

        self.logger.info(f"⌛ New version { version_number } published! ")
        
    
    #? Replication: сегодня пишем реплику БД со всей её информацией:
    #? 1) Создание реплики
    #? 2) Загрузка из реплики назад в БД
    
    
    #? Зачем? Чтобы, на всякий случай, не потерять данные пользователей
    
    
    

