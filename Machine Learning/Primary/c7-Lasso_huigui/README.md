# 此项目中已包含全部内容，创建环境安装包后直接运行即可

# 🌤️ Irvine 气温预测教学案例｜Lasso 回归

本项目基于 Irvine Daily Weather Data，使用 Lasso 回归进行气温预测与特征筛选，包含数据加载、标准化、网格搜索调参、评估与可视化等完整流程，适用于机器学习入门与回归模型教学。

## 📁 目录结构

```
7-qiwen/
├─ qiwenyuce.ipynb        # 完整教学 Notebook
├─ requirements.txt       # 依赖列表
└─ data/
	└─ weather.csv         # 数据文件（若本地不存在会自动下载）
```

## 🧩 环境要求

- Python 3.9+（建议）

## 📦 安装依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

## ▶️ 运行方式

1. 打开 qiwenyuce.ipynb。
2. 按顺序运行所有单元格。
3. 生成模型评估指标与可视化图表。

## 🎯 教学要点

- Lasso 回归的 L1 正则化与特征稀疏性
- 标准化对线性模型的重要性
- GridSearchCV + 交叉验证调参
- 回归任务评估指标：MSE、RMSE、R²
- 特征重要性解释与残差分析

## 🗂️ 数据说明

- 数据源：Irvine Daily Weather Data
- 若 data/weather.csv 不存在，Notebook 会自动从线上下载并保存到 data 目录。

## 📝 许可证

教学用途示例，可自由修改与使用。

