from telebot.types import BotCommand
from src.languages.Language import Language

commands = Language().commands

GUEST_SLASH_COMMANDS = [
    # BotCommand("start", commands["start"]),
]


STUDENT_SLASH_COMMANDS = [
    BotCommand("schedule", commands["schedule"]),
    BotCommand("done", commands["done"]),

    BotCommand("payment", commands["payment"]),
    BotCommand("version", commands["version"]),
]

