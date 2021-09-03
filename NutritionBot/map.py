import folium # 匯入 folium 套件
import json

def all_place(path):

    coordinates = []
    names = []
    addrs = []

    # fmap = fm.Map(location=location, zoom_start=15)

    with open(path, 'r', encoding='utf-8') as f:
        all_fitness = json.load(f) # taipei_fitness type :dict

    all_fitness_list = all_fitness['features']

    for mark in all_fitness_list:
        mark['geometry']['coordinates'].reverse()
        coordinates.append(mark['geometry']['coordinates'])

    for name in all_fitness_list:
        if name["properties"]["name"]:
            names.append(name["properties"]["name"])
        else:
            names.append("NULL")

    for addr in all_fitness_list:
        if addr["properties"]["addr:full"]:
            addrs.append(addr["properties"]["addr:full"])
        else:
            addrs.append("NULL")

    return coordinates, names, addrs


def find_nearest_place(location, path):
    """
    location: self_location, type: list
    """
    distance = []

    coordinates, names, addrs = all_place(path)

    for coord in coordinates:
        dist = ((coord[0] - location[0]) ** 2 + (coord[1] - location[1]) ** 2) ** (1 / 2)
        distance.append(dist)

    min_distamce_km = min(distance) * (111)
    min_distamce_km_index = distance.index(min(distance))

    fmap = folium.Map(location=location, zoom_start=15)

    tooltip = '請點選我檢視該點資訊'

    m1 = folium.Marker(location=location,
                       popup=folium.Popup('<b>目前所在地</b>', max_width=400),
                       tooltip = tooltip)

    m2 = folium.Marker(location=coordinates[min_distamce_km_index],
                       popup=folium.Popup('與目前所在地最近的運動場所<br>{}<br>距離約 {:.3f} km<br>地址：{}'.format(names[min_distamce_km_index], min_distamce_km, addrs[min_distamce_km_index]), max_width=400),
                       icon=folium.Icon(color='red'),
                       tooltip=tooltip)  # Marker顏色

    sending_text = '與目前所在地最近的運動場所\n{}\n距離約 {:.3f} km\n地址：{}'.format(names[min_distamce_km_index], min_distamce_km, addrs[min_distamce_km_index])

    fmap.add_child(child=m1)
    fmap.add_child(child=m2)
    fmap.save("taipei.html")

    return sending_text

