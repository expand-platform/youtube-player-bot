from src.utils.Logger import Logger
from src.users.InitialUsers import InitialUsers


class Cache:
    _cache_instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._cache_instance is None:
            cls._cache_instance = super().__new__(cls)
            
            cls._cache_instance.cached_users = []
            cls._cache_instance.admin_ids = InitialUsers().get_admin_ids()
        
        return cls._cache_instance
    
    def __init__(self):
        self.logger = Logger()
    
            
    def cache_user(self, new_user: dict) -> None:
        self.cached_users.append(new_user)
        
        
    def get_cached_users(self) -> list:
        if len(self.cached_users) > 0:
            self.logger.info(f"🟢 users in cache: { self.cached_users }")
            return self.cached_users
        else:
            self.logger.info(f"❌ no users in cache: { self.cached_users }")
            return []
    
    
    def get_admin_ids(self) -> list:
        self.logger.info(f"admin ids: { self.admin_ids }")
        return self.admin_ids
    
    
    def find_user(self, user_id):
        for user in self.cached_users:
            if user["user_id"] == user_id:
                return user
            else:
                return None

    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        for user in self.cached_users:
            if user["user_id"] == user_id:
                user[key] = new_value
                
                user_name = user["real_name"] or user["first_name"]
                self.logger.info(f"user { user_name } updated!")
                

    def clean_users(self):
        self.cached_users = []
        self.logger.info(f"Кеш пользователей очищен! 🧹")
        
