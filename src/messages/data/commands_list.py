from telebot.types import BotCommand
from src.languages.Language import Language

commands = Language().commands


COMMON_SLASH_COMMANDS = [
    BotCommand("start", commands["start"]),
    BotCommand("schedule", commands["start"]),
]
STUDENT_SLASH_COMMANDS = COMMON_SLASH_COMMANDS


ADMIN_SLASH_COMMANDS = COMMON_SLASH_COMMANDS + [
    BotCommand("set_commands", "Змінити команди бота"),
]

