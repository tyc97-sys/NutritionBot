import folium # 匯入 folium 套件
import json

# path = r'F:\AI\Line_Chatbot\NutritionBot\restaurant.geojson'
# coordinates = []
# with open(path, 'r', encoding='utf-8') as f:
#     all_healthy_box = json.load(f)  # taipei_fitness type :dict
#     # print(all_healthy_box)
#
# all_healthy_box_list = all_healthy_box['features']
#
# for mark in all_healthy_box_list:
#     mark['geometry']['coordinates'].reverse()
#     coordinates.append(mark['geometry']['coordinates'])

def all_restaurant(path):

    coordinates = []
    names = []
    addrs = []
    phones = []

    # fmap = fm.Map(location=location, zoom_start=15)

    with open(path, 'r', encoding='utf-8') as f:
        all_healthy_box = json.load(f) # taipei_fitness type :dict

    all_healthy_box_list = all_healthy_box['features']

    for mark in all_healthy_box_list:
        mark['geometry']['coordinates'].reverse()
        coordinates.append(mark['geometry']['coordinates'])

    for name in all_healthy_box_list:
        names.append(name["properties"]["name"])

    for addr in all_healthy_box_list:
        addrs.append(addr["properties"]["addr:full"])

    for phone in all_healthy_box_list:
        phones.append(phone["properties"]["phone"])

    return coordinates, names, addrs, phones

def find_nearest_restaurant(location, path):
    """
        location: self_location, type: list
    """

    coordinates, names, addrs, phones = all_restaurant(path)

    distance = []

    for coord in coordinates:
        dist = ((coord[0] - location[0]) ** 2 + (coord[1] - location[1]) ** 2) ** (1 / 2)
        distance.append(dist)

    nearest_healthy_box = sorted(distance)
    nearest_healthy_box_list = []
    index_ = []
    # 找最近的三個健康餐盒
    for i in range(3):
        nearest_healthy_box_list.append(nearest_healthy_box[i] * 111)
        index_.append(distance.index(nearest_healthy_box[i]))


    sending_text1 = '與目前所在地最近的健康餐盒販賣地：\n{}\n距離約 {:.3f} km\n地址：{}\n電話：{}'\
        .format(names[index_[0]], nearest_healthy_box_list[0], addrs[index_[0]], phones[index_[0]])
    sending_text2 = '與目前所在地最近的健康餐盒販賣地：\n{}\n距離約 {:.3f} km\n地址：{}\n電話：{}' \
        .format(names[index_[1]], nearest_healthy_box_list[1], addrs[index_[1]], phones[index_[1]])
    sending_text3= '與目前所在地最近的健康餐盒販賣地：\n{}\n距離約 {:.3f} km\n地址：{}\n電話：{}' \
        .format(names[index_[2]], nearest_healthy_box_list[2], addrs[index_[2]], phones[index_[2]])

    return sending_text1, sending_text2, sending_text3
    # return sending_text, addrs[min_distamce_km_index], names[min_distamce_km_index], coordinates[min_distamce_km_index]

# path = r'F:\AI\Line_Chatbot\NutritionBot\restaurant.geojson'
#
# coordinates, names, addrs, phones = all_place(path)
# # print(phones)
# print('names: {}, addr: {}, phone: {}, coor:{}'.format(names[0], addrs[0], phones[0], coordinates[0]))
# for i in range(len(addrs)):
#     print('names: {}, addr: {}, phone: {}, coor:{}'.format(names[i], addrs[i], phones[i], coordinates[i]))