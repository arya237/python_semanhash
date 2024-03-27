class Time:
    def __init__(self, time: str) -> None:
        self.hour = time[0:2]
        self.min = time[2:4]
    
    def __add__(self, minute) -> None:
        self.min += minute
        self.hour += int(minute / 60)
        self.hour %= 24
        self.min %= 60
    
    def print(self) -> None:
        print(self.hour, ":" , self.min)


        