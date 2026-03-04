# 此项目缺少数据集前往网盘下载c18-mobilenet\data，并放在正确目录下

## 📁 项目结构

```
c18-mobilenet/
├─ mobilenet.ipynb
├─ requirements.txt
├─ README.md
└─ data/
   └─ cifar-10-batches-py/
```

# ✨ MobileNet 移动端图像分类（教学案例）

本项目是一个基于 **MobileNetV2** 的图像分类教学案例，使用 **CIFAR-10** 数据集完成迁移学习流程，涵盖数据读取、预处理、模型构建、训练评估与可视化。

## 🗂️ 数据集

- 数据集：CIFAR-10（10 类，32×32 彩色图像）
- 本地路径：D:\xiangmu\20-mobilenet\data
- 请确保已将 cifar-10-batches-py 解压到上述目录内。

## 🚀 运行说明

1. 打开并运行 [mobilenet.ipynb](mobilenet.ipynb)。
2. 如遇缺少依赖，请先运行笔记本最上方的安装单元。
3. 若需使用预训练权重，请将文件放到：
   D:\xiangmu\20-mobilenet\data
   - 文件名：mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_96_no_top.h5

> 注意：若未提供本地权重，模型会从头训练主干网络，收敛速度和精度会降低。

## 📦 依赖

依赖已在 [requirements.txt](requirements.txt) 中给出。

## 📊 结果与可视化

笔记本中包含：

- 训练/验证损失与准确率曲线
- 测试集评估
- 随机样本预测可视化

## 🧩 教学扩展

笔记本末尾提供了“拓展与思考”问题及参考思路，适合课堂讨论与作业延伸。
