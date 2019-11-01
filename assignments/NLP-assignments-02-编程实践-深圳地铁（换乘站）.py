import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

SZSubwayInfo = {}
Line = []
ST = []

class subway(object):
    def __init__(self):
        self.url = 'http://map.amap.com/service/subway?_1572416772530&srhdata=4403_drw_shenzhen.json'

    def get_page(self):
        response = requests.get(self.url)
        content = response.text
        info = json.loads(content)
        return info

    def write_data(self):
        for line in self.get_page()['l']:
            with open('subway.txt', 'a', encoding='utf8') as f:
                #print(line['ln'])
                f.write(line['ln'] +': ')
            for lineinfo in line['st']:
                with open('subway.txt', 'a', encoding='utf8') as f:
                    #print(lineinfo['n'])
                    f.write(lineinfo['n'] + ' ')
            with open('subway.txt', 'a', encoding='utf8') as f:
                f.write('\n')
        f.close()

    def parse_data(self):
        for line in self.get_page()['l']:
            Line.append(line['ln'])
            stations = []
            for lineinfo in line['st']:
                if lineinfo['n'] in stations:
                    continue
                else:
                    stations.append(lineinfo['n'])
            ST.append(stations)
        for i in range(len(ST)):
            SZSubwayInfo[Line[i]] = ST[i]
        #print(SZSubwayInfo)

    def build_station_connection(self):
        station_connection = defaultdict(list)
        #print(type(station_connection))
        for i in range(len(ST)):
            for station1 in ST[i]:
                idx = ST[i].index(station1)
                if idx == 0:
                    station_connection[station1].append(ST[i][idx+1])
                elif idx == len(ST[i])-1:
                    station_connection[station1].append(ST[i][idx-1])
                else:
                    station_connection[station1].append(ST[i][idx + 1])
                    station_connection[station1].append(ST[i][idx - 1])

        #print(station_connection)
        return station_connection

    def bfs(self,graph,start,destination):
        pathes = [[start]]
        visited = set()
        #print(visited)

        while pathes:
            path = pathes.pop(0)
            #print('path:')
            #print(path)
            froniter = path[-1]
            #print('froniter:')
            #print(froniter)
            if froniter in visited: continue

            successors = graph[froniter]
            #print('successors:')
            #print(successors)
            for st in successors:
                if st in path: continue
                new_path = path + [st]
                pathes.append(new_path)

                if st == destination:
                    return new_path
                #print('new_path:')
                #print(new_path)
            visited.add(froniter)

if __name__ == '__main__':
    sz_subway = subway()
    sz_subway.get_page()
    sz_subway.write_data()
    sz_subway.parse_data()

#    _search_strategy = sz_subway.sort_by_num_of_transfer_station()
#    sz_subway.bfs_search_agent(graph,'会展中心','沙尾',_search_strategy)
#    sz_subway.bfs_search_agent(graph, '机场', '岗厦北',_search_strategy)
    #print(sz_subway.build_station_connection())
    print(sz_subway.bfs(sz_subway.build_station_connection(),"市民中心","沙尾"))
    print(sz_subway.bfs(sz_subway.build_station_connection(), "岗厦北", "机场"))