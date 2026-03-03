8-densenet-cifar10/              <-- 【项目根目录】
│
├── data/                        <-- 【数据目录】(存放数据集)
│   └── cifar-10-batches-py/     <-- (自动/手动解压) CIFAR-10 数据文件夹
│       ├── data_batch_1
│       ├── ...
│       ├── test_batch
│       └── batches.meta
│
├── notebooks/                   <-- 【代码目录】
│   └── lab08_densenet_cifar10.ipynb  <-- 核心实验代码
│
├── README.md                    <-- 项目说明书
│
└── requirements.txt             <-- 依赖库列表



本实验使用的是 CIFAR-10 数据集。 代码默认会尝试自动下载 (download=True)。如果你的网络环境无法连接到外网，导致下载失败或速度极慢，请采用以下手动下载方案。

1. 手动下载链接
   请直接点击以下链接下载数据集（Python 版本）：

   官方源 (多伦多大学): https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
   cifar-10-python.tar.gz (约 163 MB)

2. 存放位置 (关键！)
下载完成后，请按照以下步骤操作，二选一即可：

方案 A：直接放入压缩包 (推荐)
   将下载好的 cifar-10-python.tar.gz 文件直接放入 data/ 目录中。

   路径：项目根目录/data/cifar-10-python.tar.gz

   操作：不需要解压。PyTorch 检测到这个压缩包后，会自动为你解压并校验。

方案 B：手动解压
   如果你已经解压了，请确保解压后的文件夹名为 cifar-10-batches-py，并将其放入 data/ 目录。

   路径：项目根目录/data/cifar-10-batches-py/

   检查：确保该文件夹里面直接就是 data_batch_1 等文件，不要有多余的嵌套文件夹（比如 data/cifar-10-python/cifar-10-batches-py 是错的）。