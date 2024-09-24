from datetime import datetime

class Time:
    def __init__():
        pass
    
    def get_current_time(self) -> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("Formatted date and time:", formatted_datetime)