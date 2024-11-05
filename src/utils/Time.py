from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from src.utils.Logger import Logger
from src.languages.Language import Language

from src.bot.Bot import Bot
from src.database.Database import Database

from src.database.MongoDB import MongoDB


class Time:
    def __init__(self):
        self.log = Logger().info
        
        self.scheduler = BackgroundScheduler()
        
        self.bot = Bot()
        self.messages = Language().messages
        
        self.database = Database()
        
        
    def set_scheduled_tasks(self):
        self.set_weekly_tasks()
        self.set_monthly_tasks()
        
        self.scheduler.start()
        
        
        
    def set_weekly_tasks(self):
        self.scheduler.add_job(self.make_weekly_backup, CronTrigger(day_of_week='mon', hour=10, minute=0))
        self.log(f"Weekly tasks set! 🆗")
        

    def set_monthly_tasks(self):
        self.scheduler.add_job(self.make_monthly_data_refresh, 'cron', day='last', hour=10, minute=0)
        self.log(f"Monthly tasks set! 🆗")

    
    def get_current_time(self) -> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("Formatted date and time:", formatted_datetime)
        
        return formatted_datetime
        
        
    def make_monthly_data_refresh(self):
        self.bot.tell_admin(message=self.messages["monthly_data_refresh"]["intro"])
        Database().make_monthly_reset()
            
        self.log(f"Monthly reset completed 🤙")
        self.bot.tell_admin(message=self.messages["monthly_data_refresh"]["success"])
            
        
    def make_weekly_backup(self):
        MongoDB().replicate_collection(collection_name="users")
        Database().sync_cache_and_remote_users()
        
        
        
        
        