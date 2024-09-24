from telebot import TeleBot
from telebot.states.sync.context import StateContext
from telebot.types import Message

from src.messages.data.commands_list import STUDENT_SLASH_COMMANDS

from src.messages.InlineKeyboard import InlineKeyboard
from src.database.MongoDB import MongoDB
from src.utils.Logger import Logger
from src.bot.States import UserStates
from src.languages.Language import Language
from src.users.User import User

from src.bot.Bot import Bot


""" Проблема: бот на другом телефоне всё равно видит первого сохранённого пользователя, который вошёл в бот, то есть меня... Это пиздец, честно говоря, это всё сильно усложняет... """

class SlashCommands:
    def __init__(self, bot: Bot):
        self.bot = bot.bot
        self.send_messages = bot.send_messages
        self.tell_admin = bot.tell_admin
        
        self.logger = Logger()
        self.mongoDB = None
        
        self.messages = Language().messages
        
        self.chat_id = None
        
        
        self.enable_slash_commands()
        
        
    def enable_slash_commands(self):
        """ clears and sets slash commands """
        self.bot.set_my_commands([])
        self.bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)
        
        # slash commands handlers
        self.set_start()
        self.set_schedule()
        
        self.logger.info('слеш-команды (/) установлены ✅')
        
        
    """ /start """
    def set_start(self):
        @self.bot.message_handler(commands=["start"])
        def start_command(message: Message):
            self.user = User(message)
            self.logger.info(f"текущий юзер команды /start: {self.user.first_name} @{ self.user.username }")
            self.chat_id = self.user.chat_id
            
            self.mongoDB = MongoDB(self.chat_id)
            
            
            messages = self.messages["start"]
            
            self.logger.info(f"first name в коде: { self.user.first_name }")
            
            # messages[0] = messages[0].format(self.user.first_name)
            self.send_messages(chat_id=self.chat_id, messages=messages)
            
            
            self.tell_admin(f"{ self.user.first_name } @{ self.user.username } использовал команду /start ✅")
            self.logger.info(f"{ self.user.first_name } использовал команду /start ✅")
  
  
    """ /schedule """
    def set_schedule(self):
        @self.bot.message_handler(commands=["schedule"])
        def schedule_command(message: Message):
            self.user = User(message)
            self.logger.info(f"текущий юзер команды /schedule: {self.user.first_name} @{ self.user.username }")
            self.chat_id = self.user.chat_id
            
            
            messages = self.messages["schedule"]
            self.send_messages(chat_id=self.chat_id, messages=messages)
            
            self.tell_admin(f"{ self.user.first_name } @{ self.user.username } использовал команду /schedule ✅")
            self.logger.info(f"{ self.user.first_name } @{ self.user.username } использовал команду /schedule ✅")
           


class BotMessages:
    def __init__(self, bot: Bot):
        self.logger = Logger()
        self.messages = Language().messages
        self.mongoDB: MongoDB = None
        self.inline_keyboard = InlineKeyboard()
        
        
        self.bot = bot.bot
        self.bot_username = bot.username
        self.logger.info(self.bot_username)
        
        self.bot_commands = STUDENT_SLASH_COMMANDS
        
        
        self.user = None
        self.from_user_id = 0
        self.chat_id = 0
        self.user_real_name = None
        

        
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
            

        
            
            
        
        