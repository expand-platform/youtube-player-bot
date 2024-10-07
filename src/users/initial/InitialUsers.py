from src.utils.Dotenv import Dotenv
from src.utils.Logger import Logger
from src.users.initial.users_list import INITIAL_USERS


class InitialUsers:
    def __init__(self):
        self.logger = Logger()
        
        self.user_ids: list = Dotenv().user_ids
        self.initial_users: list = INITIAL_USERS
    
    
    def pin_ids_to_users(self):
        for user_id, user in zip(self.user_ids, self.initial_users):
            # self.logger.info(f"user_id: {user_id}")
            user["user_id"] = user_id
        self.logger.info(f"ids for users pinned ☑")
        
    
            
    def get_user(self, user_id):
         for user in self.initial_users:
            # self.logger.info(f"user: {user}")
            if user_id == user["user_id"]:
                # self.logger.info(f"find student: {user}")
                return user
            
    def get_initial_users(self) -> list:
        return self.initial_users