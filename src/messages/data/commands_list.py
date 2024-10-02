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
 
    BotCommand("payment", commands["payment"]),
    
    BotCommand("lessons", commands["lessons"]),
    BotCommand("done", commands["done"]),
]


ADMIN_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
    BotCommand("schedule", commands["schedule"]), # add options for changing data in db
    BotCommand("zoom", commands["zoom"]), # sends link
 
    BotCommand("payment", commands["payment"]), # shows total amount, sum left and payee left
    BotCommand("lessons", commands["lessons"]), # shows lessons left for each student
 
    BotCommand("clean", commands["clean"]),
    BotCommand("fill", commands["fill"]),
]

