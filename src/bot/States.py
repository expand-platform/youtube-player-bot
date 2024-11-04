from telebot.states import State, StatesGroup

#? /nv: new version
class VersionSequenceStates(StatesGroup):
    version_number_prompt = State()
    version_message_prompt = State()
    
    stages = [
        version_number_prompt,
        version_message_prompt,
    ] 


#? / uu: update user
class UpdateUserSequenceStates(StatesGroup):
    select_user = State()
    select_property = State()
    new_value_prompt = State()
    
    stages = [
        select_user,
        select_property,
        new_value_prompt,
    ]
    
#? /su: see use 
class SeeUserSequenceStates(StatesGroup):
    su_select_user = State()
    
    stages = [
        su_select_user
    ]
        
        