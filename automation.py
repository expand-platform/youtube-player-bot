DIALOGS = [
    #? Chapter 1: introduction
    #? Step 1: language selection
    {
        "step": {
            "name": "language_selection",
            "total_order": 1,
            
            "chapter_order": 1,
            "chapter_name": "introduction",
        
            "configuration": {
                "prompt": {
                    "type": "yes_no_buttons",
                },
                
                "slash_command": {
                    "is_slash_command": True,
                    "command_name": "/start",
                },
                
                "actions": {
                    "code": ["save_user_id", "create_user"],
                    "database": ["create_user", "update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_1_1_language_selection,
                "next_state": UserStates.step_1_1_name_prompt,
            },
        },

        
        "prompt": {
            "type": "options",
            
            "before_prompt_messages": {
                "ukr": ["Обери мову / Выбери язык"],
                "ru": ["Обери мову / Выбери язык"],
            },
            
            
            # buttons text, for example
            "prompt_options": {
                "ukr": [
                    { "yes": "Українська" },
                    { "no": "Русский" },
                ],
                "ru": [
                    { "yes": "Українська" },
                    { "no": "Русский" },
                ],
            },
          
            "options_callbacks": {
                "names":  [
                    { "yes": "ukr" }, 
                    { "no": "ru" }
                ],
                "actions": {
                    "code": ["update_active_lang"],
                    "database": ["update_active_lang", "update_last_state", "update_max_state"],
                }
            },
            
            "options_replies": {
                "ukr": [
                    { "yes": "Я запам'ятав твій вибір 👌" },
                    { "no": "Я запам'ятав твій вибір 👌" },
                ],
                "ru": [
                    { "yes": "Я запомнил твой выбор 👌" },
                    { "no": "Я запомнил твой выбор 👌" },
                ],
            },
        },
        
        "action_message": "{} first_name {} username выбрал язык {} lang ✅",
    },


    #? Chapter 1: introduction
    #? Step 2: name prompt
    {
        "step": {
            "name": "name_prompt",
            "total_order": 2,
            
            "chapter_order": 1,
            "chapter_name": "introduction",
            
            "configuration": {
                "prompt": {
                    "type": "text_prompt",
                    "data_type": "text",
                    "data_validation": "first_name",
                },
                
                "slash_command": {
                    "is_slash_command": False,
                    "command_name": "",
                },
                
                "actions": {
                    "code": ["save_real_name"],
                    "database": ["save_real_name", "update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_1_1_name_prompt,
                "next_state": UserStates.step_1_2_campaign_details,
            },
        },

        
        "prompt": {
            "type": "input",
            
            "before_prompt_messages": {
                "ukr": ["Введи своє ім'я і я розповім, що потрібно робити для того, щоб отримати $30 від Даміра"],
                "ru": ["Введи своё имя, и я расскажу, что нужно сделать, чтобы получить $30 от Дамира"],
            },
            
            "prompt_reply": {
                "ukr": [ "Радий знайомству, " ],
                "ru":  [ "Рад знакомству, " ],
            },
        },
        
        "action_message": "{} first_name {} username ввёл своё настоящее имя: {} name ✅",
    },
    

    
    #? Chapter 1: introduction
    #? Step 3: campaign details
    {
        "step": {
            "name": "campaign_details",
            "total_order": 3,
            
            "chapter_order": 1,
            "chapter_name": "introduction",
        
            "configuration": {
                "prompt": {
                    "type": "yes_no_buttons",
                },
                
                "slash_command": {
                    "is_slash_command": False,
                    "command_name": "",
                },
                
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_1_2_campaign_details,
                "next_state": UserStates.step_1_3_first_search_agreement,
            },
        },

        
        "prompt": {
            "type": "yes_no_buttons",
            
            "before_prompt_messages": {
                "ukr": [
                    "Розказую тобі умови:", 
                    "1. Ти рекомендуєш мені друга чи подругу, який (або яка) цікавиться програмуванням \n\n2. Друг чи подруга записується на пробний, безкоштовний, урок \n\n3. Він чи вона оплачує перший місяць навчання \n\n4. Після оплати я надсилаю тобі гроші",
                    "Звучить як план, що скажеш?",
                ],
                "ru": [
                    "Делюсь с тобой условиями:", 
                    "1. Ты советуешь мне друга или подругу, который (или которая) интересуется программированием \n\n2. Друг или подруга записывается на пробное, бесплатное занятие \n\n3. Он или она оплачивает первый месяц учёбы \n\n4. После оплаты я отправляю тебе деньги на карту",
                    "Звучит как план. Что скажешь?",
                ],
            },
            
            
            "prompt_options": {
                "ukr": [
                    { "yes": "Так" },
                    { "no": "Можливо" },
                ],
                "ru": [
                    { "yes": "Да" },
                    { "no": "Наверное" },
                ],
            },
          
          
            "options_callbacks": {
                "names":  [
                    { "yes": "details_accepted" }, 
                    { "no": "details_maybe" }
                ],
                "actions": {
                    "code": [],
                    "database": [],
                }
            },
            
            "options_replies": {
                "ukr": [
                    { "yes": "Я запам'ятав твій вибір 👌" },
                    { "no": "Я запам'ятав твій вибір 👌" },
                ],
                "ru": [
                    { "yes": "Я запомнил твой выбор 👌" },
                    { "no": "Я запомнил твой выбор 👌" },
                ],
            },
        },
        
        "action_message": {
            "yes": "{} first_name {} username принял условия ✅",
            "no": "{} first_name {} username решил подумать над условиями ❌",
        },
    },

    

    #? Chapter 1: introduction
    #? Step 4: first search agreement
    {
        "step": {
            "name": "first_search_agreement",
            "total_order": 4,
            
            "chapter_order": 1,
            "chapter_name": "introduction",
        
            "configuration": {
                "prompt": {
                    "type": "yes_no_buttons",
                },
                
                "slash_command": {
                    "is_slash_command": False,
                    "command_name": "",
                },
                
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_1_3_first_search_agreement,
                "next_state": UserStates.step_1_4_start_first_search,
            },
        },

        
        "prompt": {
            "type": "yes_no_buttons",
            
            "before_prompt_messages": {
                "ukr": [
                    "Тоді візьмешся за пошук першого студента? Якщо розібратись, завдання не таке вже й складне. \n\nСкажу одразу: Дамір сказав мені, щоб я допоміг тобі з пошуком першого студента. Почнемо?", 
                ],
                "ru": ["Тогда возьмёшься за поиск первого студента? Если разобраться, задача не такая уж и сложная. \n\nСразу скажу: Дамир попросил меня помочь тебе с поиском первого студента. Готов?"],
            },
            
            
            "prompt_options": {
                "ukr": [
                    { "yes": "Чому й ні? Спробую" },
                    { "no": "Можливо, але пізніше" },
                ],
                "ru": [
                    { "yes": "Хорошо, попробую" },
                    { "no": "Возможно, позже" },
                ],
            },
          
          
            "options_callbacks": {
                "names":  [
                    { "yes": "agree" }, 
                    { "no": "not_sure" }
                ],
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                }
            },
            
            "options_replies": {
                "ukr": {
                    { "yes": "Чудово, радий чути! \n\nВідтепер ти - партнер Даміра по рекламі! 🎉\n\nДавай я допоможу тобі з пошуком першого студента. Ряд коротких питань - і 30 доларів в тебе!" },
                    { "no": "Добре. Проте пам'ятай: можливості з'являються неочікувано і неочікувано зникають. \n\nНе варто відкладати на завтра те, на чому можна заробити сьогодні. " },
                },
                "ru": {
                    { "yes": "Отлично, рад слышать! \n\nДавай я помогу тебе с поиском первого студента. Серия коротких вопросов - и 30 долларов твои!" },
                    { "no": "Хорошо. Но помни: возможности появляются неожиданно и также неожиданно исчезают. \n\nНе стоит откладывать то, на чём можно заработать сегодня." },
                },
            },
        },
        
        "action_message": {
            "yes": "{} first_name {} username решил взяться за поиск первого студента ✅",
            "no": "{} first_name {} username решил отложить первый поиск ❌",
        },
    },


    #? Chapter 1: introduction.  
    #? Step 5: start education
    {
        "step": {
            "name": "start_first_search",
            "total_order": 5,
            
            "chapter_order": 1,
            "chapter_name": "introduction",
        
            "configuration": {
                "prompt": {
                    "type": "single_option",
                },
                
                "slash_command": {
                    "is_slash_command": False,
                    "command_name": "",
                },
                
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_1_4_start_first_search,
                "next_state": UserStates.step_2_1_friend_suggestion,
            },
        },

        
        "prompt": {
            "type": "single_option",
            
            "before_prompt_messages": {
                "ukr": [
                    "Чудово, радий чути! \n\nВідтепер ти - партнер Даміра по рекламі! 🎉", 
                    "Давай я допоможу тобі з пошуком першого студента. Ряд коротких питань та дій і 30 доларів - твої!",
                ],
                "ru": [
                    "Тогда возьмёшься за такое задание? Если разобраться, оно не такое уж и сложное. \n\nСкажу сразу: Дамир попросил меня сразу помочь тебе с поиском студентов. Начнём?"
                ],
            },
            
            
            "prompt_options": {
                "ukr": "Почати навчання",
                "ru": "Начать изучение",
            },
          
          
            "options_callbacks": {
                "names":  [
                    { "yes": "start" }, 
                ],
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                }
            },
            
            "options_replies": {
                "ukr": "Тоді натисни або напиши /new_friend і ми почнемо 👌",
                "ru": "Тогда нажми или напиши /new_friend и мы начнём 👌",
            },
        },
        
        "action_message": "{} first_name {} username начинает поиск первого студента... ✅",
    },
    
    
    #! Start chapter 2
    
    
    #? Chapter 2: new student suggestion
    #? Step 1: introduction
    {
        "step": {
            "name": "first_search_agreement",
            "total_order": 6,
            
            "chapter_order": 2,
            "chapter_name": "new_student_suggestion",
        
            "configuration": {
                "prompt": {
                    "type": "yes_no_buttons",
                },
                
                "slash_command": {
                    "is_slash_command": True,
                    "command_name": "/new_friend",
                },
                
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                },     
            },
            
            "states": {
                "current_state": UserStates.step_2_1_friend_suggestion,
                "next_state": {
                    "yes": UserStates.step_2_2_friend_name_input, 
                    "no": UserStates.step_3_1_education_start,
                },
            },
        },

        
        "prompt": {
            "type": "yes_no_buttons",
            
            "before_prompt_messages": {
                "ukr": [
                    "", 
                ],
                "ru": ["Тогда возьмёшься за такое задание? Если разобраться, оно не такое уж и сложное. \n\nСкажу сразу: Дамир попросил меня сразу помочь тебе с поиском студентов. Начнём?"],
            },
            
            
            "prompt_options": {
                "ukr": [
                    { "yes": "Чому й ні? Спробую" },
                    { "no": "Можливо, але пізніше" },
                ],
                "ru": [
                    { "yes": "Хорошо, попробую" },
                    { "no": "Возможно, позже" },
                ],
            },
          
          
            "options_callbacks": {
                "names":  [
                    { "yes": "agree" }, 
                    { "no": "not_sure" }
                ],
                "actions": {
                    "code": [],
                    "database": ["update_last_state", "update_max_state"],
                }
            },
            
            "options_replies": {
                "ukr": [
                    { "yes": "Чудово, радий чути! \n\nВідтепер ти - партнер Даміра по рекламі! 🎉\n\n Ти досяг рівня 1! \n\n Давай я допоможу тобі з пошуком першого студента. Ряд коротких питань та дій - і дійдеш до рівня 2!" },
                    { "no": "Добре. Проте пам'ятай: можливості з'являються неочікувано і неочікувано зникають. \n\nНе варто відкладати на завтра те, на чому можна заробити сьогодні. " },
                ],
                "ru": [
                    { "yes": "Отлично! \n\nТогда такой вопрос: кто из твоих друзей интересуется программированием? Может быть, даже ты сам (ха-ха)" },
                    { "no": "Хорошо. Но помни: возможности появляются неожиданно и также неожиданно исчезают. \n\nНе стоит откладывать то, на чём можно заработать сегодня." },
                ],
            },
        },
        
        "action_message": {
            "yes": "{} first_name {} username решил взяться за поиск первого студента ✅",
            "no": "{} first_name {} username решил отложить первый поиск ❌",
        },
    },
    
    
    """ 
        Часть 2: поиск студента
        
        1. Тебе нужно найти студента для Дамира
            yes/no
            - Я знаю кое-кого! (next state: 6 or 7)
            - Помоги с поиском (/help_me)
        
        
        YES button: 2. Если знает (заполнение)
            1) Введи имя
            
            2) Пришли его / её юзернейм или ссылку в телеграме (для связи)
            
            3) Введи мобильный (если знаешь) [optional]

                (save_stats_to_db)
                
            4) Уведомление о том, что "твоё предложение будет Approve / reject by admin. Дамир скоро напишет тебе"
            
            5) Увеличение уровня партнёра! Объяснение деталей (если много советуешь, получишь больше денег, когда таки найдёшь студента!) 1-2-3 попытки дадут свои плоды!
            
            6) Прощание (до скорой встречи)
            
            
        NO button: 2. Если не знает (вводит команду /help_me)
        
            1) Тут будет обучение, выборы разных вариантов (переход к части 3: обучение)
            
            Тут тоже будет куча промптов, только выборы будут не yes/no, а множественные (может сделаю клавиатуру крупную нижнюю, не инлайновую)
    """
  
]
