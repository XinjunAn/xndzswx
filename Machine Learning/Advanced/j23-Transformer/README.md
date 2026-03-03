建议的项目文件结构如下：
Project_Root/
├── data/                    # 数据存放目录 (脚本会自动创建并下载)
│   ├── cmn-eng.zip          # 原始压缩包
│   └── cmn.txt              # 解压后的双语语料
├── notebook/                # 代码目录
│   └── lab_nlp_transformer.ipynb  # 主实验代码 (Jupyter Notebook)
├── README.md                # 项目说明文档
└── requirements.txt         # 依赖库列表

快速开始 (Quick Start)
环境准备
确保你的环境已安装 Python 3.8+。建议创建一个新的虚拟环境。

安装项目依赖：
pip install -r requirements.txt

数据集如果下载失败，本地下载链接为：http://www.manythings.org/anki/cmn-eng.zip