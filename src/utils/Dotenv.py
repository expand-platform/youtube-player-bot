import os
from dotenv import load_dotenv


class Dotenv():
    def __init__(self):
        load_dotenv()
        
        self.bot_token = ''
        
        self.admin_id = 0
        self.student_ids = ''
        
        self.environment = ''
        self.mongodb_string = ''
        
        
        self.collect_env_data()
        
    def collect_env_data(self):
        self.bot_token = os.getenv('BOT_TOKEN')
        
        self.admin_id = int(os.getenv('ADMIN_ID'))
        self.student_ids = self.convert_to_list(os.getenv('STUDENT_IDS'))
        
        self.environment = os.getenv('ENVIRONMENT')
        self.mongodb_string = os.getenv('MONGODB_STRING')
        
        
    def convert_to_list(self, env_variable):
        list = env_variable.split(',')
        return [int(item) for item in list]
        
        
        
        
        

