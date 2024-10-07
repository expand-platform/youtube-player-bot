from datetime import datetime
from telebot.types import Message

from pymongo import MongoClient
from pymongo.collection import Collection

from src.utils.Logger import Logger
from src.utils.Dotenv import Dotenv

# from src.users.list.students import STUDENT_LIST
# from src.users.list.admins import ADMIN_LIST
from src.users.NewUser import NewGuest, NewAdmin, NewStudent

from src.users.initial.InitialUsers import InitialUsers


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


    
    def __init__(self, user_id: int = None) -> None:
        self.logger = Logger()
        self.dotenv = Dotenv()
        
        self.users_collection: Collection = self.database['users']

        if user_id:
            self.user_id = user_id
        
        
    def show_users(self):        
        self.logger.info(f"Коллекция юзеров: {list(self.users_collection.find({}))}")
    
    
    def get_all_users(self):        
        # self.show_users()
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
        

    
    # def save_student_to_db(self, student_id: int):
    #     student_object = UserHelpers().find_student(user_id=student_id)
    #     # self.logger.info(f"student: { student_object }")
        
    #     new_student = NewStudent(user_id=student_id, student_data=student_object).create_new_student()
    #     self.users_collection.insert_one(new_student)
        # self.logger.info(f"студент {student_object["real_name"]} сохранён в БД ✔")
    
    
    # def save_admin_to_db(self, admin_id: int):
    #     admin_object = UserHelpers().find_admin(user_id=admin_id)
    #     # self.logger.info(f"admin: { admin_object }")
        
    #     new_admin = NewAdmin(user_id=admin_id, admin_data=admin_object).create_new_admin()
    #     self.users_collection.insert_one(new_admin)
        # self.logger.info(f"админ {admin_object["real_name"]} сохранён в БД ✔")
        
    
        
    def save_initial_user_to_db(self, user_data) -> None:
        new_user = {}
        
        if user_data["access_level"] == "admin":
            new_user = NewAdmin(user_id=user_data["user_id"], admin_data=user_data).create_new_admin()
            
        if user_data["access_level"] == "student":
            new_user = NewStudent(user_id=user_data["user_id"], student_data=user_data).create_new_student()
        
        self.users_collection.insert_one(new_user)    
        self.logger.info(f"{user_data["real_name"]} сохранён в БД ⏳ ")
        
        

    def save_guest_to_db(self, message: Message):
        new_user = NewGuest(message=message).create_new_student()
        self.users_collection.insert_one(new_user)   
        
        # self.users_collection.insert_one(new_user)
        
        # user_real_name = new_user["real_name"] | new_user["first_name"] 
        # user_id = new_user["user_id"]
        
        # self.logger.info(f"🎯 { user_real_name } с id { user_id } сохранён в БД ")
        
        
    def save_real_name(self, real_name: str):
        filter_by_id = {'user_id' : self.user_id}
        update_operation = { '$set': { 'real_name' : real_name } }
        
        self.users_collection.update_one(filter=filter_by_id, update=update_operation)
        
        
    def update_user_data(self, key, new_value):
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
        
        
    def check_initial_users_in_db(self):
        initial_users = InitialUsers().get_initial_users()
        
        for initial_user in initial_users:
            # self.logger.info(f"student: {student}")
            filter_by_id = { "user_id": initial_user["user_id"] }
            is_user_exists_in_db = self.users_collection.find_one(filter=filter_by_id)
            
            if not is_user_exists_in_db:
                self.logger.info(f"❌ user doesn't exist, here's id: { initial_user["user_id"] }")
                
                self.save_initial_user_to_db(user_data=initial_user)
                
                # self.save_user_to_db(new_user=initial_user)
            else:
                self.logger.info(f"✔ user exist: { initial_user["real_name"]}")
        
        
    #? Admins
    # def check_admins_in_db(self):
    #     for admin_id in self.dotenv.student_ids:
    #         # self.logger.info(f"student: {student}")
    #         filter_by_id = { "user_id": admin_id }
    #         is_student_exists = self.users_collection.find_one(filter=filter_by_id)
            
    #         if not is_student_exists:
    #             self.logger.info(f"❌ admin doesn't exist, here's id: { admin_id}")
    #             self.save_admin_to_db(admin_id=admin_id)
    #         else:
    #             self.logger.info(f"✔ admin exist, here's id: { admin_id}")
        
        
    # #? Students
    
    # def check_students_in_db(self):
    #     for student_id in self.dotenv.student_ids:
    #         # self.logger.info(f"student: {student}")
    #         filter_by_id = { "user_id": student_id }
    #         is_student_exists = self.users_collection.find_one(filter=filter_by_id)
            
    #         if not is_student_exists:
    #             self.logger.info(f"❌ student doesn't exist, here's id: { student_id}")
    #             self.save_student_to_db(student_id=student_id)
    #         else:
    #             self.logger.info(f"✔ student exist, here's id: { student_id}")
                
        
        
        
    
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



