from src.utils.Logger import Logger
from src.languages.Language import Language

from src.bot.States import UpdateVersionStates

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
            formatted_variables=["user.first_name"],
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
            
            formatted_messages=[self.messages["done"], self.messages["lessons_left"]],
            formatted_variables=["user.real_name", "user.done"],
            
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
        self.step_generator.admin_command_with_state(
            handler_type="command",
            command_name="nv",
            
            active_state=None,
            next_state=UpdateVersionStates.stages[0],
            
            formatted_messages=[self.messages["prompt_new_version_number"]],
            formatted_variables=["user.real_name"],
        )
        
        #? new_version -> (step 2) -> prompt for version message 
        self.step_generator.admin_command_with_state(
            handler_type="state",
            
            active_state=UpdateVersionStates.stages[0],
            next_state=UpdateVersionStates.stages[1],
            state_variable="version_number",
            
            bot_message=self.messages["prompt_new_version_changelog"],
        )
        
        #? new_version -> (step 3) -> final (save to DB) 
        self.step_generator.admin_command_with_state(
            handler_type="state",
            
            active_state=UpdateVersionStates.stages[1],
            next_state=None,
            state_variable="version_changelog",
            
            use_state_data=True,
            requested_state_data="new_version",
            
            mongodb_activation_position="after_messages",
            mongodb_method_name="update_version",
            
            bot_reply=self.messages["new_version_success"]
        )
        
        
        self.logger.info('слеш-команды (/) установлены ✅')
        
    
    # #? У студента будет свой раздел payment, у админа - свой
    # #? Админ будет видеть всех студентов, их суммы, доход и статусы оплат (и сколько осталось) 
    # #? Студент видит только свой статус и сумму 
            









# class BotMessages:
#     def __init__(self, bot: Bot):
#         self.logger = Logger()
#         self.messages = Language().messages
#         self.mongoDB: MongoDB = None
#         self.inline_keyboard = InlineKeyboard()
        
        
#         self.bot = bot.bot
#         self.bot_username = bot.username
#         self.logger.info(self.bot_username)
        
#         self.bot_commands = STUDENT_SLASH_COMMANDS
        
        
#         self.user = None
#         self.from_user_id = 0
#         self.chat_id = 0
#         self.user_real_name = None
        

        
#     def set_slash_commands(self):
#         self.enable_slash_commands()
#         self.logger.info('слеш-команды (/) установлены ✅')

#         self.set_start()
#         self.step_1_language_selection()
#         self.step_2_name_prompt()
#         self.step_3_details_accepted()
#         self.step_4_user_agreement()

#     
            
            
#     """ 1) Обрабатываем кнопки (укр / ру)  """
#     def step_1_language_selection(self):
#         @self.bot.callback_query_handler(func=lambda call: True, state=UserStates.language_selection)
#         def language_button(call, state: StateContext):
#             state.set(UserStates.name_prompt)
            
#             callback_data = call.data
            
#             if callback_data == 'ukr':
#                 self.language.active_lang = self.language.ukr
#                 self.mongoDB.update_user_info(key="language", new_value="ukr")
                
#                 self.logger.info("выбран украинский язык ✅")
            
#             elif callback_data == 'ru':
#                 self.language.active_lang = self.language.ru
#                 self.mongoDB.update_user_info(key="language", new_value="ru")

#                 self.logger.info("выбран русский язык ✅")
            
            
#             # Send a response to the user
#             self.bot.answer_callback_query(call.id, text="")
            
#             self.bot.send_message(call.message.chat.id, text=self.language.active_lang["step_1_language_selection"]["reply_after_selection"])
            
#             name_prompt = self.language.active_lang["step_2_name_prompt"]["name_prompt"]
#             self.bot.send_message(self.chat_id, text=name_prompt)
           
            
#             self.logger.info("Переходим к вводу имени 🖋")
            

        
#     """ 2) name input """
#     def step_2_name_prompt(self):
#         @self.bot.message_handler(state=UserStates.name_prompt)
#         def name_message(message: Message, state: StateContext):
#             state.set(UserStates.campaign_details)
            
#             self.user_real_name = message.text
#             self.mongoDB.save_real_name(real_name=self.user_real_name) 
            
#             self.logger.info('Имя у нас на руках и сохранено в БД ✅')
            
            
#             name_prompt_reply = self.language.active_lang["step_2_name_prompt"]["name_prompt_reply"] + self.user_real_name
#             self.bot.send_message(self.chat_id, text=name_prompt_reply)

#             # second message            
#             details_intro_message = self.language.active_lang["step_3_campaign_details"]["details_intro"] 
#             self.bot.send_message(self.chat_id, text=details_intro_message)
            
#             campaign_conditions = self.language.active_lang["step_3_campaign_details"]["details_conditions"]
#             self.bot.send_message(self.chat_id, text=campaign_conditions)

            
#             self.inline_keyboard.show_yes_no_keyboard(
#                 yes_button_text=self.language.active_lang["step_3_campaign_details"]["details_accepted_button"],
#                 no_button_text=self.language.active_lang["step_3_campaign_details"]["details_maybe_button"],
                
#                 yes_button_callback="details_accepted",
#                 no_button_callback="details_maybe",
#             )

#             campaign_details_end = self.language.active_lang["step_3_campaign_details"]["details_end"]
#             self.bot.send_message(
#                 chat_id=self.chat_id,
#                 text=campaign_details_end,
#                 reply_markup=self.inline_keyboard.keyboard
#             )
            
#             self.logger.info('Детали рассказаны, жмём кнопку дальше... ✅')
            
            
#     """ 3) Пользователь соглашается на детали (жмёт кнопки) """
#     def step_3_details_accepted(self):
#         @self.bot.callback_query_handler(func=lambda call: True, state=UserStates.campaign_details)
#         def agreement_handler(call, state: StateContext):
#             callback_data = call.data
#             state.set(UserStates.first_search_agreement)
            
#             self.inline_keyboard.show_yes_no_keyboard(
#                 yes_button_text=self.language.active_lang["step_4_user_agreement"]["agree_button_text"],
#                 no_button_text=self.language.active_lang["step_4_user_agreement"]["not_sure_button_text"],
                
#                 yes_button_callback="agree",
#                 no_button_callback="not_sure",
#             )
            
            
#             if callback_data == 'details_accepted':
#                 self.bot.send_message(call.message.chat.id, text=self.language.active_lang["step_4_user_agreement"]["success_call_to_action"], reply_markup=self.inline_keyboard.keyboard)
#                 self.logger.info("Пользователь согласен ✅")
                
#             elif callback_data == 'details_maybe':
#                 self.bot.send_message(call.message.chat.id, text=self.language.active_lang["step_4_user_agreement"]["maybe_call_to_action"], reply_markup=self.inline_keyboard.keyboard)
#                 self.logger.info("Пользователь решил подумать ❌")
            
            
#             # Send a response to the user
#             self.bot.answer_callback_query(call.id, text="")
            
#             self.logger.info('Выбор сделан ✅')
            
            
#     """ 4) Пользователь соглашается начать поиск (и жмёт кнопки) """
#     def step_4_user_agreement(self):
#         @self.bot.callback_query_handler(func=lambda call: True, state=UserStates.first_search_agreement)
#         def agreement_handler(call, state: StateContext):
#             state.set(UserStates.start_first_search)
#             callback_data = call.data
            
#             if callback_data == 'agree':
#                 self.bot.send_message(call.message.chat.id, text=self.language.active_lang["step_4_user_agreement"]["agree_reply"])
#                 self.logger.info("Пользователь согласен ✅")
#             elif callback_data == 'not_sure':
#                 self.bot.send_message(call.message.chat.id, text=self.language.active_lang["step_4_user_agreement"]["not_sure_reply"])
#                 self.logger.info("Пользователь решил подумать ❌")
            
            
#             # Send a response to the user
#             self.bot.answer_callback_query(call.id, text="")
            
#             self.logger.info('Выбор сделан ✅')
#             self.logger.info("Ты достиг конца переписки с ботом 🏁")
            
#             self.bot.stop_polling()
            

        
            
            
        
        