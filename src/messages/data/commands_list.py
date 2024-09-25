from telebot.types import BotCommand
from src.languages.Language import Language

commands = Language().commands

GUEST_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
]

STUDENT_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
    BotCommand("schedule", commands["schedule"]),
    BotCommand("payment", commands["payment"]),
]



ADMIN_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
    BotCommand("schedule", commands["schedule"]),
    BotCommand("payment", commands["payment"]),
    # BotCommand("clean", commands["clear_users"]),
]

