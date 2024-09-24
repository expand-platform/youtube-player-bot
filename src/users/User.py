from datetime import datetime

from src.utils.Dotenv import Dotenv
from src.database.MongoDB import MongoDB

from src.utils.Logger import Logger


admin_id = Dotenv().admin_id


class User:
    """ stores info from /start message and collects data throughout the conversation """
    
    def __init__(self, message):
        self.logger = Logger()
        
        self.id = message.from_user.id
        
        self.first_name = message.chat.first_name.encode().decode('utf-8')
        self.username = message.chat.username
        self.chat_id = message.chat.id
        
        self.joined_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.user_role = "partner"
        self.referral_level = 1

        self.mongoDB = MongoDB(self.id)
        self.is_in_database = self.mongoDB.check_if_user_exists()
        
        # save user to db if not registered yet
        if not self.is_in_database: 
            self.logger.info("Регистрируем этого парня (девушку) в базе данных... 💂‍♂️")
            self.check_if_is_admin()
            self.saveUserToDB()


    def check_if_is_admin(self):
        if self.chat_id == admin_id:
            self.logger.info('Регистрирую Дамира... 🌟')
            self.user_role = 'admin'
            self.referral_level = 999


    def saveUserToDB(self):
        new_user = {
            "id": self.id,
            "chat_id": self.chat_id,
            
            "first_name": self.first_name,
            "username": self.username,
            
            "user_role": self.user_role,
            "referral_level": self.referral_level,
            
            "joined_at": self.joined_at,
            
            "language": "ukr", # default lang
            "stats": {}        # future statistics
        }
        
        self.logger.info(f"🐍 new_user: {new_user}")
        self.mongoDB.save_user(new_user)
        
    
    # def saveAction(self):
        # print('test: ')


""" 
    User actions:
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
