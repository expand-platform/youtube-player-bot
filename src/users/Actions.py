class Actions:
    pass

""" 
    Actions to save in DB:
    - registration 
    - command used 
    - leave chat (idle for 10s-15s) 
    - filled in some data
    - press a button
    - choose a menu link / (or go to specific menu option)

    Structure: 
    [
        "Дамир": [
            {
                "time": "18:09:23 28-12-2023",
                "comment": "зашёл в бота", 
                "action_type": "login", 
                "command": "/start", 
            },
            {
                "time": "18:10:01 28-12-2023",
                "comment": "нажал /start", 
                "action_type": "login", 
                "command": "/start", 
            },
            {
                "time": "18:11:20 28-12-2023",
                "comment": "вышел из бота", 
                "action_type": "logout", 
                "command": "", 
            },
        ]
    ]
"""
