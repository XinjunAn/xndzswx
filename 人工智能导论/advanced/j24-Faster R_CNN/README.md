# 此项目缺少data，前往网盘下载

建议的项目文件结构如下：

```
Plaintext
Project_Root/
├── data/ # 数据集存放目录 (上一级目录)
│ └── PennFudanPed/ # 自动下载解压后的数据
├── notebook/ # 代码目录
│ └── lab_cv_faster_rcnn.ipynb # 主实验代码 (Jupyter Notebook)
├── README.md # 项目说明文档
└── requirements.txt # 依赖库列表
```

快速开始 (Quick Start)
确保你的环境已安装 Python 3.8+。建议创建一个新的虚拟环境。
安装项目依赖：
pip install -r requirements.txt

数据集说明：
名称: Penn-Fudan Database for Pedestrian Detection and Segmentation
来源: University of Pennsylvania
规模: 170 张图片（训练集 + 测试集）。
特点: 小规模数据集，非常适合教学演示，在普通 GPU 上也能在几分钟内完成微调训练。
可以通过内置代码直接下载，若因网络问题下载失败，再尝试手动下载。
本地下载链接：https://www.cis.upenn.edu/~jshi/ped_html/PennFudanPed.zip
