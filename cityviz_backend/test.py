import numpy as np
from sklearn.metrics import confusion_matrix
from tqdm import tqdm
from sklearn.manifold import TSNE
import csv
import random
# import matplotlib.pyplot as plt

# # 使用t-SNE进行降维
# embeddings = np.genfromtxt("./data/test_embeds.txt")
# perplexity = 20
# tsne = TSNE(n_components=2, verbose=1, perplexity=perplexity, n_iter=300)
# tsne_results = tsne.fit_transform(embeddings[:30000])
# np.savetxt('./test_embeds_tsne.txt', tsne_results)
# tsne_results.

# labels_num = [2, 8, 22, 4102, 4096]
# a = sum(labels_num)


# tsne_res = np.genfromtxt("./test_embeds_tsne.txt")
# print(tsne_res.shape)
# print(np.min(tsne_res[:, 0]))
# print(np.min(tsne_res[:, 1]))
# print(np.max(tsne_res[:, 0]))
# print(np.max(tsne_res[:, 1]))


# 保存混淆矩阵
def save_cul_groups_conf_matrix():
    complete_city_list = ['Amsterdam', 'Athens', 'Atlanta', 'Auckland', 'Bangalore',
        'Bangkok', 'Barcelona', 'Beijing', 'Berlin', 'Bogota', 'Boston',
        'Brisbane', 'Brussels', 'Bucharest', 'Budapest', 'BuenosAires',
        'Chengdu', 'Chicago', 'Copenhagen', 'Dallas', 'Denver', 'Dubai',
        'Dublin', 'Frankfurt', 'Geneva', 'Guangzhou', 'Hamburg',
        'Hongkong', 'Houston', 'Istanbul', 'Jakarta', 'Johannesburg',
        'KualaLumpur', 'Lima', 'Lisbon', 'London', 'LosAngeles',
        'Luxembourg', 'Madrid', 'Manila', 'Melbourne', 'MexicoCity',
        'Miami', 'Milan', 'Montreal', 'Moscow', 'Mumbai', 'Munich',
        'Nairobi', 'NewDelhi', 'NewYork', 'Norway', 'Paris', 'Perth',
        'Prague', 'Rome', 'SanFrancisco', 'SanPaulo', 'Santiago', 'Sydney',
        'Seoul', 'Shanghai', 'Shenzhen', 'Singapore', 'Stockholm',
        'Taipei', 'Tel Aviv', 'Tianjin', 'Tokyo', 'Toronto', 'Vancouver',
        'Vienna', 'Warsaw', 'Washington', 'Zurich']

    #文化圈分类
    Germanic_Europe = ['Hamburg', 'Berlin', 'Luxembourg', 'Amsterdam', 'Zurich', 'Frankfurt', 'Munich', 'Vienna']
    Latin_America = ['Lima', 'SanPaulo', 'Bogota', 'Santiago', 'MexicoCity', 'BuenosAires']
    Confucian_Asia = ['Shenzhen', 'Shanghai', 'Guangzhou', 'Beijing', 'Tokyo', 'Hongkong', 'Singapore', 'Taipei', 'Tianjin','Seoul', 'Chengdu']
    Anglo = ['Auckland', 'Johannesburg', 'SanFrancisco', 'Dallas', 'Vancouver', 'Houston', 'NewYork', 'Melbourne', 'Montreal', 'Washington', 'Chicago', 'Dublin', 'Miami', 'Boston', 'Toronto', 'LosAngeles', 'London', 'Denver', 'Atlanta', 'Perth', 'Brisbane', 'Sydney']
    Sub_Sahara_Africa = ['Nairobi']
    Southern_Asia = ['Mumbai', 'Jakarta', 'KualaLumpur', 'Bangalore', 'Bangkok', 'Manila', 'NewDelhi']
    Latin_Europe = ['Paris', 'Madrid', 'Geneva', 'Barcelona', 'Milan', 'Rome', 'Lisbon', 'Brussels', 'Tel Aviv']
    Eastern_Europe = ['Athens', 'Budapest', 'Bucharest', 'Moscow', 'Warsaw', 'Prague']
    Nordic_Europe = ['Norway', 'Copenhagen', 'Stockholm']
    Arab = ['Istanbul', 'Dubai']

    culture_group = [Germanic_Europe, Latin_America, Confucian_Asia, Anglo, Sub_Sahara_Africa, Southern_Asia, Latin_Europe, Eastern_Europe, Nordic_Europe, Arab]
    culture_group_labels = ['Germanic_Europe', 'Latin_America', 'Confucian_Asia', 'Anglo', 'Sub_Sahara_Africa', 'Southern_Asia', 'Latin_Europe', 'Eastern_Europe', 'Nordic_Europe', 'Arab']

    culture_group = [Germanic_Europe, Latin_America, Confucian_Asia, Anglo, Sub_Sahara_Africa, Southern_Asia, Latin_Europe, Eastern_Europe, Nordic_Europe, Arab]
    culture_group_labels = ['Germanic_Europe', 'Latin_America', 'Confucian_Asia', 'Anglo', 'Sub_Sahara_Africa', 'Southern_Asia', 'Latin_Europe', 'Eastern_Europe', 'Nordic_Europe', 'Arab']

    # 创建一个从类索引到文化组标签的映射
    index_to_culture_label = {}
    for group_idx, group_cities in enumerate(culture_group):
        for city in group_cities:
            index = complete_city_list.index(city)  # 假设class_names包含所有城市名称
            index_to_culture_label[index] = culture_group_labels[group_idx]

    # 转换原始标签到文化组标签
    test_labels_grouped = []
    test_predictions_grouped = []

    test_res = np.loadtxt('./data/test_preds.txt', delimiter=',', dtype=int)

    for i in tqdm(range(test_res.shape[0])):
        idx = test_res[i, 1]
        if idx in index_to_culture_label.keys() and test_res[i, 0] in index_to_culture_label.keys():
            test_labels_grouped.append(index_to_culture_label[test_res[i,1]])
            test_predictions_grouped.append(index_to_culture_label[test_res[i, 0]])

            
    # test_labels_grouped = [index_to_culture_label[idx] for idx in test_labels if idx in index_to_culture_label.keys()]
    # test_predictions_grouped = [index_to_culture_label[idx] for idx in test_predictions if idx in index_to_culture_label.keys()]

    # 计算文化组标签的混淆矩阵
    conf_matrix_grouped = confusion_matrix(test_labels_grouped, test_predictions_grouped, normalize='true')

    np.savetxt('./data/cul_groups_normalized_conf_matrix.npy', conf_matrix_grouped)

def save_cities_conf_matrix():
    test_res = np.loadtxt('./data/test_preds.txt', delimiter=',', dtype=int)
    conf_matrix = confusion_matrix(test_res[:, 1], test_res[:, 0])
    np.savetxt('./data/cities_conf_matrix.npy', conf_matrix)

def compute_cities_tsne_pos():
    test_res = np.loadtxt('./data/cities_conf_matrix.txt', dtype=int)
    perplexity = 20
    tsne = TSNE(n_components=2, verbose=1, perplexity=perplexity, n_iter=300)
    tsne_results = tsne.fit_transform(test_res)
    np.savetxt('./data/cities_tsne_pos.txt', tsne_results)

    max_val = np.max(np.abs(tsne_results))
    normalized_tsne_results = tsne_results/max_val
    np.savetxt('./data/normalized_cities_tsne_pos.txt', normalized_tsne_results)


# compute_cities_tsne_pos()
import colorsys
import re
def parse_rgb_color(rgb_str):
    """
    从 RGB 颜色字符串中解析出红绿蓝三个通道的值。
    
    参数:
    rgb_str (str): RGB 颜色字符串,格式为 "rgb(r, g, b)" 或 "#rrggbb"
    
    返回:
    (float, float, float): 对应的 RGB 颜色值 (0.0 - 1.0)
    """
    # 尝试解析 "rgb(r, g, b)" 格式
    match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', rgb_str)
    if match:
        r, g, b = [int(x) / 255.0 for x in match.groups()]
        return r, g, b
    
    # 尝试解析 "#rrggbb" 格式
    match = re.match(r'#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', rgb_str)
    if match:
        r, g, b = [int(x, 16) / 255.0 for x in match.groups()]
        return r, g, b
    
    # 如果都不匹配,返回 None
    return None

def rgb_to_hsl(r, g, b):
    """
    将 RGB 颜色转换为 HSL 颜色。
    
    参数:
    r (float): 红色通道的值 (0.0 - 1.0)
    g (float): 绿色通道的值 (0.0 - 1.0)
    b (float): 蓝色通道的值 (0.0 - 1.0)
    
    返回:
    (float, float, float): 对应的 HSL 颜色值 (色相, 饱和度, 亮度)
    """
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h, s, l

def convert_color2hsl():
    with open('./data/cities_colors_new.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter="\t")
        data = list(reader)
    new_data = []
    for city_color in data:
        now_city = city_color["city"]
        r,g,b = parse_rgb_color(city_color["color"])
        h,s,l = rgb_to_hsl(r, g, b)
        new_data.append({
            "city": now_city,
            "h": h*360,
            "s": s*100,
            "l": l*100,
            "a": 1
        })

    # 将 dict list 保存为 CSV 文件
    with open('./data/cities_hsla_colors.csv', 'w', newline='') as csvfile:
        # 创建 CSV 写入器,并指定列名
        fieldnames = ['city', 'h', 's', 'l', 'a']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # 写入表头
        writer.writeheader()

        # 写入数据行
        for row in new_data:
            writer.writerow(row)

def gen_rand_list():
    # 创建一个示例列表
    data = [i for i in range(181731)]

    # 打乱列表顺序
    random.shuffle(data)

    # 将打乱顺序的列表保存到 CSV 文件
    with open('./data/rand_sel.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

    print("数据已保存到 output.csv 文件中.")


convert_color2hsl()