# VGG-16 轻量化与边缘设备适配（FashionMNIST 教学案例）

本项目基于 PyTorch 实现了一个面向教学的 **VGG-16 轻量化改造方案**，在 FashionMNIST 数据集上完成从数据读取、模型设计、训练评估到轻量化对比与量化示例的完整流程。

核心目标：在尽量保持分类性能的前提下，降低模型参数量与模型体积，使其更适合边缘设备部署。

## 1. 项目亮点

- 基于经典 VGG-16 结构进行轻量化改造
- 支持通过 `width_mult` 进行通道缩放
- 在中后期阶段使用深度可分离卷积降低计算量
- 使用全局平均池化减少全连接层参数
- 包含训练曲线可视化、预测结果可视化
- 提供参数量/模型体积对比与动态量化示例

## 2. 目录结构

```text
j18-VGG/
├── README.md
├── requirements.txt
├── VGG.ipynb
└── data/
    └── FashionMNIST/
        └── raw/
            ├── t10k-images-idx3-ubyte
            ├── t10k-labels-idx1-ubyte
            ├── train-images-idx3-ubyte
            └── train-labels-idx1-ubyte
```

## 3. 环境依赖

`requirements.txt`：

- `torch==2.1.2`
- `torchvision==0.16.2`
- `numpy==1.26.4`
- `matplotlib==3.8.2`

安装方式：

```bash
pip install -r requirements.txt
```

## 4. 数据集说明

本项目使用 **FashionMNIST**，默认从本地路径读取：

```python
data_root = r"D:\xiangmu\j18-VGG\data"
```

注意：若你的工程路径不同，请在 `VGG.ipynb` 中将 `data_root` 修改为你本地的 `data` 目录。

## 5. 模型设计（VGG16-Lite）

轻量化策略：

1. **通道缩放**：通过 `width_mult` 缩小每层通道数（示例中为 `0.5`）
2. **深度可分离卷积**：从指定 stage 开始替换普通卷积（示例中从第 3 个 stage）
3. **全局平均池化**：`AdaptiveAvgPool2d((1,1))` 替代大规模全连接输入

模型构造示例：

```python
model = VGG16Lite(num_classes=10, width_mult=0.5, use_depthwise_from_stage=3)
```

## 6. 训练配置

- 损失函数：`CrossEntropyLoss(label_smoothing=0.1)`
- 优化器：`AdamW(lr=1e-3, weight_decay=1e-4)`
- 学习率策略：`CosineAnnealingLR(T_max=epochs)`
- 训练轮次：`epochs = 50`
- 数据增强：`RandomCrop + RandomHorizontalFlip`

训练过程中记录：

- `train_loss` / `test_loss`
- `train_acc` / `test_acc`
- 学习率变化

## 7. Notebook 使用流程

打开并按顺序运行 `VGG.ipynb`：

1. 环境与依赖导入
2. 数据集读取与可视化
3. 构建 VGG16-Lite
4. 训练与验证
5. 绘制损失/准确率曲线
6. 测试集预测可视化
7. 与标准 VGG-16 做参数与体积对比
8. （可选）执行动态量化示例

## 8. 结果与分析要点

Notebook 中给出了以下分析方向：

- 训练后期可能出现过拟合（训练损失下降、测试损失上升）
- 可通过数据增强、权重衰减、标签平滑、学习率调度缓解
- 轻量化模型在参数量和模型体积上相较标准 VGG-16 更具优势
- 动态量化（线性层 INT8）可进一步减小模型体积

## 9. 可拓展方向

- 更小 `width_mult` 下结合知识蒸馏提升精度
- 对不同 stage 的深度可分离卷积替换策略做消融实验
- 面向边缘部署关注延迟、峰值内存、能耗与算子支持
- 迁移到 RGB 数据集时将输入通道改为 3 并调整归一化参数

## 10. 适用场景

- 计算机视觉课程中的 CNN 与模型压缩教学
- 轻量化网络设计实验
- 边缘设备部署前的模型对比与原型验证
