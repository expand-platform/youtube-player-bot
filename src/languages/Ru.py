BOT_SETTINGS_RU = {
    "bot_intro_description": "Бот для любимых студентов платформы EXPAND ♥"
}


BOT_COMMANDS_RU = {
    "start": "Все команды бота",
    
    "schedule": "Когда мой урок?",
    "zoom": "Ссылка на Zoom",
    "plan": "План-карта",
    
    "payment": "Реквизиты и оплата",
    "lessons": "Остаток уроков",
    
    "done": "Заполнить отчёт",
    
    "clean": "Очистить базу данных",
    "fill": "Наполнить базу данных",
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

/payment Реквизиты и оплата
/lessons Остаток уроков

/done Заполнить отчёт
"""
],
    
    
#? /schedule, /zoom
"schedule": [
"""*Суббота*

*09:45*
- Ира Г.

*11:00*
- Даня О.
- Дима Л.

*12:30*
- Кирилл К.
- Ярослав Г.

*14:00*
- Назар С.
- Илья С.
""",

"""*Воскресенье*

*09:30*
- Ира Г.
- Олег Г.

*11:00*
- Ярослав Г.
- Никита Ш.

*12:30*
- Максим С.
- Артём Л.
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
    

#? /payment
"payment_amount": """
Цена за этот месяц: {} грн
""",
"payment_details": [
"Карты для оплаты:",
"Приватбанк (Лукьяненко О.):",
"5457 0825 1846 9775",
"Монобанк (Лукьяненко Д.)",
"5375 4114 3011 2057",
"Остаток уроков смотри в /lessons",
],
"payment_status": "Ты (уже оплатил / ещё не оплатил) {} уроки в этом месяце",


#? /lessons, /done 
"done": "Спасибо, {}! Отчёт заполнен ☑",
"lessons_left": "У тебя осталось ещё {} уроков в этом месяце 😎", 
"no_lessons_left": """
В этом месяце у нас больше не намечается уроков 😎

До встречи в следующем!
""" ,
#? Нужно будет сделать, чтобы писало "На этот месяц у нас с тобой всё!", 
#? когда lessons_left == 0


#? Admins 

#? /clean, /fill
"clean_success": "База пользователей очищена 🚮" ,
"fill_success": "Пользователи снова появились в базе данных 👍",
}


