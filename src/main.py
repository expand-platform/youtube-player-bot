from contextlib import asynccontextmanager
from math import log
from os import getenv

from fastapi import FastAPI
import uvicorn


from src.utils.Logger import Logger 
from src.bot.Bot import Bot
# from src.messages.BotMessages import BotMessages
# from src.database.MongoDB import MongoDB
from src.database.Database import Database
from src.database.Cache import Cache


@asynccontextmanager
async def main(app: FastAPI):
    logger = Logger()
    logger.info('сервер FastAPI / uvicorn включён 👀')


    database = Database()
    # database.clean_users()
    database.sync_cache_and_remote_users()
    
    
    # set commands and message handlers
    # school_bot = Bot()
    # BotMessages(school_bot)
    # school_bot.start_bot()


    yield
    # school_bot.disconnect_bot()
    logger.info('сервер выключен ❌')
    
    

    
    

app = FastAPI(lifespan=main)


if __name__ == "__main__":
    PORT = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
