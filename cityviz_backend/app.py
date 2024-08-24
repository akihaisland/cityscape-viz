from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import numpy as np
import csv
from sklearn.manifold import TSNE
import os

app = Flask(__name__)
CORS(app)

data_apth = "./"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    return f'Hello, {name}!'


@app.route('/test')
def test():
    tsne_res = np.genfromtxt("./test_embeds_tsne.txt")[:300, :].tolist()
    return jsonify(tsne_res)

def get_random_sample(vec_len=3000):
    # 读取顺序 CSV 文件
    with open('./data/rand_sel.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        data = [int(row[0]) for row in reader]

    return data[:vec_len]


@app.route('/api/tsneVec')
def req_tsne_res():
    vec_len = request.args.get("vec_len", 3000, int)

    # 线程使用tsne进行计算
    tsne_res_file = f'./data/embeds_tsne_res/{vec_len}.txt'
    # test_a = os.listdir(f'./data/embeds_tsne_res/')
    # test_b = os.getcwd()
    # print("test_b: "+test_b)
    # print(os.path)
    if os.path.exists(tsne_res_file):
        tsne_res = np.genfromtxt(tsne_res_file).tolist()
    else:
        embeddings = np.genfromtxt("./data/test_embeds.txt")
        perplexity = 20
        tsne = TSNE(n_components=2, verbose=1, perplexity=perplexity, n_iter=300)
        tsne_results = tsne.fit_transform(embeddings[get_random_sample(vec_len)])
        tsne_res = tsne_results.tolist()
        np.savetxt(tsne_res_file, tsne_res)

    # tsne_res = np.genfromtxt("./data/test_embeds_tsne.txt")[get_random_sample(vec_len), :].tolist()
    return jsonify(tsne_res)


@app.route('/api/streetScale')
def req_street_scale_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat0.txt")[get_random_sample(vec_len), 1].tolist()
    return jsonify(res)

@app.route('/api/greenery')
def req_greenery_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat0.txt")[get_random_sample(vec_len), 0].tolist()
    return jsonify(res)

@app.route('/api/data_cities')
def req_data_labels():
    vec_len = request.args.get("vec_len", 3000, int)
    # res = np.genfromtxt("./data/test_labels.txt", dtype=int)[get_random_sample(vec_len)].tolist()
    res = np.genfromtxt("./data/test_preds.txt", dtype=int, delimiter=",")[get_random_sample(vec_len), 1].tolist()

    # labels对应的城市列表
    complete_city_list = ['Amsterdam', 'Athens', 'Atlanta', 'Auckland', 'Bangalore',
        'Bangkok', 'Barcelona', 'Beijing', 'Berlin', 'Bogota', 'Boston',
        'Brisbane', 'Brussels', 'Bucharest', 'Budapest', 'Buenos Aires',
        'Chengdu', 'Chicago', 'Copenhagen', 'Dallas', 'Denver', 'Dubai',
        'Dublin', 'Frankfurt', 'Geneva', 'Guangzhou', 'Hamburg',
        'Hong Kong', 'Houston', 'Istanbul', 'Jakarta', 'Johannesburg',
        'Kuala Lumpur', 'Lima', 'Lisbon', 'London', 'Los Angeles',
        'Luxembourg', 'Madrid', 'Manila', 'Melbourne', 'Mexico City',
        'Miami', 'Milan', 'Montreal', 'Moscow', 'Mumbai', 'Munich',
        'Nairobi', 'New Delhi', 'New York', 'Oslo', 'Paris', 'Perth',
        'Prague', 'Rome', 'San Francisco', 'Sao Paulo', 'Santiago', 'Sydney',
        'Seoul', 'Shanghai', 'Shenzhen', 'Singapore', 'Stockholm',
        'Taipei', 'Tel Aviv', 'Tianjin', 'Tokyo', 'Toronto', 'Vancouver',
        'Vienna', 'Warsaw', 'Washington', 'Zurich']
    
    #文化圈分类
    Germanic_Europe = ['Hamburg', 'Berlin', 'Luxembourg', 'Amsterdam', 'Zurich', 'Frankfurt', 'Munich', 'Vienna']
    Latin_America = ['Lima', 'Sao Paulo', 'Bogota', 'Santiago', 'Mexico City', 'Buenos Aires']
    Confucian_Asia = ['Shenzhen', 'Shanghai', 'Guangzhou', 'Beijing', 'Tokyo', 'Hong Kong', 'Singapore', 'Taipei', 'Tianjin','Seoul', 'Chengdu']
    Anglo = ['Auckland', 'Johannesburg', 'San Francisco', 'Dallas', 'Vancouver', 'Houston', 'New York', 'Melbourne', 'Montreal', 'Washington', 'Chicago', 'Dublin', 'Miami', 'Boston', 'Toronto', 'Los Angeles', 'London', 'Denver', 'Atlanta', 'Perth', 'Brisbane', 'Sydney']
    Sub_Sahara_Africa = ['Nairobi']
    Southern_Asia = ['Mumbai', 'Jakarta', 'Kuala Lumpur', 'Bangalore', 'Bangkok', 'Manila', 'New Delhi']
    Latin_Europe = ['Paris', 'Madrid', 'Geneva', 'Barcelona', 'Milan', 'Rome', 'Lisbon', 'Brussels', 'Tel Aviv']
    Eastern_Europe = ['Athens', 'Budapest', 'Bucharest', 'Moscow', 'Warsaw', 'Prague']
    Nordic_Europe = ['Oslo', 'Copenhagen', 'Stockholm']
    Arab = ['Istanbul', 'Dubai']

    culture_group = [Germanic_Europe, Latin_America, Confucian_Asia, Anglo, Sub_Sahara_Africa, Southern_Asia, Latin_Europe, Eastern_Europe, Nordic_Europe, Arab]
    culture_group_labels = ['Germanic Europe', 'Latin America', 'Confucian_Asia', 'Anglo', 'Sub Sahara Africa', 'Southern Asia', 'Latin Europe', 'Eastern Europe', 'Nordic Europe', 'Arab']
    culture_group_cities_idx = []
    city_idx2culture_group = [-1]*len(complete_city_list)
    for i in range(len(culture_group)):
        now_cultural_cities_idx = []
        for j in range(len(culture_group[i])):
            now_city_idx = complete_city_list.index(culture_group[i][j])
            now_cultural_cities_idx.append(now_city_idx)
            city_idx2culture_group[now_city_idx] = i
        culture_group_cities_idx.append(now_cultural_cities_idx)

    idx2culture_group = []
    for city_idx in res:
        idx2culture_group.append(city_idx2culture_group[city_idx])

    

    return jsonify({
        "idx2city": res, # 每个数据的城市编号
        "idx2culture_group": idx2culture_group, # 每个数据的文化圈编号
        "cities_in_culture_groups": culture_group_cities_idx, # 每个文化圈所含的城市编号
        "cities_name": complete_city_list, # 每个城市编号代表的城市名称
        "culture_groups_names": culture_group_labels, # 每个城市编号代表的文化圈名称
    })


@app.route('/api/normalized_conf_matrix')
def req_normalized_conf_matrix():
    """请求混淆矩阵"""
    city_matrix = np.genfromtxt("./data/cities_normalized_conf_matrix.txt").tolist()
    cul_group_matrix = np.genfromtxt("./data/cul_groups_normalized_conf_matrix.txt").tolist()
    
    return jsonify({
        "city": city_matrix,
        "cul_group": cul_group_matrix
    })


@app.route('/api/cities_pos')
def req_cities_pos():
    """请求城市的位置"""
    # 读取有表头的 CSV 文件
    with open('./data/location.csv', 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    
    return jsonify(data)

@app.route('/api/cities_tsne_pos')
def req_cities_tsne_pos():
    """请求城市tsne的位置"""
    # 读取有表头的 CSV 文件
    cities_pos = np.genfromtxt("./data/normalized_cities_tsne_pos.txt").tolist()
    return jsonify(cities_pos)

@app.route('/api/colors')
def req_data_colors():
    """请求城市tsne的位置"""
    # 读取有表头的 CSV 文件
    with open('./data/cities_hsla_colors.csv', 'r') as file:
        reader = csv.DictReader(file)
        cities_colors = list(reader)
    with open('./data/cul_groups_hsla_colors.csv', 'r') as file:
        reader = csv.DictReader(file)
        cul_group_colors = list(reader)

    for colors in [cities_colors, cul_group_colors]:
        for color_dict in colors:
            for color_d in ["h", "s", "l", "a"]:
                color_dict[color_d] = float(color_dict[color_d])
    
    complete_city_list = ['Amsterdam', 'Athens', 'Atlanta', 'Auckland', 'Bangalore',
        'Bangkok', 'Barcelona', 'Beijing', 'Berlin', 'Bogota', 'Boston',
        'Brisbane', 'Brussels', 'Bucharest', 'Budapest', 'Buenos Aires',
        'Chengdu', 'Chicago', 'Copenhagen', 'Dallas', 'Denver', 'Dubai',
        'Dublin', 'Frankfurt', 'Geneva', 'Guangzhou', 'Hamburg',
        'Hong Kong', 'Houston', 'Istanbul', 'Jakarta', 'Johannesburg',
        'Kuala Lumpur', 'Lima', 'Lisbon', 'London', 'Los Angeles',
        'Luxembourg', 'Madrid', 'Manila', 'Melbourne', 'Mexico City',
        'Miami', 'Milan', 'Montreal', 'Moscow', 'Mumbai', 'Munich',
        'Nairobi', 'New Delhi', 'New York', 'Oslo', 'Paris', 'Perth',
        'Prague', 'Rome', 'San Francisco', 'Sao Paulo', 'Santiago', 'Sydney',
        'Seoul', 'Shanghai', 'Shenzhen', 'Singapore', 'Stockholm',
        'Taipei', 'Tel Aviv', 'Tianjin', 'Tokyo', 'Toronto', 'Vancouver',
        'Vienna', 'Warsaw', 'Washington', 'Zurich']
    culture_group_labels = ['Germanic_Europe', 'Latin_America', 'Confucian_Asia', 'Anglo', 'Sub_Sahara_Africa', 'Southern_Asia', 'Latin_Europe', 'Eastern_Europe', 'Nordic_Europe', 'Arab']

    ordered_cities_colors = []
    for city_name in complete_city_list:
        raw_index = next((i for i, d in enumerate(cities_colors) if d['city'] == city_name), None)
        if raw_index != None:
            ordered_cities_colors.append(cities_colors[raw_index])
        else: continue

    ordered_cul_groups_colors = []
    for cul_group_name in culture_group_labels:
        raw_index = next((i for i, d in enumerate(cul_group_colors) if d['cul_group'] == cul_group_name), None)
        if raw_index != None:
            ordered_cul_groups_colors.append(cul_group_colors[raw_index])
        else: continue


    
    return jsonify({
        "cities_colors": ordered_cities_colors,
        "cul_groups_colors": ordered_cul_groups_colors
    })

@app.route('/api/building_color')
def req_building_color_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat4_sum.txt")[get_random_sample(vec_len)]
    
    labels = np.genfromtxt("./data/test_preds.txt", dtype=int, delimiter=",")[get_random_sample(vec_len), 1]
    cities_num = np.max(labels)+1
    stat = np.zeros([cities_num, res.shape[1]])
    for i in range(cities_num):
        stat[i, :] = np.sum((res.T*(labels==i)).T, axis=0) / np.sum(labels==i)

    attr_names = []
    for i in range(res.shape[1]):
        attr_names.append(f"bin{i*256}-bin{(i+1)*256-1}")

    return jsonify({"data": stat.tolist(), "tags": attr_names})

@app.route('/api/urban_sign')
def req_urban_sign_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat3_filtered.txt")[get_random_sample(vec_len)]
    
    labels = np.genfromtxt("./data/test_preds.txt", dtype=int, delimiter=",")[get_random_sample(vec_len), 1]
    cities_num = np.max(labels)+1
    stat = np.zeros([cities_num, res.shape[1]])
    for i in range(cities_num):
        stat[i, :] = np.sum((res.T*(labels==i)).T, axis=0) / np.sum(labels==i)


    attr_names = ['Plaque', 'Engrave Wall', 'Poster', 'Stand Alone', 'Hanging', 'Banner']
    return jsonify({"data": stat.tolist(), "tags": attr_names})

@app.route('/api/facade_material')
def req_facade_material_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat1.txt")[get_random_sample(vec_len)]
    
    labels = np.genfromtxt("./data/test_preds.txt", dtype=int, delimiter=",")[get_random_sample(vec_len), 1]
    cities_num = np.max(labels)+1
    stat = np.zeros([cities_num, res.shape[1]])
    for i in range(cities_num):
        stat[i, :] = np.sum((res.T*(labels==i)).T, axis=0) / np.sum(labels==i)

    attr_names = ['Brick', 'Concrete', 'Glass', 'Metal', 'Other', 'Paint', 'Stone', 'Wood']
    return jsonify({"data": stat.tolist(), "tags": attr_names})

@app.route('/api/architectural_style')
def req_architectural_style_data():
    vec_len = request.args.get("vec_len", 3000, int)
    res = np.genfromtxt("./data/test_feat2.txt")[get_random_sample(vec_len)]
    
    labels = np.genfromtxt("./data/test_preds.txt", dtype=int, delimiter=",")[get_random_sample(vec_len), 1]
    cities_num = np.max(labels)+1
    stat = np.zeros([cities_num, res.shape[1]])
    for i in range(cities_num):
        stat[i, :] = np.sum((res.T*(labels==i)).T, axis=0) / np.sum(labels==i)

    attr_names = ['Art_Deco', 'Brutalism', 'Eastern_Asian_Regional', 'Eastern_European_Regional', 'Georgian', 'Greystone', 'High-tech', \
                'International', 'Middle_Eastern_Regional',
                'Modern_high-rise_Apartment', 'Neoclassical', 'Nordic_Regional',
                'Postmodern', 'Ranch-style', 'Scandinavian_Vernacular',
                'Southeast_Asian_Regional', 'Southern_Asian_Regional',
                'Southern_European_Regional', 'Tube-shaped_Apartment', 'Victorian',
                'Western_European_Vernacular', 'Worker_Cottage']
    return jsonify({"data": stat.tolist(), "tags": attr_names})

# @app.route('/api/streetScale')
# def req_street_scale_data():
#     vec_len = request.args.get("vec_len", 3000, int)
#     res = np.genfromtxt("./data/test_feat0.txt")[:vec_len, :].tolist()
#     return jsonify(res)

# missing Facade material, Architectural style, Greenery, Urban sign

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050)
    # req_data_colors()