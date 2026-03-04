2-industrial-fault-prediction/      <-- 【项目根目录】
│
├── notebooks/                       <-- 【代码目录】
│   └── lab02_industrial_complete.ipynb   <-- 核心实验代码 (Jupyter Notebook)
│
├── data/                            <-- 【数据目录】
│   └── (本实验数据由代码实时生成，无需手动下载文件)
│       (如果你在代码中执行了 to_csv，生成的文件会保存在这里)
│
├── requirements.txt                 <-- 依赖库列表
│
└── README.md                        <-- 项目说明书


本实验使用的数据集为 “UCI AI4I 2020 增强版物理仿真数据”。
原始原型：https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset
本实验实现：为了模拟工业大数据场景（原始 UCI 数据仅 1万条，数据量太小），我们通过 Python 代码复现了其物理逻辑，生成了 500,000 条 仿真样本。