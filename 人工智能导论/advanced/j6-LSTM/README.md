# 此项目已包含全部内容

# 机床振动预测（LSTM）教学案例 | Time-Series Forecasting

本项目是一个面向教学的时序预测案例，演示如何使用LSTM对机床振动信号进行建模与预测。包含数据生成、序列构造、建模训练、评估与滚动预测等完整流程。

## 1. 项目结构

```
- jichunag.ipynb: 教学Notebook，包含完整流程与讲解
- requirements.txt: 依赖列表
- data/
  - simulated_vibration.csv: 生成的模拟振动数据
```

## 2. 环境准备

建议使用Python 3.9+。

安装依赖:

```bash
pip install -r requirements.txt
```

## 3. 运行方式

1. 打开并运行Notebook:

```bash
jupyter notebook jichunag.ipynb
```

2. 按照Notebook中的章节依次执行代码单元。

## 4. Notebook内容概览

1. 环境准备与数据路径
2. 生成模拟振动数据集
3. 构造振动时间序列并可视化
4. 窗口化与数据集划分
5. 构建LSTM模型
6. 训练模型与曲线可视化
7. 评估与结果对比
8. 滚动预测未来若干步
9. 拓展与思考

## 5. 数据说明

数据为模拟生成的机床振动信号，包含:

- time: 时间索引
- vibration: 振动幅值（目标序列）
- speed: 工况转速
- load: 工况载荷

## 6. 结果输出

- 训练过程损失曲线
- 测试集预测与真实值对比图
- 未来步预测曲线

## 7. 教学要点

- 时序预测的窗口化处理
- LSTM建模与防过拟合策略
- MAE与RMSE评估指标
- 预测结果的业务解释
