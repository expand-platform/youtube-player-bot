import os
from dotenv import load_dotenv


class Dotenv():
    def __init__(self):
        load_dotenv()
        
        self.ads_bot_token = ''
        self.notificator_bot_token = ''
        
        
        self.admin_id = 0
        self.mongodb_string = ''
        
        self.collect_env_data()
        
    def collect_env_data(self):
        self.ads_bot_token = os.getenv('ADS_BOT_TOKEN')
        self.notificator_bot_token = os.getenv('NOTIFICATOR_BOT_TOKEN')
        self.admin_id = int(os.getenv('ADMIN_ID'))
        
        self.mongodb_string = os.getenv('MONGODB_STRING')
        
        
        
        

