# 此项目缺少data，网盘下载后放在对应目录下

为了确保代码（.ipynb）能正确读取数据，请保持以下目录结构：

```
19-resnet-50/                  # 项目根目录
├── data/                      # 数据集根目录
│   ├── Training/              # 训练集 (用于模型学习)
│   │   ├── glioma_tumor/      # 类别 A (例如：纹理类型 I)
│   │   ├── meningioma_tumor/  # 类别 B (例如：纹理类型 II)
│   │   ├── no_tumor/          # 类别 C (例如：正常/无特征)
│   │   └── pituitary_tumor/   # 类别 D (例如：纹理类型 III)
│   └── Testing/               # 测试集 (用于模型验证)
│       ├── glioma_tumor/
│       ├── meningioma_tumor/
│       ├── no_tumor/
│       └── pituitary_tumor/
├── notebook/                  # 代码目录
│   └── lab_cv_resnet_structure.ipynb  # 主实验代码 (Jupyter Notebook)
├── README.md                  # 项目说明文档
└── requirements.txt           # 环境依赖列表
```

运行安装命令：
pip install -r requirements.txt

本实验采用的是公开的 MRI 结构扫描数据集（Brain Tumor MRI Dataset），但在教学中我们将其视为通用的结构纹理分类任务。
数据来源：Kaggle / 公开医疗影像库
图像格式：.jpg / .png (不同分辨率，代码会自动 Resize 为 224x224)
分类任务：4 分类 (Class Classification)
进行本地下载的数据集链接：https://www.kaggle.com/datasets/sartajbhuvaji/brain-tumor-classification-mri
