from telebot.states import State, StatesGroup


class UserStates(StatesGroup):
    # chapter 1: Introduction 
    language_selection = State()
    name_prompt = State()
    campaign_details = State()
    first_search_agreement = State()
    start_first_search = State()
    
    # chapter 2: First friend suggestion (+ help in each step) 
    friend_suggestion = State()
    friend_name_input = State()


    # chapter 3: Help with search (education) 
    education_start = State()
    occupation_options = State()
    # ну и так далее, 3.2, 3.3