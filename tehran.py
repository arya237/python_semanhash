from collections import defaultdict as mymap
from vehicle import vehicle
from copy import copy, deepcopy
from mytime import Time


class node:
    value = float('inf')
    direction = []
    type_vehicle = []
    line = []

class mylist(list[vehicle]):

    def get_min(self) -> vehicle:
        minimum = vehicle()
        minimum.set_value(float('inf'))
        for i in self:
            if i.get_value() < minimum.get_value():
                minimum = i
        return minimum
    
    def get_vic(self, vehicle: str) -> vehicle:
        # print(vehicle, end=': ')
        for i in self:
            if i.get_type_of_vehicle() == vehicle:
                # print("finded")
                return i
    
    def calc_price(self, vehicle: str, flag: bool) -> int:
        if flag == 1:
            if vehicle == 'metro':
                return 3267
            elif vehicle == 'taxi':
                return 6000
            elif vehicle == 'bus':
                return 2250
        else: return 0
    
    def calc_time(self, vehicle: str, flag: bool, time: Time):
        t = 2  if  18 < time.get_hour() < 20 else 1
        m = 24 if  6  < time.get_hour() < 8  else 8
        b = 2  if  6  < time.get_hour() < 8  else 1
       
        if vehicle == "taxi" and flag == 0:
            # print(self.get_min(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value() * (2*t)
        
        elif vehicle == "taxi" and flag == 1:
            # print(self.get_vic(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value() *(2*t) + (5*t)
        
        elif vehicle == "metro" and flag == 0:
            # print(self.get_vic(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value()
        
        elif vehicle == "metro" and flag == 1:
            # print(self.get_vic(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value() + m
        
        elif vehicle == "bus" and flag == 0:
            # print(self.get_vic(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value() * (4*b)
        
        elif vehicle == "bus" and flag == 1:
            # print(self.get_vic(vehicle).get_type_of_vehicle())
            return self.get_vic(vehicle).get_value() * (4*b) + (15*b)
        





class Tehran:

    def __init__(self) -> None:
        self.graph = mymap(lambda: mymap(mylist))
        self.lines = mymap(list[str])
        self.station_info = mymap(lambda: mymap(mylist[str]))
        self.read_from_file()
        

    def find_minimum(self, list: mymap, visited: list) -> str:
        min = float('inf')
        min_name = ""  
        for key, Value in list.items():
            if (key not in visited) and Value.value < min:
                min = list[key].value
                min_name = key
        return min_name
            
    def read_from_file(self) -> None:
        start = ""
        destination = ""
        line = ""
        value: int
        flag: bool = 1

        file = open("taxi_bus_distance.txt", "r")
        
        line = file.readline().strip('\n')

        while True:
            start = file.readline().rstrip('\n')
            
            if flag:
                self.lines[line].append(start)
        
                flag = 0
                if line[0] == "M":
                    self.station_info[start][line].append("metro")
                    self.station_info[start][line].append("taxi")
                elif line[0] == "B":
                    self.station_info[start][line].append("bus")

            if start == 'end*':
                break

            if start == 'end':
                line = file.readline().strip('\n')
                start = file.readline().rstrip('\n')

                if line[0] == "M":
                    self.station_info[start][line].append("metro")
                    self.station_info[start][line].append("taxi")
                elif line[0] == "B":
                    self.station_info[start][line].append("bus")

                self.lines[line].append(start)

            destination = file.readline().rstrip('\n')
            value = file.readline().rstrip('\n')
            self.lines[line].append(destination)

            if line[0] == 'M':
                Vehicle1 = vehicle(value, "metro", line)
                Vehicle2 = vehicle(value, "taxi", line)

                self.station_info[destination][line].append("metro")
                self.station_info[destination][line].append("taxi")

                self.graph[start][destination].append(Vehicle1)
                self.graph[start][destination].append(Vehicle2)

                self.graph[destination][start].append(Vehicle1)
                self.graph[destination][start].append(Vehicle2)
            
            elif line[0] == "B":
                Vehicle1 = vehicle(value, 'bus', line)
                
                self.station_info[destination][line].append("bus")
                self.graph[start][destination].append(Vehicle1)
                self.graph[destination][start].append(Vehicle1)
        
    def find_shortest_path(self, start: str, destiny: str) -> None:
        pathes = mymap(lambda: node())
        visited: list[str] = []
        
        pathes[start].value = 0
        pathes[start].direction.append(start)
        

        for i in range(0, len(self.graph)):
            
            min_state = self.find_minimum(pathes, visited)
            visited.append(min_state)

            for key, value in self.graph[min_state].items():
                if (key not in visited and int(pathes[min_state].value) != float('inf') 
                    and int(pathes[min_state].value) + int(value.get_min().value) < float(pathes[key].value)):
                    pathes[key].value = int(pathes[min_state].value) + int(value.get_min().value)
                    pathes[key].direction = pathes[min_state].direction.copy()
                    pathes[key].direction.append(key)
                    pathes[key].type_vehicle = pathes[min_state].type_vehicle.copy()
                    pathes[key].type_vehicle.append(value.get_min().get_type_of_vehicle())
                    pathes[key].line = pathes[min_state].line.copy()
                    pathes[key].line.append(value.get_min().get_line())

                    
        print(pathes[destiny].value, end=":\n")
        print(self.calc_arrive_time(pathes[destiny]))
        print(pathes[destiny].direction[0], end=" -> ")

        for i in range(1, len(pathes[destiny].direction)):
            print(" ( " ,pathes[destiny].type_vehicle[i - 1], " ) ", pathes[destiny].direction[i], end=" -> ")

    
    def find_best_cost(self, src: str, destiny: str):
        pathes = mymap(lambda: node())
        visited = []

        pathes[src].value = 0
        # pathes[src].direction.append(src)  #check later!!!!!!! mirdamad is in every node!


        for i in range(0, len(self.graph)):
            min = self.find_minimum(pathes, visited)
            self.set_price_in_stations(self.station_info[min], min, pathes, visited)
            visited.append(min)
        
        print(pathes[destiny].value)
        print(self.calc_arrive_time(pathes[destiny]))
        print(pathes[destiny].direction[0], end=' -> ')

        for i in range(1, len(pathes[destiny].direction)):
            print('(',pathes[destiny].type_vehicle[i - 1], ')', pathes[destiny].direction[i], end=' -> ')

        # print(len(pathes[destiny].direction))
        # print(len(pathes[destiny].type_vehicle))
        # for i in pathes[destiny].direction:
        #     print(i)
        

    
    def set_price_in_stations(self, vehicles: mymap, src: str, list: mymap[str, node], visited) -> None:
        
        for line, value in vehicles.items():
            for Vehicle in value:
                
                index_src = self.lines[line].index(src)
                
                resault = node()
                resault.value = copy(list[src].value)
                resault.direction = copy(list[src].direction)
                resault.type_vehicle = copy(list[src].type_vehicle)
                resault.line = copy(list[src].line)

                flag: bool = 1

                for i in range(index_src, len(self.lines[line]) - 1):
                    
                    if src == self.lines[line][i]:
                        
                        if len(list[src].type_vehicle) == 0:
                            flag = 1
                        elif list[src].type_vehicle[-1] != Vehicle:
                            flag = 1
                        elif list[src].line[-1] != line:
                            flag = 1
                    
                    resault.value += self.graph[self.lines[line][i]][self.lines[line][i + 1]].calc_price(Vehicle, flag)
                    resault.direction.append(self.lines[line][i + 1])
                    resault.type_vehicle.append(Vehicle)
                    resault.line.append(line)
                    flag = 0

                    if list[self.lines[line][i + 1]].value >= resault.value:
                        list[self.lines[line][i + 1]].value = copy(resault.value)
                        list[self.lines[line][i + 1]].direction = copy(resault.direction)
                        list[self.lines[line][i + 1]].type_vehicle = copy(resault.type_vehicle)
                        list[self.lines[line][i + 1]].line = copy(resault.line)
                
                resault.value = copy(list[src].value)
                resault.direction = copy(list[src].direction)
                resault.type_vehicle = copy(list[src].type_vehicle)
                resault.line = copy(list[src].line)
                flag: bool = 1 

                for i in range(index_src, 0, -1):
                    if list[self.lines[line][i - 1]] not in visited:
                        
                        if src == self.lines[line][i]:
                        
                            if len(list[src].type_vehicle) == 0:
                                flag = 1
                            elif list[src].type_vehicle[-1] != Vehicle:
                                flag = 1
                            elif list[src].line[-1] != line:
                                flag = 1

                    resault.value += self.graph[self.lines[line][i]][self.lines[line][i - 1]].calc_price(Vehicle, flag)
                    resault.direction.append(self.lines[line][i - 1])
                    resault.type_vehicle.append(Vehicle)
                    resault.line.append(line)
                    flag = 0

                    if list[self.lines[line][i - 1]].value >= resault.value:
                        list[self.lines[line][i - 1]].value = copy(resault.value)
                        list[self.lines[line][i - 1]].direction = copy(resault.direction)
                        list[self.lines[line][i - 1]].type_vehicle = copy(resault.type_vehicle)
                        list[self.lines[line][i - 1]].line = copy(resault.line)
    
    def find_best_time(self, src, destiny):
        pathes = mymap(lambda: node())
        visited = []
        
        pathes[src].value = 0
        pathes[src].direction.append(src)
        time = Time("10:00")

        for i in range(0, len(self.graph)):
            min = self.find_minimum(pathes, visited)
            self.set_time_in_stations(self.station_info[min], min, pathes, visited, time)
            visited.append(min)
        
        print(pathes[destiny].value)
    
    def set_time_in_stations(self, vehicles: mymap, src: str, list: mymap[str, node], visited, start_time: Time) -> None:
        
        for line, value in vehicles.items():
            for Vehicle in value:

                resault = node()
                resault.value = copy(list[src].value)
                resault.direction = copy(list[src].direction)
                resault.type_vehicle = copy(list[src].type_vehicle)
                resault.line = copy(list[src].line)
                
                flag: bool = 1
                src_index = self.lines[line].index(src)

                for i in range(src_index, len(self.lines[line]) - 1):
                    
                    if src == self.lines[line][i]:
                        
                        if len(list[src].type_vehicle) == 0:
                            flag = 1
                        elif list[src].type_vehicle[-1] != Vehicle:
                            flag = 1
                        elif list[src].line[-1] != line:
                            flag = 1

                    temp = copy(start_time)
                    temp.__add__(resault.value)
                    # print("src: ", self.lines[line][i], " -> ", self.lines[line][i + 1] ) 
                    resault.value += self.graph[self.lines[line][i]][self.lines[line][i + 1]].calc_time(Vehicle, flag, temp)
                    resault.direction.append(self.lines[line][i + 1])
                    resault.type_vehicle.append(Vehicle)
                    resault.line.append(line)
                    flag = 0

                    if list[self.lines[line][i + 1]].value >= resault.value:
                        list[self.lines[line][i + 1]].value = copy(resault.value)
                        list[self.lines[line][i + 1]].direction = copy(resault.direction)
                        list[self.lines[line][i + 1]].type_vehicle = copy(resault.type_vehicle)
                        list[self.lines[line][i + 1]].line = copy(resault.line)


                resault.value = copy(list[src].value)
                resault.direction = copy(list[src].direction)
                resault.type_vehicle = copy(list[src].type_vehicle)
                resault.line = copy(list[src].line)
                flag: bool = 1 

                for i in range(src_index, 0, -1):
                    if list[self.lines[line][i - 1]] not in visited:
                        
                        if src == self.lines[line][i]:
                        
                            if len(list[src].type_vehicle) == 0:
                                flag = 1
                            elif list[src].type_vehicle[-1] != Vehicle:
                                flag = 1
                            elif list[src].line[-1] != line:
                                flag = 1

                    temp = copy(start_time)
                    temp.__add__(resault.value)
                    resault.value += self.graph[self.lines[line][i]][self.lines[line][i - 1]].calc_time(Vehicle, flag, temp)
                    resault.direction.append(self.lines[line][i - 1])
                    resault.type_vehicle.append(Vehicle)
                    resault.line.append(line)
                    flag = 0

                    if list[self.lines[line][i - 1]].value >= resault.value:
                        list[self.lines[line][i - 1]].value = copy(resault.value)
                        list[self.lines[line][i - 1]].direction = copy(resault.direction)
                        list[self.lines[line][i - 1]].type_vehicle = copy(resault.type_vehicle)
                        list[self.lines[line][i - 1]].line = copy(resault.line)
    
    def calc_arrive_time(self, destiny: node) -> int:
        minute: int = 0
        b = 15
        t = 5
        m = 8
        time = Time("10:00")
        flag: bool = 1
        
        for i in range(0, len(destiny.direction) - 1):

            if i == 0 or (destiny.type_vehicle[i] != destiny.type_vehicle[i - 1]) or (destiny.line[i] != destiny.line[i - 1]):
                flag = 1

            minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].calc_time(destiny.type_vehicle[i], flag, time)
            flag = 0
            # print(minute)
            #     if destiny.type_vehicle[i] == 'bus':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value() *(4) + b
            #     elif destiny.type_vehicle[i] == 'metro':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value() + m
            #     elif destiny.type_vehicle[i] == 'taxi':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value() *(2) + t

            #     flag = 0

            # else:
            #     if (destiny.type_vehicle[i] != destiny.type_vehicle[i - 1]) and destiny.type_vehicle[i] == 'bus':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value()*(4) + b

            #     elif (destiny.type_vehicle[i] != destiny.type_vehicle[i - 1]) and destiny.type_vehicle[i] == 'metro':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value() + m

            #     elif destiny.type_vehicle[i] == 'metro':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value()
                
            #     elif destiny.type_vehicle[i] == 'bus':
            #         minute += self.graph[destiny.direction[i]][destiny.direction[i + 1]].get_vic(destiny.type_vehicle[i]).get_value() *(4)

        
        return minute

                    



                        
tehran = Tehran()
src = input()
destiny = input()
tehran.find_shortest_path(src, destiny)
print("\n*************\n")
tehran.find_best_cost(src, destiny)
# print("\n*************\n")
# tehran.find_best_time(src, destiny)
# print(tehran.graph["Mirdamad"]["Meydan-e Hazrat-e ValiAsr"].get_min())
                        
# def func(a, b):
#     print(a+b+c)

# def func(a, b, c):
#     print(a, b, c)

# func(2,3)




            
            



