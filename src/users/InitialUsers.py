from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger
from src.users.users_list import INITIAL_USERS


class InitialUsers:
    def __init__(self):
        self.logger = Logger()
        
        self.user_ids: list = Dotenv().user_ids
        self.initial_users: list = INITIAL_USERS
        
        self.admin_ids = []
        
        self.initial_admins = 1
        
        self.pin_ids_to_users()
    
    
    def pin_ids_to_users(self) -> None:
        for user_id, user in zip(self.user_ids, self.initial_users):
            user["user_id"] = user_id
            user["chat_id"] = user_id
            
        self.logger.info(f"ids for users pinned ☑")
        
        
    def get_admin_ids(self):
        if len(self.initial_users) > 0:
            for admin in self.initial_users[0:self.initial_admins]:
                self.admin_ids.append(admin["user_id"])
                
                self.logger.info(f"admin in cache: {admin}")
                self.logger.info(f"admin ids: {self.admin_ids}")
            return self.admin_ids
        else: 
            self.logger.info(f"❌ no admins found! ")
            
            
    def get_user(self, user_id) -> dict:
         for user in self.initial_users:
            if user_id == user["user_id"]:
                return user
            
            
    def get_initial_users(self) -> list:
        self.logger.info(f"self.initial_users: { self.initial_users }")
        return self.initial_users