from src.utils.Logger import Logger

from src.users.NewUser import NewGuest, NewAdmin, NewStudent, NewUser

from src.database.Cache import Cache
from src.users.InitialUsers import InitialUsers
from src.database.MongoDB import MongoDB

class Database:
    """ Higher-level class for syncing Cache (users) and MongoDB """
    
    def __init__(self):
        self.logger = Logger()
        
        self.mongoDB: MongoDB = MongoDB()
        
        self.initial_users = InitialUsers().get_initial_users()
        self.cache = Cache()
        # self.cached_users = Cache().get_cached_users()
        self.admin_ids = Cache().get_admin_ids()
    
        
    
    def get_user(self, user_id, message=None):
        active_user = self.cached_users.find_user(user_id)
        
        if not active_user and message:
            self.mongoDB.save_guest_to_db(message)
            
         
    def sync_cache_and_remote_users(self):
        """ Sync users across sources: 
            1) initial users with mongoDB
            2) mongoDB with cache 
            3) make local backup if MongoDB data isn't available  
        """
        
        self.update_remote_users()
        self.update_cached_users()
    
            
    def update_remote_users(self):
        # save initial users to database
        for initial_user in self.initial_users:
            filter_by_id = { "user_id": initial_user["user_id"] }
            is_user_exists_in_db = self.mongoDB.users_collection.find_one(filter=filter_by_id)
            
            if not is_user_exists_in_db:
                self.logger.info(f"❌ user doesn't exist, here's id: { initial_user["user_id"] }")

                new_user = NewUser().create_new_user(initial_user)
                self.mongoDB.save_user_to_db(new_user)

            else:
                self.logger.info(f"✔ user exist: { initial_user["real_name"]}")



    def update_cached_users(self):
        mongo_users = self.mongoDB.get_all_users()
        self.logger.info(f"mongo_users len: { len(mongo_users) }")
        self.logger.info(f"initial_users len: { len(self.initial_users) }")

        # if no MongoDB or Mongo and initials users are the same
        if len(mongo_users) == len(self.initial_users) or not len(mongo_users) or len(mongo_users) == 0:
            self.cache_initial_users()
        
        # when mongoDB has additional users
        else:
            self.cache_mongo_users()
            
        
            
    def cache_initial_users(self):
        for initial_user in self.initial_users:
            new_user = NewUser().create_new_user(initial_user)
            self.cache.cache_user(new_user)
            # self.cached_users.append(new_user)

        self.logger.info(f"🔀 saved initial users to cache: { self.cache.cached_users }")


    def cache_mongo_users(self):
        mongo_users = self.mongoDB.get_all_users()
        
        for mongo_user in mongo_users:
            self.cache.cache_user(mongo_user)
            # self.cached_users.append(mongo_user)
            
        self.logger.info(f"🏡 cache filled with MongoDB: { self.cache.cached_users }")
            
            
    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        self.mongoDB.update_user_in_db(user_id=user_id, key=key, new_value=new_value)
        
        self.cached_users.update_user(user_id=user_id, key=key, new_value=new_value)
            
    
    # def get_cached_users(self):
        # return self.cached_users


    # def get_admin_ids(self):
    #     return self.admin_ids

            
    def clean_users(self):
        self.mongoDB.clean_users()
        self.cache.clean_users()