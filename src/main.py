from os import getenv
from threading import Thread
from keyboard import add_hotkey
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.utils.Logger import Logger
from src.database.Database import Database
from src.bot.Bot import Bot
from src.dialogs.BotDialogs import BotDialogs


class Server:
    def __init__(self):
        self.log = Logger().info
        self.bot = Bot()
        
        self.app = FastAPI(lifespan=self.start_server)
        
        self.listener_thread = Thread(target=self.handle_ctrl_c)
        self.listener_thread.start()
        
        
    @asynccontextmanager
    async def start_server(self, app: FastAPI):
        self.log("сервер FastAPI / uvicorn включён 👀")

        database = Database()
        database.sync_cache_and_remote_users()
        
        BotDialogs().enable_dialogs()
        
        bot_thread = Thread(target=self.bot.start_bot)
        bot_thread.start()

        try:
            yield  
        
        except KeyboardInterrupt:
            self.log("Manual shutdown triggered.")
        
        finally:
            self.bot.disconnect_bot()
            bot_thread.join()  
            self.log("сервер выключен ❌")
            self.listener_thread.join()  


    def handle_ctrl_c(self):
        add_hotkey("ctrl+c", self.shutdown)
        

    def shutdown(self):
        self.log("CTRL+C detected from keyboard! Initiating shutdown...")
        self.bot.disconnect_bot()
        uvicorn.server.Server.should_exit = True
        self.log("Server and bot shutdown complete.")


server = Server()
app = server.app


if __name__ == "__main__":
    PORT = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
