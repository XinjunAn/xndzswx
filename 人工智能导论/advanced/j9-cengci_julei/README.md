# 此项目已包含全部内容

# 传感器数据层次聚类（凝聚式）教学案例

本项目是一个面向教学的层次聚类（凝聚式）示例，覆盖从数据生成、标准化、树状图分析到聚类结果可视化的完整流程。

## 01. 内容概览

- 生成模拟传感器数据并保存到 [data/sensor_data.csv](data/sensor_data.csv)
- 读取数据、查看统计信息与缺失值
- 标准化特征并输出中间统计结果
- 计算链接矩阵与树状图（dendrogram）
- 训练凝聚式层次聚类模型并对比真实状态
- PCA 降维可视化聚类结果
- 给出拓展思考与解答思路

## 02. 文件结构

```
- ./
- ├─ [chuanganqi.ipynb](chuanganqi.ipynb) : 教学用主笔记本
- ├─ [requirements.txt](requirements.txt) : 依赖列表与版本
- └─ [data/](data/) : 生成的数据文件目录
-    └─ [data/sensor_data.csv](data/sensor_data.csv) : 生成的传感器样例数据
```

## 03. 运行方式

1. 安装依赖

```bash
pip install -r requirements.txt
```

2. 打开并运行笔记本

在 Jupyter 或 VS Code 中打开 [chuanganqi.ipynb](chuanganqi.ipynb)，按顺序执行所有单元格。

## 04. 教学提示

- 树状图的“距离断层”常用于选择合适的簇数 $k$。
- 不同链接方式（ward/average/complete）会影响簇的形状与合并顺序，可作为对比实验。
- 数据量增大时，可先做采样或使用预聚类方法，再进行层次聚类细化。

## 05. 依赖

详见 [requirements.txt](requirements.txt)。
