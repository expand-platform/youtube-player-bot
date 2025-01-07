from src.utils.Logger import Logger
from src.users.InitialUsers import InitialUsers
from src.users.NewUser import NewUser


class Cache:
    _cache_instance = None
    
    users: list = None
    admin_ids: list = None
    
    def __new__(cls, *args, **kwargs):
        if cls._cache_instance is None:
            cls._cache_instance = super().__new__(cls)
            
            cls._cache_instance.users = []
            cls._cache_instance.admin_ids = InitialUsers().get_admin_ids()
        
        return cls._cache_instance
    
    def __init__(self):
        self.log = Logger().info
    
            
    def cache_user(self, new_user: dict) -> None:
        self.users.append(new_user)
        
        
    def get_users_from_cache(self) -> list:
        if len(self.users) > 0:
            # self.log(f"🟢 users in cache: { self.cached_users }")
            return self.users
        else:
            # self.log(f"❌ no users in cache: { self.cached_users }")
            return []
    
    
    def get_admin_ids(self) -> list:
        # self.log(f"admin ids: { self.admin_ids }")
        return self.admin_ids
    
    
    def find_active_user(self, user_id):
        # self.log(f"user_id (Cache.find_active_user): { user_id }")
        for user in self.users:
            # self.log(f"user: { user }")
            if user["user_id"] == user_id:
                return user
        # if user not found
        return None
    

    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        for user in self.users:
            if user["user_id"] == user_id:
                user[key] = new_value
                
                # real_name, last_name = Database().get_real_name(active_user=user)
                # self.log(f"user { user_name } updated: key: {key} and value {new_value}")
                
    def get_user(self, user_id: int) -> dict:
        for user in self.users:
            if user["user_id"] == user_id:
                return user
            
            
    def remove_user(self, user_id: int) -> None:
        for cache_user in self.users:
            if user_id == cache_user["user_id"]:
                self.users.remove(cache_user)
                print(f"User removed from cache!")
                
        
    
    def find_user_by_property(self, property_name, value):
        for user in self.users:
            if property_name in user:
                if value == user[property_name]:
                    print("🐍 user (find_user_by_property): ",user)
                    return user
                
        
                

    def clean_users(self):
        self.users = []
        self.log(f"Кеш пользователей очищен! 🧹")
        
        initial_users = InitialUsers().get_initial_users()
        admin = NewUser().create_new_user(user_info=initial_users[0])
        
        self.cache_user(admin)
