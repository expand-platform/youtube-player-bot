from fastapi import FastAPI


import uvicorn
from os import getenv

from src.utils.Logger import Logger 
from src.bot.Bot import Bot
from src.messages.BotMessages import BotMessages


def main(app: FastAPI):
    logger = Logger()
    logger.info('сервер FastAPI включён 👀')

    #? Тут будет примерно следующий порядок:
    #? 1) Инициализируется Mongo, вносит в БД пользователей (если нужно, т.к. там уже могут быть пользователи). Кажется, insert_one не будет делать это, если юзер уже есть в БД. Если же нет, делаем проверку is_user_exists()
    #? 2) Затем кешируем всех юзеров тут (по любому делаем это при старте). Класс CachedUsers, в котором будут находится юзеры (но в кеше может жить куда больше)
    #? 3) Только после этого есть смысл запускать бота и всё остальное
    
    #? 1) Сохраняем юзеров в БД
    #? 2) Кешируем их
    #? 3) Запускаем бота с этими данными (кеш должен быть доступен в других местах, это важно). Вероятно, тут его импорта не будет или же он просто будет импортится из одного файла в разные места (чтобы избежать circular import)


    # set commands and message handlers
    school_bot = Bot()
    BotMessages(school_bot)
    school_bot.start_bot()
    
    school_bot.disconnect_bot()
    logger.info('сервер выключен ❌')
    

app = FastAPI(lifespan=main)


if __name__ == "__main__":
    PORT = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
