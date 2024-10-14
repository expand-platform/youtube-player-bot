from telebot.states import State, StatesGroup


class UpdateVersionStates(StatesGroup):
    version_number_prompt = State()
    version_message_prompt = State()
    
    stages = [
        version_number_prompt,
        version_message_prompt,
    ] 
        
        