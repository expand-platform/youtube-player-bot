from datetime import datetime

from src.utils.Dotenv import Dotenv
from src.database.MongoDB import MongoDB

from src.utils.Logger import Logger

from src.users.students import STUDENTS




class User:
    """ stores info from /start message and collects data throughout the conversation """
    
    def __init__(self, message):
        self.logger = Logger()
                
        self.admin_id = Dotenv().admin_id
        self.student_ids = Dotenv().student_ids
        
        
        self.id = message.from_user.id
        self.chat_id = message.chat.id
        
        self.first_name = message.chat.first_name.encode().decode('utf-8')
        self.username = message.chat.username
        self.real_name = ""
        
        
        self.joined_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.access_level = self.check_access_level()
        
        
        self.mongoDB = MongoDB(self.id)
        self.is_in_database = self.mongoDB.check_if_user_exists()
        
        # save user to db if not registered yet
        if not self.is_in_database: 

            self.logger.info("Регистрируем этого парня (девушку) в базе данных... 💂‍♂️")
            
            self.create_new_user()
            self.set_access_level()
            
            self.saveUserToDB()
        
        else:
            self.logger.info(f"Ты уже есть в базе данных")
            self.real_name = self.mongoDB.get_real_name(self.id)


    def create_new_user(self):
        self.new_user = {
            "id": self.id,
            "chat_id": self.chat_id,
            
            "first_name": self.first_name,
            "username": self.username,
            
            "access_level": self.access_level,
            
            "language": "ru", 
            "joined_at": self.joined_at,
            
            "real_name": "",

            "stats": {},       
        }


    def set_access_level(self):
        if self.chat_id == self.admin_id:
            self.logger.info("О, Дамир... 🌟")
            self.access_level = "admin"
            
            self.new_user["real_name"] = "Дамир"
            self.real_name = "Дамир"

            
        elif self.chat_id in self.student_ids:
            self.logger.info("О, это наш студент... 👋")
            self.access_level = "student"
            
            self.recognize_student()


    def check_access_level(self):
        if self.chat_id == self.admin_id:
            return "admin"
        elif self.chat_id in self.student_ids:
            return "student"
        else: return "guest"
        
        
    def recognize_student(self):
        for student in STUDENTS:
            if self.id == student["user_id"]:
                self.real_name = student["real_name"]
                self.logger.info(f"Я узнал тебя, {self.real_name}")
                
                self.new_user["real_name"] = self.real_name
                self.new_user["payment_amount"] = student["payment_amount"]
                self.new_user["payment_status"] = student["payment_status"]
            
            else:
                self.logger.info(f"Ты не студент, {self.first_name}")
                        

    def saveUserToDB(self):        
        self.logger.info(f"🐍 new_user: {self.new_user}")
        self.mongoDB.save_user(self.new_user)
        
