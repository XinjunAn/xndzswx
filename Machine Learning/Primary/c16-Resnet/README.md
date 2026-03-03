# 🚀 ResNet-18 复现：Fashion-MNIST 教学案例

本项目在 Fashion-MNIST 数据集上复现 ResNet-18，帮助理解残差连接（skip connection）与完整训练流程：数据准备 → 模型搭建 → 训练评估 → 结果分析。

## ✨ 实验目标与数据路径

- 数据集：Fashion-MNIST（10 类灰度图，28×28）
- 数据下载位置：D:\xiangmu\18-Resnet\data
- 目标：完成 ResNet-18 的训练与评估，并展示关键中间结果（数据规模、模型参数量、训练曲线与预测示例）

## 🧰 环境依赖

依赖已在 requirements.txt 中固定版本：
- torch
- torchvision
- numpy
- matplotlib
- tqdm
- Pillow

建议使用与 Notebook 相同的 Python/Conda 环境运行。

## ▶️ 运行方式

1. 安装依赖（根据你的环境选择 pip 或 conda）。
2. 打开并运行 Resnet.ipynb，从上到下依次执行所有单元。
3. 首次运行会自动下载 Fashion-MNIST 到 data/ 目录。

## 🧭 主要流程说明

### ① 固定随机种子与设备设置
- 固定随机种子以保证复现性。
- 自动检测 GPU/CPU。

### ② 数据加载与可视化
- 对 28×28 灰度图进行 ToTensor + Normalize。
- 使用 DataLoader 构建训练与测试集。
- 可视化一个 batch 的图像与标签。

### ③ 模型结构（ResNet-18 小改版）
为适配 28×28 灰度图，做了两点调整：
- 输入通道从 3 改为 1。
- 去掉 7×7 卷积与最大池化，改为 3×3 卷积与更温和下采样。

### ④ 训练与评估
- 损失函数：交叉熵
- 优化器：Adam
- 在每个 epoch 结束后评估测试集准确率

### ⑤ 结果可视化
- 绘制训练/测试 Loss 与 Accuracy 曲线
- 展示部分测试集预测结果

## 🗂️ 目录结构

```text
.
├─ Resnet.ipynb
├─ requirements.txt
└─ data
	└─ FashionMNIST
		└─ raw
			├─ t10k-images-idx3-ubyte
			├─ t10k-labels-idx1-ubyte
			├─ train-images-idx3-ubyte
			└─ train-labels-idx1-ubyte
```

## 💡 拓展与思考

1. 更深网络是否更好（修改 block 数量）
2. 数据增强的影响（随机裁剪、水平翻转）
3. 优化器与学习率策略对比（SGD + momentum + StepLR）
4. 残差块加入 Dropout 的效果
5. 类别混淆分析（混淆矩阵）
