from datetime import datetime, timedelta

from telebot.types import Message
from src.utils.Logger import Logger

from src.users.NewUser import NewGuest, NewUser

from src.database.Cache import Cache
from src.users.InitialUsers import InitialUsers
from src.database.MongoDB import MongoDB

class Database:
    """ Higher-level class for syncing Cache (users) and MongoDB """
    
    
    _db_instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._db_instance is None:
            cls._db_instance = super(Database, cls).__new__(cls)
            
            # pin user ids once
            InitialUsers().pin_ids_to_users()
            
            cls._db_instance.initial_users = InitialUsers().get_initial_users()
            cls._db_instance.cache = Cache()
            cls._db_instance.admin_ids = Cache().get_admin_ids()
            
        return cls._db_instance
    
    
    def __init__(self):
        self.logger = Logger()
        self.mongoDB = MongoDB()
        
    #! reduce number of times this method has been called
    #! for super fast time-to-response
    #! Now it's called 3 times: Filters, / command and maybe somewhere else (use search for set_active_user)
    def detect_active_user(self, message: Message):
        # self.logger.info(f"looking for user_id { message.from_user.id }...")
        active_user = self.cache.find_active_user(user_id=message.chat.id)
        

        if active_user:
            self.logger.info(f"👌 this user is in cache: { active_user }")

            # add some data from telegram
            self.complete_user_profile(active_user, message)
            
            return active_user
        
        if not active_user:
            # self.logger.info(f"👐 wow, it's someone new: { active_user }")
            new_guest = NewGuest(message).create_new_guest()
            
            self.mongoDB.save_user(new_guest)
            
            # cache user after it's being registered
            self.update_cached_users()
            return new_guest
            
         
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
                # self.logger.info(f"❌ user doesn't exist, here's id: { initial_user["user_id"] }")

                new_user = NewUser().create_new_user(initial_user)
                # self.complete_user_profile(new_user)
                
                self.mongoDB.save_user(new_user)
            
            # if user exists:
            # self.logger.info(f"✔ user exist: { initial_user["real_name"]}")


    def update_cached_users(self):
        mongo_users = self.mongoDB.get_all_users()
        
        # self.logger.info(f"mongo_users len: { len(mongo_users) }")
        # self.logger.info(f"initial_users len: { len(self.initial_users) }")

        # no Mongo backup
        if not len(mongo_users) or len(mongo_users) == 0:
            self.cache_initial_users()
        
        # fetch users by default (once)
        else:
            self.cache_mongo_users()
            
        
            
    def cache_initial_users(self):
        for initial_user in self.initial_users:
            new_user = NewUser().create_new_user(initial_user)
            self.cache.cache_user(new_user)
            # self.cached_users.append(new_user)

        # self.logger.info(f"🔀 saved initial users to cache: { self.cache.cached_users }")


    def cache_mongo_users(self):
        mongo_users = self.mongoDB.get_all_users()
        
        for mongo_user in mongo_users:
            self.cache.cache_user(mongo_user)
            # self.cached_users.append(mongo_user)
            
        # self.logger.info(f"🏡 cache filled with MongoDB: { self.cache.cached_users }")
            
            
            
    def clean_users(self):
        self.mongoDB.clean_users()
        self.cache.clean_users()
        
        
    #? active user methods
    def complete_user_profile(self, active_user: dict, message: Message):
        # add first_name
        if not active_user.get("first_name"):
            self.update_user(user=active_user, key="first_name", new_value=message.from_user.first_name)
            # self.logger.info(f"first_name updated: { message.from_user.first_name }")
            
        
        # add username
        if not active_user.get("username"):
            username = message.from_user.username 
            
            if username == None or username == "None":
                self.update_user(user=active_user, key="username", new_value="not set")
            else:
                self.update_user(user=active_user, key="username", new_value=username)
                
            # self.logger.info(f"username updated: { message.from_user.username }")
        
        
    
    def get_real_name(self, active_user: dict):
        real_name = ""
        last_name = ""
        
        if active_user["access_level"] == "student" or active_user["access_level"] == "admin":
            real_name = active_user.get("real_name") 
            last_name = active_user.get("last_name")
        
        if active_user["access_level"] == "guest":
            real_name = active_user.get("first_name") 
        
        return real_name, last_name
    
    
    
    def update_user(self, user: dict, key: str, new_value: str | int | bool):
        self.mongoDB.update_user(user_id=user["user_id"], key=key, new_value=new_value)
        self.cache.update_user(user_id=user["user_id"], key=key, new_value=new_value)
        
        real_name, last_name = self.get_real_name(user)
        self.logger.info(f"📅 Пользователь обновлён (update_user): { real_name } { last_name }")
        
    
    def update_lessons(self, message: Message):
        # работа с данными, затем с кешом и монго
        active_user = self.detect_active_user(message)
                
        if active_user["done_lessons"] < active_user["max_lessons"]:
            active_user["done_lessons"] += 1
        
        if active_user["lessons_left"] > 0:
            active_user["lessons_left"] -= 1
            
        self.update_user(user=active_user, key="done_lessons", new_value=active_user["done_lessons"])
        self.update_user(user=active_user, key="lessons_left", new_value=active_user["lessons_left"])
            
        return {
            "done_lessons": active_user["done_lessons"],
            "lessons_left": active_user["lessons_left"]
        }
        
         
    def check_done_reports_limit(self, max_lessons: int, done_lessons: int) -> bool:
        is_report_allowed = False
        
        limit_multiplier = 1

        if max_lessons == 8:
            limit_multiplier = 2
            
        
        #? Тут делаем проверку
        now = datetime.now()
        current_week_number = self.week_of_month(now)
        
        current_time = now.strftime(f"%d %B, %H:%M")

        print(f"Current time: {current_time}")
        print(f"Current week in month: {current_week_number}")
        
        allowed_reports_limit = current_week_number * limit_multiplier # 2 * 1 или 2 * 2
        print("🐍allowed_reports_limit: ", allowed_reports_limit)
        
        
        if done_lessons < allowed_reports_limit:
            is_report_allowed = True

        # else...        
        self.logger.info(f"is_report_allowed: { is_report_allowed }")
        return is_report_allowed
        
    
    def week_of_month(self, dt):
        first_day = dt.replace(day=1)
        dom = dt.day
        adjusted_dom = dom + first_day.weekday()  # Weekday ranges from 0 (Monday) to 6 (Sunday)
        return (adjusted_dom - 1) // 7 + 1


