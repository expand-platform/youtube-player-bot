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
 
    BotCommand("lessons", commands["lessons"]),
    BotCommand("payment", commands["payment"]),
    
    BotCommand("done", commands["done"]),
]

# Admin commands:
# /clean
# /fill
