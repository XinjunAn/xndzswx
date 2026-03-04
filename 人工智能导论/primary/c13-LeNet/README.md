# 此项目缺少数据集，前往网盘下载，并移动到对应目录位置

```
15-lenet/ <-- 【项目根目录】
│
├── data/ <-- 【数据目录】
│ └── MNIST/ <-- (自动生成) PyTorch 数据集根目录
│ └── raw/ <-- (自动生成) 存放原始 .gz 压缩包的位置
│ ├── train-images-idx3-ubyte.gz
│ ├── train-labels-idx1-ubyte.gz
│ ├── t10k-images-idx3-ubyte.gz
│ └── t10k-labels-idx1-ubyte.gz
│
├── notebooks/ <-- 【代码目录】
│ └── lab15_lenet_mnist.ipynb <-- 核心实验代码
│
├── README.md <-- 项目说明书
│
└── requirements.txt <-- 依赖库 (包含 PyTorch, Torchvision)
```

如果自动下载完全失败，或者网络受限，请点击下方链接下载 4 个文件，并严格按照目录结构存放。

训练集图片: train-images-idx3-ubyte.gz

训练集标签: train-labels-idx1-ubyte.gz

测试集图片: t10k-images-idx3-ubyte.gz

测试集标签: t10k-labels-idx1-ubyte.gz

存放位置 (非常重要！) 请手动创建文件夹，确保文件路径如下所示（不要解压，保持 .gz 格式）：
项目根目录/data/MNIST/raw/train-images-idx3-ubyte.gz
项目根目录/data/MNIST/raw/train-labels-idx1-ubyte.gz
项目根目录/data/MNIST/raw/t10k-images-idx3-ubyte.gz
项目根目录/data/MNIST/raw/t10k-labels-idx1-ubyte.gz
(注：MNIST 和 raw 文件夹名称必须严格一致，区分大小写)
