from datetime import datetime
from telebot.types import Message

from pymongo import MongoClient
from pymongo.collection import Collection

from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv

from src.users.NewUser import NewGuest, NewAdmin, NewStudent, NewUser

# from src.database.users.InitialUsers import InitialUsers



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

        
    def show_users(self):        
        self.logger.info(f"Коллекция юзеров: {list(self.users_collection.find({}))}")
    
    
    def get_all_users(self):        
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
        
        
    def save_user_to_db(self, new_user) -> None:
        self.users_collection.insert_one(new_user)
        
        user_name = new_user["real_name"] or new_user["first_name"] 
        self.logger.info(f"{ user_name } сохранён в БД ⏳ ")
        

        
    def update_user_in_db(self, user_id: int, key: str, new_value: str | int | bool):
        filter_by_id = { 'user_id' : user_id }
        update_operation = { '$set': { key : new_value } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    
    # def get_real_name(self, id) -> str:
    #     filter_by_id = {'user_id' : self.user_id}
    #     user = self.users_collection.find_one(filter=filter_by_id)
        
    #     return user["real_name"]
    
    # def get_user_info(self):
    #     pass
    
    
    def get_payment_data(self) -> int:
        filter_by_id = {'user_id' : self.user_id}
        user = self.users_collection.find_one(filter=filter_by_id)
        
        self.logger.info(f"payment amount: {user["payment_amount"]}")
        
        return user["payment_amount"]
        
        
    def clean_users(self):
        self.users_collection.delete_many({})
        self.logger.info(f"Коллекция пользователей MongoDB очищена! 🧹")
        

    def save_users(self, users: list):
        self.users_collection.insert_many(users)
        self.logger.info(f"Пользователи сохранены в БД!")
        
   
        
    
    def save_students(self):
        self.logger.info("Записываю студентов в базу данных... 👩‍🎓")
        
        all_students = []
        
        for student in STUDENT_LIST:
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
                
                "max_lessons": student["max_lessons"],
                "done_lessons": 0,
                "lessons_left": student["max_lessons"],

                "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                
                "stats": {}, 
            }
            
            all_students.append(new_student)
        
        self.logger.info(f"all students: {all_students}")
            
        
        # сохраняем студентов балком
        self.save_users(all_students)
     



