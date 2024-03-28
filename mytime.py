class Time:
    def __init__(self, time: str) -> None:
        self.hour = int(time[0:2])
        self.min = int(time[3:5])
    
    def get_hour(self) -> int:
        return self.hour
    def get_minute(self) -> int:
        return self.min
    
    def __add__(self, minute) -> None:
        self.min += minute
        self.hour += int(minute / 60)
        self.hour %= 24
        self.min %= 60
    
    def print(self) -> None:
        print(self.hour, ":" , self.min)

   