# 此项目缺少数据集data，前往网盘或官网下载后，分别放置在正确路径下

```
Project
│
├── data\ # 存放数据集压缩包
│ ├── VOCtrainval_06-Nov-2007.tar
│ └── VOCtest_06-Nov-2007.tar
│── nootbook\ # 存放代码文件
│ ├── lab_cv_multilabel.ipynb # 主实验代码
└── README.md # 项目说明文档 (当前文件)
```

数据集下载与配置
由于官方源不稳定，建议手动下载数据集并放入 data 目录。

下载链接 (PJ Reddie 镜像源 - 高速推荐):

训练/验证集 (450MB): http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar
测试集 (430MB): http://pjreddie.com/media/files/VOCtest_06-Nov-2007.tar

下载上述两个 .tar 文件。

将它们直接移动到 Project 目录下，按项目树状图存放

注意：不需要手动解压，代码运行 torchvision 函数时会自动检测并解压。
