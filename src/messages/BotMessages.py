from telebot import TeleBot
from telebot.states.sync.context import StateContext
from telebot.types import Message

from src.messages.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS, ADMIN_SLASH_COMMANDS

from src.messages.InlineKeyboard import InlineKeyboard
from src.database.MongoDB import MongoDB
from src.utils.Logger import Logger
from src.bot.States import UserStates
from src.languages.Language import Language
from src.users.User import User

from src.bot.Bot import Bot



class BotMessages:
    def __init__(self, bot: Bot):
        self.bot = bot.bot
        self.send_messages = bot.send_messages
        self.format_message = bot.format_message
        self.tell_admin = bot.tell_admin
        
        self.logger = Logger()
        self.messages = Language().messages
        
        self.chat_id = None
        
        self.enable_slash_commands()
        
        
    def set_slash_commands(self, message):
        user = User(message)
        
        if user.access_level == "guest":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)
        
        elif user.access_level == "student":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
            
        elif user.access_level == "admin":
            self.bot.set_my_commands([])
            self.bot.set_my_commands(commands=ADMIN_SLASH_COMMANDS)
        
        
    def enable_slash_commands(self):
        """ clears and sets slash commands """

        # guests
        self.set_guest_start()
        
        # students / admins
        self.set_start()
        self.set_schedule()
        self.set_payment()

        # admin only
        self.set_clean_users()
        
        self.logger.info('слеш-команды (/) установлены ✅')
        
    
    #? Со временем вынесу guest commands в отдельный класс
    def set_guest_start(self):
        @self.bot.message_handler(commands=['start'], access_level=["guest"])
        def handle_guest_start(message):
            # set guests commands 
            self.set_slash_commands(message)
            user = User(message)
            
            
            
            
            self.format_message(chat_id=user.chat_id, message=self.messages["guest_welcome"], format_variable=user.first_name)
            
            self.tell_admin(f"{ user.first_name } @{ user.username } использовал команду /start ✅")
            self.logger.info(f"{ user.first_name } использовал команду /start ✅")
            
        
    """ /start """
    def set_start(self):
        @self.bot.message_handler(commands=["start"], access_level=["student", "admin"])
        def start_command(message: Message):
            self.set_slash_commands(message)
            user = User(message)
            self.chat_id = user.chat_id
            
            
            # greetings and commands
            self.format_message(chat_id=self.chat_id, message=self.messages["welcome_greeting"], format_variable=user.real_name)
            # self.format_message(chat_id=self.chat_id, message=self.messages["access_level"], format_variable=user.access_level)
            
            messages = self.messages["start"]
            self.send_messages(chat_id=self.chat_id, messages=messages)
            
            self.tell_admin(f"{ user.real_name } @{ user.username } нажал /start ✅")
            self.logger.info(f"{ user.real_name } нажал /start ✅")
  
  
  
    """ /schedule """
    def set_schedule(self):
        @self.bot.message_handler(commands=["schedule"], access_level=["student", "admin"])
        def schedule_command(message: Message):
            self.set_slash_commands(message)
            user = User(message)
            self.logger.info(f"текущий юзер команды /schedule: {user.first_name} @{ user.username }")
            self.chat_id = user.chat_id
            
            
            messages = self.messages["schedule"]
            self.send_messages(chat_id=self.chat_id, messages=messages, disable_preview=True)
            
            
            self.tell_admin(f"{ user.real_name } @{ user.username } зашёл в раздел /schedule ⏰")
            self.logger.info(f"{ user.real_name } @{ user.username } зашёл в раздел /schedule ⏰")
            
            
    #? У студента будет свой раздел payment, у админа - свой
    #? Админ будет видеть всех студенто, их суммы, доход и статусы оплат (и сколько осталось) 
    #? Студент видит только свой статус и сумму 
            
    """ /payment """
    def set_payment(self):
        @self.bot.message_handler(commands=["payment"], access_level=["student"])
        def payment_command(message: Message):
            user = User(message)
            mongoDB = MongoDB(user.id)
            self.chat_id = user.chat_id
            
            payment_amount = mongoDB.get_payment_data()
            
            
            
            messages = self.messages["payment_amount"]
            self.format_message(chat_id=self.chat_id, message=messages, format_variable=payment_amount)
            
            self.tell_admin(f"{ user.real_name } @{ user.username } зашёл в раздел /payment 💰")
            self.logger.info(f"{ user.real_name } @{ user.username } зашёл в раздел /payment 💰")
           
           
    """ ADMIN COMMANDS """
    
    
    """ /clean_users """
    def set_clean_users(self):
        @self.bot.message_handler(commands=["clean"], access_level=["admin"])
        def clean_users_command(message: Message):
            user = User(message)
            
            mongoDB = MongoDB(user.id)
            mongoDB.clean_users()
            
            self.tell_admin(f"База пользователей очищена 🚮")



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
            

        
            
            
        
        