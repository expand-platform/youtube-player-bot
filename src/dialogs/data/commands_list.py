from telebot.types import BotCommand
from src.languages.Language import Language

commands = Language().commands

GUEST_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
]


STUDENT_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
    
    BotCommand("schedule", commands["schedule"]),
    BotCommand("zoom", commands["zoom"]),
    
    BotCommand("plan", commands["plan"]),
    # BotCommand("hometask", commands["hometask"]),
 
    BotCommand("payment", commands["payment"]),
    BotCommand("card", commands["card"]),

    BotCommand("lessons", commands["lessons"]),
    BotCommand("done", commands["done"]),

    BotCommand("version", commands["version"]),
]

# Admin commands:
# /clean
# /fill
# /nv - new version
