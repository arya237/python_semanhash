from collections import defaultdict as mymap
from vehicle import vehicle

class Tehran:

    def __init__(self) -> None:
        self.graph = mymap(lambda: mymap(list))
        self.read_from_file()
        
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



tehran = Tehran()

# d = {'A': 1, "B":2, "C":3}

# print(*d.items())

for i in tehran.graph:
    print(i, end=" -> ")
    for j in tehran.graph[i]:
        print(j, end=": ")
        for vec in tehran.graph[i][j]:
            print(vec.get_type_of_vehicle(), end=' ')


            
            



