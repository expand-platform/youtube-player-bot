from telebot.types import Message
from datetime import datetime

from src.utils.Dotenv import Dotenv

from src.users.types import GuestT, AdminT, StudentT

#? Думаю, здесь можно создать один класс, правда в нём будет много проверок...

class NewGuest:
    """ base class for adding new users to DB """
    def __init__(self, message: Message):
        self.message = message
        self.user_id = message.chat.id
    

    def create_new_guest(self):
        new_guest: GuestT = {
            "first_name":  self.message.chat.first_name.encode().decode('utf-8'),
            "username": self.message.chat.username,
            
            "user_id": self.message.from_user.id,
            "chat_id": self.message.chat.id,

            "access_level": "guest",

            "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
        return new_guest
        
        

class NewAdmin():
    def __init__(self, user_id: int, admin_data):
        self.user_id = user_id
        
        self.real_name = admin_data["real_name"]
        self.user_name = admin_data["username"]
        
        
    def create_new_admin(self):
        new_admin: AdminT = {
            "real_name": self.real_name,
            "username": self.user_name,
            
            "user_id": self.user_id,
            "chat_id": self.user_id,
            
            "access_level": "admin",
            
            "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        }
        return new_admin

class NewStudent():
    def __init__(self, user_id: int, student_data: object):
        self.user_id = user_id
        self.student_data = student_data
        
        self.real_name = student_data["real_name"]
        self.last_name = student_data["last_name"]
        self.payment_amount = student_data["payment_amount"]
        self.max_lessons = student_data["max_lessons"]

            
        
    def create_new_student(self):
        new_student: StudentT = {
            "real_name": self.real_name,
            "last_name": self.last_name,
            
            "user_id": self.user_id,
            "chat_id": self.user_id,
            
            "access_level": "student",
            
            "payment_amount": self.payment_amount,
            "payment_status": False,
            
            "max_lessons": self.max_lessons,
            "done_lessons": 0,
            "lessons_left": self.max_lessons,

            "joined_at": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            
            "stats": {},
        }
        return new_student
        

