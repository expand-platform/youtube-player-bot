from typing import TypedDict

class UserT(TypedDict):
    first_name: str 
    username: str
    
    user_id: int
    chat_id: int

    access_level: str
    language: str

    joined_at: str
    

class GuestT(UserT):
    pass

    
class AdminT(UserT):
    real_name: str
    last_name: str
    
    language: str
    
    joined_at: str


class StudentT(UserT):
    real_name: str
    last_name: str
    
    language: str
    
    payment_amount: int
    payment_status: bool
    
    max_lessons: int
    done_lessons: int
    lessons_left: int
    
    stats: dict
    
