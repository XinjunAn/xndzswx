# 此项目缺少数据集，前往网盘或官网下载后，放置在正确路径下

## 🧭 目录结构

```
Project_Root/
├── data/                                 # 数据集目录 (自动创建)
    └── NEU-DET/
    │   ├── train/                        # 训练集
    │       ├── annotations/
    │       │   ├── [1439个XML标注文件]
    │       └── images/
    │       │   ├── crazing/
    │       │       ├── [240个图片文件]
    │       │   ├── inclusion/
    │       │       ├── [240个图片文件]
    │       │   ├── patches/
    │       │       ├── [240个图片文件]
    │       │   ├── pitted_surface/
    │       │       ├── [240个图片文件]
    │       │   ├── rolled-in_scale/
    │       │       ├── [240个图片文件]
    │       │   └── scratches/
    │       │       ├── [240个图片文件]
    │   └── validation/                  # 验证集与测试集
    │       ├── annotations/
    │           ├── [361个XML标注文件]
    │       └── images/
    │           ├── crazing/
    │               ├── [60个图片文件]
    │           ├── inclusion/
    │               ├── [60个图片文件]
    │           ├── patches/
    │               ├── [60个图片文件]
    │           ├── pitted_surface/
    │               ├── [60个图片文件]
    │           ├── rolled-in_scale/
    │               ├── [60个图片文件]
    │           └── scratches/
    │               ├── [60个图片文件]
├── nootbook/
    └── lab_defect_detection_v2.ipynb   # 主实验代码
├── README.md                           # 项目说明
└── requirements.txt                    # 依赖列表
```

数据集运行会自行下载，因为网络问题如果下载失败，请采用手动下载方式进行下载。
Kaggle 下载
下载地址: https://www.kaggle.com/datasets/kaustubhb999/neu-surface-defect-database
下载完成后，按上面的项目结构目录存放。
