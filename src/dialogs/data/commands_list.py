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
    
    BotCommand("projects", commands["projects"]),
    BotCommand("plan", commands["plan"]),
    BotCommand("codewars", commands["codewars"]),
 
    BotCommand("payment", commands["payment"]),
    BotCommand("card", commands["card"]),

    # BotCommand("hometask", commands["hometask"]),
    BotCommand("lessons", commands["lessons"]),
    BotCommand("done", commands["done"]),

    BotCommand("version", commands["version"]),
]

