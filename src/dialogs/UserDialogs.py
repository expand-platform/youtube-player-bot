from src.utils.Logger import Logger
from src.languages.Language import Language

from src.automation.StepGenerator import StepGenerator
from src.bot.Bot import Bot


class UserDialogs:
    def __init__(self):
        self.log = Logger().info
        
        self.bot = Bot()
        
        self.step_generator = StepGenerator()
        self.messages = Language().messages
        
        
    def set_user_dialogs(self):
        #* Guests
        #? /start
        self.step_generator.set_command(
            command_name="start",
            access_level=["guest"],
            
            set_slash_command=True,
            
            formatted_messages=[self.messages["guest_welcome"]],
            formatted_variables=["user.real_name"],
        )
        
        
        #* Students 
        #? /start 
        self.step_generator.set_command(
            command_name="start",
            access_level=["student", "admin"], 
            
            set_slash_command=True,
            
            bot_after_message=self.messages["start"],

            formatted_messages=[self.messages["welcome_greeting"]],
            formatted_variables=["user.real_name"],
        )
        
        #? /schedule 
        self.step_generator.set_command(
            command_name="schedule",
            access_level=["student", "admin"], 
            
            bot_before_multiple_messages=self.messages["schedule"],
        )
        
        #? /zoom
        self.step_generator.set_command(
            command_name="zoom",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["zoom"]
        )
       
        #? /plan
        self.step_generator.set_command(
            command_name="plan",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["plan"]
        )
        
        #? /payment 
        self.step_generator.set_command(
            command_name="payment",
            access_level=["student"], 
            
            formatted_messages=[self.messages["payment_amount"]],
            formatted_variables=["user.payment_amount"],

            bot_after_multiple_messages=self.messages["payment_details"]
        )
        
        #? /lessons
        self.step_generator.set_command(
            command_name="lessons",
            access_level=["student"], 
            
            formatted_messages=[self.messages["lessons_left"]],
            formatted_variables=["user.lessons_left"],
        )
        
        #? /done
        self.step_generator.set_command(
            command_name="done",
            access_level=["student"], 
            
            mongodb_method_name="update_lessons",
            mongodb_activation_position="after_messages",
        )
        
        #? /version
        self.step_generator.set_command(
            command_name="version",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["version_intro"],
            
            mongodb_activation_position="after_messages",
            mongodb_method_name="get_latest_versions_info",
        )
        
        self.log(f"Команды и диалоги пользователей включены 🎬")
        
        #? делаем /new_month
        
        