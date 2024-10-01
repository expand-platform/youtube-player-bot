from fastapi import FastAPI


import uvicorn
from os import getenv

from src.utils.Logger import Logger 
from src.bot.Bot import Bot
from src.messages.BotMessages import BotMessages


def main(app: FastAPI):
    logger = Logger()
    logger.info('сервер FastAPI включён 👀')


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
