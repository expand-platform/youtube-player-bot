from typing import TypedDict

class UserT(TypedDict):
    real_name: str
    
    first_name: str 
    username: str
    
    user_id: int
    chat_id: int

    access_level: str

    joined_at: str
    
    payment_amount: int
    payment_status: bool
    
    max_lessons: int
    done_lessons: int
    lessons_left: int
    
    stats: dict
    
