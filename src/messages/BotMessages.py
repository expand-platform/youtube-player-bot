from src.utils.Logger import Logger
from src.languages.Language import Language

from src.bot.States import VersionSequenceStates, UserUpdateSequenceStates

from src.bot.Bot import Bot
from src.automation.StepGenerator import StepGenerator


class BotMessages:
    def __init__(self, bot: Bot):
        self.logger = Logger()
        
        self.bot: Bot = bot.bot_instance
        self.tell_admin = bot.tell_admin
        
        self.step_generator = StepGenerator(bot)
        self.messages = Language().messages
        
        self.enable_slash_commands()
   
        
    def enable_slash_commands(self):
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
        
    
        #* Admin
        #? /clean
        self.step_generator.simple_admin_command(
            command_name="clean",
            mongodb_method_name="clean",
        )

        #? /fill
        self.step_generator.simple_admin_command(
            command_name="fill",
            mongodb_method_name="fill",
        )
        
        #? /nv 
        #? new_version (step 1) -> prompt for version number 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="command",
            command_name="nv",
            
            active_state=None,
            next_state=VersionSequenceStates.stages[0],
            
            formatted_messages=[self.messages["prompt_new_version_number"]],
            formatted_variables=["user.real_name"],
        )
        
        #? new_version -> (step 2) -> prompt for version message 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="state",
            
            active_state=VersionSequenceStates.stages[0],
            next_state=VersionSequenceStates.stages[1],
            state_variable="version_number",
            
            bot_before_message=self.messages["prompt_new_version_changelog"],
        )
        
        #? new_version -> (step 3) -> final (save to DB) 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="state",
            
            active_state=VersionSequenceStates.stages[1],
            next_state=None,
            state_variable="version_changelog",
            
            use_state_data=True,
            requested_state_data="new_version",
            
            mongodb_activation_position="after_messages",
            mongodb_method_name="update_version",
            
            bot_after_message=self.messages["new_version_success"]
        )
        
        
        
        #? /uu  
        #? /uu (step 1) -> user selection from DB 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="command",
            command_name="uu",
            
            active_state=None,
            next_state=UserUpdateSequenceStates.stages[0],
            
            formatted_messages=[self.messages["select_user"]],
            formatted_variables=["user.real_name"],
            
            keyboard_with_before_message="select_users",
        )
        
        #? /uu (step 2) -> property selection from user 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="keyboard",
            handler_filter="user_id",
            
            active_state=UserUpdateSequenceStates.stages[0],
            next_state=UserUpdateSequenceStates.stages[1],
            state_variable="user_id",
            
            bot_before_message=self.messages["select_property"],
            keyboard_with_before_message="select_user_property",
        )
        
        #? /uu (step 3) -> new_value prompt for user 
        self.step_generator.set_command_with_sequence(
            access_level=["admin"],
            handler_type="keyboard",
            handler_filter="user_property",
            
            active_state=UserUpdateSequenceStates.stages[1],
            next_state=UserUpdateSequenceStates.stages[2],
            state_variable="user_property",
            
            bot_before_message=self.messages["new_value_prompt"],
            # keyboard_with_before_message="select_user_property",
        )
        
        #? /uu (step 4) -> final (success message) 
        self.step_generator.set_command_with_sequence(
            handler_type="state",

            active_state=UserUpdateSequenceStates.stages[2],
            next_state=None,
            state_variable="new_value",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            mongodb_activation_position="before_messages",
            mongodb_method_name="update_user",
            
            bot_after_message=self.messages["update_user_success"]
        )
        
        
        self.logger.info('слеш-команды (/) установлены ✅')
        
    
    # #? У студента будет свой раздел payment, у админа - свой
    # #? Админ будет видеть всех студентов, их суммы, доход и статусы оплат (и сколько осталось) 
    # #? Студент видит только свой статус и сумму 
            

