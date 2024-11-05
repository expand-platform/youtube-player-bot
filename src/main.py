from os import getenv
from threading import Thread
from keyboard import add_hotkey
import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.utils.Logger import Logger
from src.utils.Time import Time
from src.database.Database import Database
from src.bot.Bot import Bot
from src.dialogs.BotDialogs import BotDialogs



class Server:
    def __init__(self):
        self.log = Logger().info
        self.time = Time()
        
        self.bot = Bot()
        
        # threads 
        self.bot_thread = None
        self.listener_thread = None
        
        self.app = FastAPI(lifespan=self.start_server)
        
        
        
    @asynccontextmanager
    async def start_server(self, app: FastAPI):
        self.log("сервер FastAPI / uvicorn включён 👀")
        
        self.start_threads()

        try:
            yield  
        
        except KeyboardInterrupt:
            self.log("Manual shutdown triggered.")
        
        finally:
            self.shut_server_down()
            


    def start_threads(self):
        self.start_ctrl_c_thread()
        self.time.set_scheduled_tasks()
        
        self.start_bot_thread()


    def start_bot_thread(self):
        database = Database()
        database.sync_cache_and_remote_users()
        
        BotDialogs().enable_dialogs()
        
        self.bot_thread = Thread(target=self.bot.start_bot)
        self.bot_thread.start()
        

    def start_ctrl_c_thread(self):
        self.listener_thread = Thread(target=self.handle_ctrl_c)
        self.listener_thread.start()
        

    def handle_ctrl_c(self):
        add_hotkey("ctrl+c", self.shut_server_down)
        
        
    def shut_server_down(self):
        self.bot.disconnect_bot()
        uvicorn.server.Server.should_exit = True
        
        self.time.scheduler.remove_all_jobs()
        self.listener_thread.join()
          
        self.bot_thread.join()  
        
        self.log("Сервер выключен ❌")
        


server = Server()
app = server.app


if __name__ == "__main__":
    PORT = int(getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
