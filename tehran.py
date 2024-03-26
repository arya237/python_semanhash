from collections import defaultdict as mymap
from vehicle import vehicle


class node:
    value = float('inf')
    direction = []
    type_vehicle = []

class mylist(list[vehicle]):

    def get_min(self) -> vehicle:
        minimum = vehicle()
        minimum.set_value(float('inf'))
        for i in self:
            if i.get_value() < minimum.get_value():
                minimum = i
        return minimum


class Tehran:

    def __init__(self) -> None:
        self.graph = mymap(lambda: mymap(mylist))
        self.lines = mymap(list[str])
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

        file = open("taxi_bus_distance.txt", "r")
        
        line = file.readline().strip('\n')

        while True:
            start = file.readline().rstrip('\n')

            if start == 'end*':
                break

            if start == 'end':
               line = file.readline().strip('\n')
               start = file.readline().rstrip('\n')

            destination = file.readline().rstrip('\n')
            value = file.readline().rstrip('\n')

            if line[0] == 'M':
                Vehicle1 = vehicle(value, "metro", line)
                Vehicle2 = vehicle(value, "taxi", line)

                self.graph[start][destination].append(Vehicle1)
                self.graph[start][destination].append(Vehicle2)

                self.graph[destination][start].append(Vehicle1)
                self.graph[destination][start].append(Vehicle2)
            
            elif line[0] == "B":
                Vehicle1 = vehicle(value, 'Bus', line)
                
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

                    
        print(pathes[destiny].value, end=":\n")
        print(pathes[destiny].direction[0], end=" -> ")

        for i in range(1, len(pathes[destiny].direction)):
            print(" ( " ,pathes[destiny].type_vehicle[i - 1], " ) ", pathes[destiny].direction[i], end=" -> ")
                    
                      






tehran = Tehran()
src = input()
destiny = input()
tehran.find_shortest_path(src, destiny)

# d = {'A': 1, "B":2, "C":3}

# print(*d.items())

# for i in tehran.graph:
#     print(i, end=" -> ")
#     for j in tehran.graph[i]:
#         print(j, end=": ")
#         for vec in tehran.graph[i][j]:
#             print(vec.get_type_of_vehicle(), end=' ')


            
            



