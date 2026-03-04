# 该项目缺少数据集，下载data后，放在对应目录下

## 项目结构

```
c20-tuijian/
├── README.md
├── requirements.txt
├── tuijian.ipynb
└── data/
    └── ml-100k/
        ├── allbut.pl
        ├── mku.sh
        ├── README
        ├── u.genre
        ├── u.info
        ├── u.item
        ├── u.occupation
        ├── u.user
        ├── u1.base
        ├── u1.test
        ├── u2.base
        ├── u2.test
        ├── u3.base
        ├── u3.test
        ├── u4.base
        ├── u4.test
        ├── u5.base
        ├── u5.test
        ├── ua.base
        ├── ua.test
        ├── ub.base
        └── ub.test
```

# j33-tuijian

一个基于 `MovieLens 100K` 数据集的推荐系统练习项目，主要在 Jupyter Notebook 中完成数据处理与建模实验。

## 环境依赖

项目依赖见 `requirements.txt`，主要包括：

- numpy==1.26.4
- pandas==2.2.2
- scipy==1.15.3
- scikit-learn==1.4.2
- torch==2.7.1
- ipykernel==7.2.0

## 快速开始

1. 创建并激活 Python 虚拟环境（可选但推荐）。
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 启动 Notebook：

```bash
jupyter notebook
```

4. 打开并运行：`tuijian.ipynb`

## 数据说明

- 数据集目录：`data/ml-100k/`
- 数据来源：MovieLens 100K（分割文件如 `u1.base/u1.test` 等用于训练/测试）。

## 备注

- 本项目以 Notebook 实验为主，建议按单元顺序执行。
- 若遇到包版本冲突，建议使用独立虚拟环境重新安装依赖。
