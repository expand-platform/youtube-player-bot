from telebot.states import State, StatesGroup

#! User states


class HometaskStates(StatesGroup):
    pass
    # version_number_prompt = State()
    # version_message_prompt = State()

    # stages = [
    #     version_number_prompt,
    #     version_message_prompt,
    # ]


#! Admin states


# ? /nv: new version
class VersionSequenceStates(StatesGroup):
    version_number_prompt = State()
    version_message_prompt = State()

    stages = [
        version_number_prompt,
        version_message_prompt,
    ]


# ? / uu: update user
class UpdateUserSequenceStates(StatesGroup):
    select_user = State()
    select_property = State()
    new_value_prompt = State()

    stages = [
        select_user,
        select_property,
        new_value_prompt,
    ]


# ? /su: see use
class SeeUserSequenceStates(StatesGroup):
    su_select_user = State()

    stages = [su_select_user]


# ? /be: bulk editor
class BulkEditorStates(StatesGroup):
    be_select_user_type = State()
    be_select_user_property = State()
    be_enter_new_value = State()

    stages = [be_select_user_type, be_select_user_property, be_enter_new_value]


# ? /ru: remove user
class RemoveUserStates(StatesGroup):
    select_user = State()

    stages = [
        select_user,
    ]


# ? /ru: remove user
class AdminPaymentStates(StatesGroup):
    select_user = State()

    stages = [
        select_user,
    ]

# ? /sched: change schedule
class AdminScheduleStates(StatesGroup):
    select_day = State()
    show_schedule_hint = State()
    input_new_schedule = State()

    stages = [
        select_day,
        show_schedule_hint,
        input_new_schedule
    ]
