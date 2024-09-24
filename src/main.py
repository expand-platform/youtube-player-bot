from fastapi import FastAPI


import uvicorn
from os import getenv, path

from src.utils.Logger import Logger 
from src.bot.Bot import SchoolBot
from src.messages.BotMessages import BotMessages, SlashCommands 


def main(app: FastAPI):
    logger = Logger()
    logger.info('сервер FastAPI включён 👀')

    
    school_bot = SchoolBot()
    
    # set commands and message handlers
    SlashCommands(school_bot) 
    BotMessages(school_bot)
    
    school_bot.start_bot()
    
    
    yield
    logger.info('код при выключении ❌')
    
    school_bot.disconnect_bot()
    logger.info('сервер выключен ❌')
    

app = FastAPI(lifespan=main)


if __name__ == "__main__":
    PORT = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
