from src.utils.Logger import Logger
from src.languages.Language import Language

from src.bot.Bot import Bot
from src.dialogs.DialogGenerator import DialogGenerator

from src.bot.States import VersionSequenceStates, UpdateUserSequenceStates, SeeUserSequenceStates, BulkEditorStates

class AdminDialogs:
    def __init__(self):
        self.log = Logger().info
        
        self.bot = Bot()
        
        self.dialog_generator = DialogGenerator()
        self.messages = Language().messages
        
    def set_admin_dialogs(self):
        #? /clean
        self.dialog_generator.simple_admin_command(
            command_name="clean",
            mongodb_method_name="clean",
        )

        #? /fill
        self.dialog_generator.simple_admin_command(
            command_name="fill",
            mongodb_method_name="fill",
        )
        
               
        #! need to write /replica to test new time features (scheduler)
        #? /replica
        self.dialog_generator.simple_admin_command(
            command_name="replica",
            
            mongodb_method_name="replicate_users",
            mongodb_activation_position="before_message",
            
            bot_after_message=self.messages["replica"]["success"],
        )
        
        #? /load_replica
        self.dialog_generator.simple_admin_command(
            command_name="load_replica",
            
            mongodb_method_name="load_replica",
            mongodb_activation_position="before_message",
            
            bot_after_message=self.messages["replica"]["load_success"],
        )
        
        #? /new_month
        self.dialog_generator.simple_admin_command(
            command_name="new_month",
            
            mongodb_method_name="monthly_refresh",
            mongodb_activation_position="after_message",
            
            bot_before_message=self.messages["monthly_data_refresh"]["intro"],
            bot_after_message=self.messages["monthly_data_refresh"]["success"],
        )
        
        
        #? /nv 
        #? new_version (step 1) -> prompt for version number 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="nv",
            
            active_state=None,
            next_state=VersionSequenceStates.stages[0],
            
            # mongodb_method_name="show_latest_version",
            # mongodb_activation_position="after_messages",
            
            formatted_messages=[self.messages["prompt_new_version_number"], self.messages["latest_version"]],
            formatted_variables=["user.real_name", "latest_version"],
        )
        
        #? new_version -> (step 2) -> prompt for version message 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="state",
            
            active_state=VersionSequenceStates.stages[0],
            next_state=VersionSequenceStates.stages[1],
            state_variable="version_number",
            
            bot_before_message=self.messages["prompt_new_version_changelog"],
        )
        
        #? new_version -> (step 3) -> final (save to DB) 
        self.dialog_generator.make_dialog(
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
        #? /uu (step 1) -> user selection
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="uu",
            handler_prefix="uu",
            
            active_state=None,
            next_state=UpdateUserSequenceStates.stages[0],
            
            bot_before_message=self.messages["select_user"],
            
            buttons_callback_prefix="user_id",
            keyboard_with_before_message="select_users",
        )
        
        #? /uu (step 2) -> property selection from user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="uu",
            handler_property="user_id",
            
            active_state=UpdateUserSequenceStates.stages[0],
            next_state=UpdateUserSequenceStates.stages[1],
            state_variable="user_id",
            
            bot_before_message=self.messages["select_property"],
            
            buttons_callback_prefix="user_property",
            keyboard_with_before_message="select_user_property",
        )
        
        #? /uu (step 3) -> new_value prompt for user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="uu",
            handler_property="user_property",
            
            active_state=UpdateUserSequenceStates.stages[1],
            next_state=UpdateUserSequenceStates.stages[2],
            state_variable="user_property",
            
            bot_before_message=self.messages["new_value_prompt"],
        )
        
        #? /uu (final: step 4) -> success message 
        self.dialog_generator.make_dialog(
            handler_type="state",
            handler_prefix="uu",

            active_state=UpdateUserSequenceStates.stages[2],
            next_state=None,
            state_variable="new_value",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            mongodb_activation_position="before_messages",
            mongodb_method_name="update_user",
            
            bot_after_message=self.messages["update_user_success"]
        )
        
        
        #? /su (see user) 
        #? /su (step 1) -> user selection 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="su",
            
            handler_prefix="su",
            buttons_callback_prefix="user_id",
            
            active_state=None,
            next_state=SeeUserSequenceStates.stages[0],
            
            bot_before_message=self.messages["su_intro"],
            keyboard_with_before_message="select_users",
        )
        
        #? /su (final: step 2) -> show user info 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
                        
            handler_prefix="su",
            handler_property="user_id",
            
            active_state=SeeUserSequenceStates.stages[0],
            next_state=None,
            state_variable="user_id",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            mongodb_method_name="show_user",
            mongodb_activation_position="before_messages",
            
            bot_before_message=self.messages["su_another_user"],
        )
        
        #? /be -> bulk editor
        #? step 1: select user type by access_level
        self.dialog_generator.make_dialog(
            handler_type="command",
            command_name="be",
            access_level=["admin"],
            
            active_state=None,
            next_state=BulkEditorStates.stages[0],
            
            bot_before_message=self.messages["bulk_editor"]["select_user_type"],
            
            handler_prefix="be",
            buttons_callback_prefix="access_level",
            keyboard_with_before_message="users.access_level",
        )
        
        #? /be (step 2) -> property selection from user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="be",
            handler_property="access_level",
            
            active_state=BulkEditorStates.stages[0],
            next_state=BulkEditorStates.stages[1],
            
            state_variable="user.category",
            use_state_data=True,
            requested_state_data="user.category",
            
            bot_before_message=self.messages["bulk_editor"]["select_user_property"],
            
            buttons_callback_prefix="user_property",
            keyboard_with_before_message="users.access_level.properties",
        )
        
        #? /be (step 3) -> new_value prompt
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="be",
            handler_property="user_property",
            
            active_state=BulkEditorStates.stages[1],
            next_state=BulkEditorStates.stages[2],
            state_variable="user_property",
            
            bot_before_message=self.messages["bulk_editor"]["enter_new_value"],
        )
        
        #? /be (final: step 4) -> success message 
        self.dialog_generator.make_dialog(
            handler_type="state",
            handler_prefix="be",

            active_state=BulkEditorStates.stages[2],
            next_state=None,
            state_variable="new_value",
            
            use_state_data=True,
            requested_state_data="all",
            
            mongodb_activation_position="before_messages",
            mongodb_method_name="bulk_update",
            
            bot_after_message=self.messages["bulk_editor"]["success"],
        )
        
        
        self.log(f"Команды / диалоги админа установлены 🥂")
        
        
                
    #? У студента будет свой раздел payment, у админа - свой
    #? Админ будет видеть всех студентов, их суммы, доход и статусы оплат (и сколько осталось) 
    #? Студент видит только свой статус и сумму 
            
        
        