from telebot import TeleBot
from telebot.states.sync.context import StateContext
from telebot.types import Message

from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS, ADMIN_SLASH_COMMANDS

from src.messages.InlineKeyboard import InlineKeyboard
from src.database.MongoDB import MongoDB
from src.utils.Logger import Logger
from src.bot.States import UserStates
from src.languages.Language import Language
from src.users.Users import NewUser

from src.bot.Bot import Bot
from src.automation.StepGenerator import StepGenerator

from src.users.Users import Users


class BotMessages:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot.bot_instance
        self.chat_id = None
        
        # helpers
        self.tell_admin = bot.tell_admin
        
        self.step_generator = StepGenerator(bot)
        self.logger = Logger()
        self.messages = Language().messages
        
        # self.users = Users()
        
        self.enable_slash_commands()
   
        
    def enable_slash_commands(self):
        """ clears and sets slash commands """
        #? Guests
        #? /start
        self.step_generator.set_command(
            command_name="start",
            access_level=["guest"],
            
            set_slash_command=True,
            
            format_message=self.messages["guest_welcome"],
            format_variable="user.first_name",
        )
        
        
        #? Students 
        #? /start 
        self.step_generator.set_command(
            command_name="start",
            access_level=["student", "admin"], 
            
            set_slash_command=True,
            
            format_message=self.messages["welcome_greeting"],
            format_variable="user.real_name",
            
            message_text=self.messages["start"],
        )
        
        #? /schedule 
        self.step_generator.set_command(
            command_name="schedule",
            access_level=["student", "admin"], 
            
            multiple_messages=self.messages["schedule"],
        )
        
        #? /payment 
        self.step_generator.set_command(
            command_name="payment",
            access_level=["student", "admin"], 
            
            format_message=self.messages["payment_amount"],
            format_variable="user.payment",
        )
        

        #? Admin
        self.set_clean_users()
        self.fill_database()
        
        self.logger.info('слеш-команды (/) установлены ✅')
        
        
    
    # #? У студента будет свой раздел payment, у админа - свой
    # #? Админ будет видеть всех студенто, их суммы, доход и статусы оплат (и сколько осталось) 
    # #? Студент видит только свой статус и сумму 
            
           
    #? ADMIN COMMANDS 
    # """ /clean_users """
    def set_clean_users(self):
        @self.bot.message_handler(commands=["clean"], access_level=["admin"])
        def clean_users_command(message: Message):
            
            MongoDB().clean_users()
            self.tell_admin(self.messages["clean_success"])


    def fill_database(self):
        @self.bot.message_handler(commands=["fill"], access_level=["admin"])
        def clean_users_command(message: Message):
            
            MongoDB().save_students()
            self.tell_admin(self.messages["fill_success"])









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
            

        
            
            
        
        