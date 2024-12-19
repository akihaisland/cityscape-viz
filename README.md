# CityViz
This platform supports cross-cultural research on cityscapes. The data was collected from 5,750,000 street view images across 75 cities worldwide.

## Installation
You need install [Node.js](http://nodejs.cn/download/) and [Python](https://www.python.org/).

### Python dependency Library
They're all in the requirements.txt.
```sh
Flask>=2.0.0
flask-cors>=3.0.0
numpy>=1.21.0
pandas>=1.3.0
scikit-learn>=0.24.0
torch>=1.9.0
tqdm>=4.62.0
seaborn>=0.11.0
matplotlib>=3.4.0
plotly>=5.0.0
```

### Install all dependency
```sh
pip install -r requirements.txt -i https://pypi.douban.com/simple
```

## Data
- [ ] raw data
- [x] Preprocessed [data](cityviz_backend\data) used to launch the system.

### Source Data
```
to be upload
```

### File Path
<!-- You need to put `imdb_vis30k`, `imdb_Beagle` and `data2vis_imdb` in `/Frontend/src/assets/static/`. -->
You need to modify the relevant paths in `data_process.ipynb` to be consistent.


## How To Run this Project
We have deployed the project to a cloud server. You can either directly open the [link](http://47.120.10.244:5173/) to use the system or follow the instructions below to deploy the system.

### Frontend -- Vue
#### Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).

#### Customize configuration
See [Vite Configuration Reference](https://vitejs.dev/config/).

#### Enter the Folder
```sh
cd cityviz_frontend
```

#### Project Setup
```sh
npm install
```

#### Compile and Hot-Reload for Development
```sh
npm run dev
```

#### Compile and Minify for Production
```sh
npm run build
```
---

### Backend -- Flask
#### Recommended IDE Setup
[VSCode](https://code.visualstudio.com/) or [Pycharm](https://www.jetbrains.com/pycharm/download/#section=windows) 

#### Enter the Folder
```sh
cd cityviz_backend
```

#### Compile and Run for Development
```sh
python app.py
```
