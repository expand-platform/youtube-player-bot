#? Displayed in menu from left 
MENU_COMMANDS_RU = {
    "schedule": "Когда мой урок?",
    "done": "Заполнить отчёт",

    "payment": "Оплата",
    "version": "Что нового в боте?",
}



BOT_MESSAGES_RU = {
#? Guests only messages
"guest_welcome": """Привет, {}! 

Этот бот - приватный. Он доступен только студентам платформы EXPAND. 

Ты можешь посмотреть мой [ютуб](https://www.youtube.com/@expand_platform), [канал](https://t.me/expand_platform) и [сайт](https://expandplatform.com/) или написать мне [лично](https://t.me/best_prepod), чтобы записаться к нам на обучение""",


#? Common for students x admins

#? /start x welcome message
"welcome_greeting": "Привет, {}! \n\nЧудный день, не так ли?",
"start": [
"""
/schedule Когда мой урок?
/done Заполнить отчёт

/payment Оплата
/version Что нового в боте?
"""
],
    
    
#? /schedule x zoom
"schedule": [
"""
*Понедельник / на неделе*
*08:00* 
😀 Ира

*15:00*
🎨 Ярослав 
🎉 Кирилл 
""",

"""
*Воскресенье*

*09:00* 
🎁 Никита
🎭 Илья 
⭐ Олег

*11:15*
😎 Даня
🤠 Дима 
🧐 Назар

*13:30*
🚀 Максим 
🛹 Артём

*15:45*
🎨 Ярослав 
🎉 Кирилл 
""",

"""Ссылка на Zoom:
https://us04web.zoom.us/j/5302871397?pwd=b1hVdmRKWXpvc3Vkblo5WkxmamVCdz09
"""
],

#? /payment
"payment": {
"amount": "Цена в этом месяце: *{} грн*",
"status": """
*{}* уроки в этом месяце
""",
#? array for sending card numbers separately (it's handy)
"details": [
"Приватбанк, Лукьяненко О.",
" `5457 0825 1846 9775`",
"Монобанк, Лукьяненко Д.",
" `4441 1110 3601 7980`",
],
},


#? /done 
"done": "Спасибо, {}! Отчёт заполнен ☑",
"done_forbidden": """
Прости, {}, но ты уже заполнил(а) все необходимые отчёты за этот месяц 🙃

До встречи на следующей неделе!""",

#? /lessons
"lessons_left": "У тебя осталось ещё {} уроков в этом месяце 😎", 
"no_lessons_left": """
В этом месяце у нас больше не намечается уроков 😎

До встречи на следующей неделе!
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

#? income
"income": {
    "count": "Студентов: *{}*",
    "amount": "Возможный доход : *{} грн*",
    "average": "Средний доход со студента: *{} грн*",
},

#? /nv (new version)
"prompt_new_version_number": "{}, какой номер новой версии (только цифры) ❓",
"latest_version": "Последняя версия: {}",
"prompt_new_version_changelog": "Теперь кратко опиши изменения в новой версии (их увидят твои студенты)",
"new_version_success": "Новая версия бота опубликована в /version 😎",

#? /uu (update user)
"select_user": "Кого меняем?",
"select_property": "*Что* меняем?",
"new_value_prompt": "Какое значение задаём?",
"update_user_success": "⭐ Пользователь успешно изменён! Смотри /su",

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

"remove_user": {
    "select_user": "Кого хочешь удалить?",
    "success": "Пользователь успешно удалён! Смотри /su"
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