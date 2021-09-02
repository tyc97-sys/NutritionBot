import folium # 匯入 folium 套件
import json

def all_centre(path):

    fitness_coordinates = []

    # fmap = fm.Map(location=location, zoom_start=15)

    with open(path, 'r', encoding='utf-8') as f:
        all_fitness = json.load(f) # taipei_fitness type :dict

    all_fitness_list = all_fitness['features']

    for mark in all_fitness_list:
        mark['geometry']['coordinates'].reverse()
        fitness_coordinates.append(mark['geometry']['coordinates'])

    return fitness_coordinates


def find_nearest_centre(location, path):
    """
    location: self_location, type: list
    """
    distance = []

    fitness_coordinates = all_centre(path)

    for coord in fitness_coordinates:
        dist = ((coord[0] - location[0]) ** 2 + (coord[1] - location[1]) ** 2) ** (1 / 2)
        distance.append(dist)

    min_distamce_km = min(distance) * (111)
    min_distamce_km_index = distance.index(min(distance))

    fmap = folium.Map(location=location, zoom_start=15)

    tooltip = '請點選我檢視該點資訊'

    m1 = folium.Marker(location=location,
                       popup=folium.Popup('<b>目前所在地</b>', max_width=400))

    m2 = folium.Marker(location=fitness_coordinates[min_distamce_km_index],
                       popup=folium.Popup('與目前所在地最近的運動場所<br>距離約 {:.3f} km'.format(min_distamce_km), max_width=400),
                       icon=folium.Icon(color='red'))  # Marker顏色

    fmap.add_child(child=m1)
    fmap.add_child(child=m2)
    fmap.save("taipei_fitness.html")

