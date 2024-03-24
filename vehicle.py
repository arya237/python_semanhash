import sys

class vehicle:
    def __init__(self, value:int = sys.maxsize, name:str = "", line:str = "") -> None:
        self.set_name_of_vehicle(name)
        self.set_line(line)
        self.set_value(value)

    def set_value (self, value:int) -> None:
        self.value = value
    def set_name_of_vehicle(self, name:str) -> None:
        self.vehicle_name = name
    def set_line(self, line:str) -> None:
        self.line = line
    def get_value(self) -> int:
        return self.value
    def get_line(self) -> str:
        return self.line
    def get_type_of_vehicle(self) -> str:
        return self.vehicle_name



