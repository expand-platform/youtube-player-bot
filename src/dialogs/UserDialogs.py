from src.utils.Logger import Logger
from src.languages.Language import Language

from src.dialogs.DialogGenerator import DialogGenerator
from src.bot.Bot import Bot


class UserDialogs:
    def __init__(self):
        self.log = Logger().info
        
        self.bot = Bot()
        
        self.dialog_generator = DialogGenerator()
        self.messages = Language().messages
        
        
    def set_user_dialogs(self):
        #* Guests
        #? /start
        self.dialog_generator.set_command(
            command_name="start",
            access_level=["guest"],
            
            set_slash_command=True,
            
            formatted_messages=[self.messages["guest_welcome"]],
            formatted_variables=["user.real_name"],
        )
        
        
        #* Students 
        #? /start 
        self.dialog_generator.set_command(
            command_name="start",
            access_level=["student", "admin"], 
            
            set_slash_command=True,
            
            bot_after_message=self.messages["start"],

            formatted_messages=[self.messages["welcome_greeting"]],
            formatted_variables=["user.real_name"],
        )
        
        #? /schedule 
        self.dialog_generator.set_command(
            command_name="schedule",
            access_level=["student", "admin"], 
            
            bot_before_multiple_messages=self.messages["schedule"],
        )
        
        #? /zoom
        self.dialog_generator.set_command(
            command_name="zoom",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["zoom"]
        )
       
        #? /plan
        self.dialog_generator.set_command(
            command_name="plan",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["plan"]
        )
        
        #? /payment 
        self.dialog_generator.set_command(
            command_name="payment",
            access_level=["student"], 
            
            formatted_messages=[self.messages["payment"]["amount"], self.messages["payment"]["status"]],
            formatted_variables=["user.payment_amount", "user.payment_status"],
        )
        
        
        #? /card 
        self.dialog_generator.set_command(
            command_name="card",
            access_level=["student", "admin"], 
            
            bot_before_multiple_messages=self.messages["payment"]["details"],
        )
        
        #? /lessons
        self.dialog_generator.set_command(
            command_name="lessons",
            access_level=["student"], 
            
            formatted_messages=[self.messages["lessons_left"]],
            formatted_variables=["user.lessons_left"],
        )
        
        #? /done
        self.dialog_generator.set_command(
            command_name="done",
            access_level=["student"], 
            
            mongodb_method_name="update_lessons",
            mongodb_activation_position="after_messages",
        )
        
        #? /version
        self.dialog_generator.set_command(
            command_name="version",
            access_level=["student", "admin"], 
            
            bot_after_message=self.messages["version_intro"],
            
            mongodb_activation_position="after_messages",
            mongodb_method_name="get_latest_versions_info",
        )
        
        #! Sequences
        
        #? /hometask (step 1) -> show home task and buttons (edit / remind me)  
        self.dialog_generator.make_dialog(
            access_level=["student"],
            handler_type="command",
            command_name="hometask",
            
            handler_prefix="ht",
            buttons_callback_prefix="hometask_actions",
            
            active_state=None,
            next_state=None,
            
            formatted_messages=[self.messages["hometask"]["task"]],
            formatted_variables=["user.hometask"],
            
            keyboard_with_before_message="hometask_actions",
        )
        
        self.log(f"Команды и диалоги пользователей включены 🎬")
        
        
        