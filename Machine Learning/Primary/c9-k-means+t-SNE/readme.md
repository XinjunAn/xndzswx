5-k-means/                   <-- 【项目根目录】
│
├── data/                    <-- 【数据目录】 (自动下载/存放 MNIST 数据)
│   └── openml               <-- 代码运行后会自动生成文件在这里
│
├── notebooks/               <-- 【代码目录】
│   └── lab09_digits_tsne_visual.ipynb  <-- 核心实验代码
│
├── README.md                <-- 【说明文档】 项目介绍与运行指南
│
└── requirements.txt         <-- 【依赖文件】 记录所需的 Python 库

关于数据集可以通过 Scikit-learn 库接口直接下载与加载，下载大概需要十多分钟左右，也可以直接解压缩数据集压缩包,压缩包存放到了data文件夹中，解压完成后按上面的项目树状图存放。
数据集本地下载：
下载链接: https://www.openml.org/d/554
说明: 这是 scikit-learn 官方推荐的源。如果在代码中无法自动下载，可以尝试从这里下载，但手动适配 scikit-learn 的缓存结构非常麻烦（不推荐手动替换，建议挂代理让代码自动跑）。