BOT_SETTINGS_RU = {
    "bot_intro_description": "Бот для любимых студентов платформы EXPAND ♥"
}


BOT_COMMANDS_RU = {
    "start": "Все команды бота",
    
    "schedule": "Когда мой урок?",
    "zoom": "Ссылка на Zoom",
    
    "plan": "План-карта",
    "codewars": "Случайна задача из Codewars",
    "projects": "Выбиралка проектов",
    
    "payment": "Оплата",
    "card": "Реквизиты и номер карты",
    "lessons": "Остаток уроков",
    
    "hometask": "Домашка",
    
    "done": "Заполнить отчёт",
    
    "clean": "Очистить базу данных",
    "fill": "Наполнить базу данных",
    
    "version": "Что нового в боте?",
}



BOT_MESSAGES_RU = {
#? Guests
"guest_welcome": """Привет, {}! 

Этот бот - приватный. Он создан для студентов курса EXPAND. 

Ты можешь посмотреть мой [ютуб](https://www.youtube.com/@expand_platform), [канал](https://t.me/expand_platform) и [сайт](https://expandplatform.com/) или написать мне [лично](https://t.me/best_prepod), чтобы записаться к нам на обучение""",


#? Students / Admins

#? /start
"welcome_greeting": "Привет, {}! \n\nЧем я могу помочь?",
"start": [
"""
/schedule Когда следующий урок?
/zoom  Ссылка для Zoom

/plan  План-карта
/projects Выбрать задачу или проект
/codewars Случайная задачка из Codewars

/payment Оплата
/card Реквизиты

/lessons Остаток уроков
/done Заполнить отчёт

/version Что нового в боте?
"""
],
    
    
#? /schedule, /zoom
"schedule": [
"""*Суббота*

*08:00*
- Ира Г.

*11:00*
- Даня О.
- Дима Л.
- Назар С.

*15:45*
- Ярослав Г.
- Кирилл К.
""",

"""*Воскресенье*

*11:30*
- Максим С.
- Артём Л.

*13:15*
- Никита Ш.
- Илья С. 
- Олег Г.

*15:00*
- Ярослав Г.
- Кирилл К.
""",
"""
Прислать ссылку для Zoom? 
Нажми /zoom"""
],

"zoom": """Ссылка для встречи в Zoom:
https://us04web.zoom.us/j/5302871397?pwd=b1hVdmRKWXpvc3Vkblo5WkxmamVCdz09
""",


#? /plan
"plan": [
"""
1) План-карта *JavaScript*  
https://www.expandplatform.com/web/  


2) План-карта *Python*  
https://www.expandplatform.com/python/  


3) Разработка *сервисов*  
https://www.expandplatform.com/services/


Карта всех проектов
https://www.expandplatform.com/students/projects/

""",  
],

#? choose project
"project_picker": {
"link": """
Выбери задачу или проект себе по душе:
https://www.expandplatform.com/students/projects/picker/
"""
},

#? codewars bot
"codewars": {
"link": r"""
Хочешь взять прикольную задачку себе по уровню?

Переходи в наш бот с *задачами из Codewars*:  
@codewars\_challenges\_bot
"""
},
    

#? /payment

"payment": {
    
"amount": "Цена за этот месяц: *{} грн*",

"status": """
*{}* уроки в этом месяце

Реквизиты для оплаты: /card
Остаток уроков: /lessons
""",

"details": [
"Карты для оплаты:",
"Приватбанк (Лукьяненко О.):",
"*5457 0825 1846 9775*",
"Монобанк (Лукьяненко Д.)",
"*5375 4114 3011 2057*",
"Остаток уроков смотри в /lessons",
],

},


#? /done 
"done": "Спасибо, {}! Отчёт заполнен ☑",
"done_forbidden": """
Прости, {}, но ты уже заполнил(а) все необходимые отчёты за этот месяц 🙃

Жду тебя на следующей неделе!""",


#? /lessons
"lessons_left": "У тебя осталось ещё {} уроков в этом месяце 😎", 
"no_lessons_left": """
В этом месяце у нас больше не намечается уроков 😎

До встречи в следующем!
""" ,

#? /version
"version_intro": "Что нового в боте 👓",

#? /hometask
"hometask": {
"empty": "Домашнего задания пока нет",

"task": """
Домашка на эту неделю:

{}
""",

"buttons": {
    "edit_button": "Изменить д/з" 
}
},


#! Admins 
#? /clean, /fill
"clean_success": "База пользователей очищена 🚮" ,
"fill_success": "Пользователи снова появились в базе данных 👍",

#? /nv (new version)
"prompt_new_version_number": "{}, какой номер новой версии (только цифры) ❓",
"latest_version": "Последняя версия: {}",
"prompt_new_version_changelog": "Теперь кратко опиши изменения в новой версии (их увидят твои студенты)",
"new_version_success": "Новая версия бота опубликована в /version 😎",

#? /uu (update user)
"select_user": "Кого меняем?",
"select_property": "*Что* меняем?",
"new_value_prompt": "Какое значение задаём?",
"update_user_success": "⭐ Пользователь успешно изменён!",

#? /su: see user
"su_intro": "Кого смотрим?",
"su_another_user": "🥂 Жми /su для другого пользователя",

#? monthly refresh data
"monthly_data_refresh": {
"intro": "Время обновить данные наших студентов...",
"success": "Данные студентов обновлены 👍\nСмотри /su",
},

"weekly_replica": {
"intro": "Время создать реплику данных наших студентов...",
"success": "Данные студентов реплицированы! ✅",
},

"replica": {
    "success": "🎄 Коллекция успешно реплицирована! 🎄",
    "load_success": "🎄 Данные успешно восстановлены из реплики! 🎄\nПроверь /su",
},

#? bulk editor
"bulk_editor": {

"select_user_type": "Кого будем менять?",
"select_user_property": "Что будем менять?",
"enter_new_value": "Введи новое значение:",

"success": """
🏁 Пользователи успешно изменены! 

Смотри /su
""",

},

}


MONTHS_RU = {
    1: "января", 
    2: "февраля", 
    3: "марта", 
    4: "апреля",
    5: "мая", 
    6: "июня", 
    7: "июля", 
    8: "августа",
    9: "сентября", 
    10: "октября", 
    11: "ноября", 
    12: "декабря"
}