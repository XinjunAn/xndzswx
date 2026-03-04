# 此项目缺少data数据集

# 基于 DenseNet 特征融合的 Flowers-17 花卉分类教学实验

## 项目概览

本项目是一个**轻量入门**级深度学习教学案例，使用 Oxford Flowers-17 数据集，演示如何在 DenseNet 中进行**多层特征融合**，并完成一个可复现的端到端分类实验流程。

---

## 1. 知识点介绍

### DenseNet（密集连接神经网络）

- **核心特点**：每一层接收前面**所有层**的输出，形成"密集连接"
- **优势**：
  - 梯度传播更高效（梯度反向传播路径更多）
  - 特征复用效率高（避免信息瓶颈）
  - 参数量相对较少

### 特征融合（Feature Fusion）

- **定义**：不只用最后一层的**高级语义特征**，而是融合中间层的多尺度特征
- **中间层信息**：
  - `block2`：低层特征（纹理、边缘）
  - `block3`：中层特征（局部形状、纹理组合）
  - `block4`：高层特征（语义、对象部分）

### 在花卉分类中的意义

花卉分类经常需要识别：

- **花瓣形状与纹理**（需要低-中层特征）
- **花蕊颜色和形态**（需要中层特征）
- **整体轮廓和形态**（需要高层特征）

多尺度特征融合通常比单一输出层更**鲁棒**且**准确率更高**。

---

## 2. 项目设计意义

本实验帮助学生：

1. **掌握标准深度学习流程**：
   - 数据准备与预处理
   - 模型定义与初始化
   - 训练、验证、测试评估
   - 结果分析与可视化

2. **理解模型结构改造的影响**：
   - 通过"基线 DenseNet" vs "融合 DenseNet" 的对比
   - 理解不同层的特征如何影响分类
   - 学会作消融实验（Ablation Study）

3. **为进阶技术打基础**：
   - 迁移学习与微调策略
   - 混合注意力机制
   - 多模型集成

---

## 3. 环境与依赖

### 系统要求

- Python 3.8+
- CUDA 11.0+（可选，支持 GPU 加速）

### 依赖库

```bash
pip install -r requirements.txt
```

**requirements.txt 内容**：

```
torch==2.5.1
torchvision==0.20.1
numpy==1.26.4
matplotlib==3.9.2
seaborn==0.13.2
scikit-learn==1.5.2
Pillow==10.4.0
tqdm==4.66.5
```

### 快速安装

```bash
cd D:\xiangmu\j20-DenseNet
pip install -r requirements.txt
```

---

## 4. 项目结构

```
D:\xiangmu\j20-DenseNet\
├── densenet.ipynb              # 主教学 notebook
├── requirements.txt             # 依赖列表
├── README.md                    # 本文件
└── data/
    ├── image_0001.jpg ~ image_1360.jpg  # Flowers-17 图像（17类×80张）
    └── jpg/  (可选)             # 或在此目录中
```

### 数据说明

- **数据集**：Oxford Flowers-17
- **总数**：1360 张图像
- **类别数**：17
- **每类**：80 张
- **图像格式**：JPG
- **文件名**：`image_XXXX.jpg`（XXXX = 0001 ~ 1360）
- **标签推断**：由文件名自动推断（0~16）

---

## 5. 使用方法

### 5.1 准备数据

将 Flowers-17 数据集的 1360 张图像放在下列任一位置：

- `D:\xiangmu\j20-DenseNet\data\`
- `D:\xiangmu\j20-DenseNet\data\jpg\`

代码会自动检测并读取。

### 5.2 运行 Notebook

在 JupyterLab / Jupyter Notebook / VS Code 中打开 `densenet.ipynb`，顺序执行所有单元：

```bash
jupyter notebook densenet.ipynb
```

**主要单元组成**：

1. **导入库与设备设置**：固定随机种子、设置 CUDA/CPU
2. **数据读取**：本地加载 1360 张图像
3. **数据统计**：显示每类样本数、训练/验证/测试划分
4. **样本可视化**：随机展示 12 张图像
5. **数据管道**：定义 Dataset、DataLoader、数据增强
6. **模型定义**：DenseNetFusionClassifier（融合3层特征）
7. **训练**：8 个 epoch，含验证、最佳权重保存
8. **测试评估**：准确率、分类报告、混淆矩阵、预测样例
9. **拓展思考**：4 个学生思考题 + 解题提示

### 5.3 预期运行时间

- **首次运行**：下载 ImageNet 预训练权重 (~150MB)，约 2-5 分钟
- **训练 8 epoch**：GPU(NVIDIA V100) 约 8-12 分钟，CPU 约 30-60 分钟
- **总耗时**：20-90 分钟（取决于硬件）

---

## 6. 核心实现细节

### 6.1 DenseNetFusionClassifier

**模型结构**：

```
输入 224×224 RGB 图像
  ↓
DenseNet121 特征提取器 （骨干网络）
  ├→ denseblock2 → GlobalAvgPool → 512-dim 特征 (f2)
  ├→ denseblock3 → GlobalAvgPool → 1024-dim 特征 (f3)
  └→ denseblock4 → GlobalAvgPool → 1024-dim 特征 (f4)
  ↓
特征拼接 (Concatenate)
  ↓ 2560-dim
线性层 (2560 → 512) + ReLU + Dropout
  ↓
分类头 (512 → 17)
  ↓
输出 logits (17 类置信度)
```

**实现方式**：

- 使用 PyTorch Hook 机制拦截中间层输出
- 全局平均池化（GAP）将每个特征 map 降至 1D
- 特征拼接后过小型 MLP 分类头

### 6.2 数据增强策略

**训练集**：

- 随机大小缩放（0.7~1.0）并裁剪至 224×224
- 随机水平翻转
- 色彩抖动（亮度、对比度、饱和度）
- 标准化（ImageNet 均值/标差）

**验证/测试集**：

- 固定缩放至 224×224
- 中心裁剪
- 标准化

### 6.3 训练配置

| 参数         | 值                          |
| ------------ | --------------------------- |
| 优化器       | AdamW                       |
| 学习率       | 1e-4                        |
| Weight Decay | 1e-4                        |
| 批大小       | 32                          |
| Epoch        | 8                           |
| 学习率调度   | CosineAnnealingLR (T_max=8) |
| 损失函数     | CrossEntropyLoss            |

### 6.4 数据划分

- **训练集**：~1004 张（74%）
- **验证集**：~153 张（11%）
- **测试集**：~203 张（15%）

分层随机划分，保证每类比例一致。

---

## 7. 输出与结果

### 7.1 中间输出示例

**数据统计**：

```
使用数据目录: D:\xiangmu\j20-DenseNet\data
图像总数: 1360

每类样本数（应均为80）：
class 00: 80
class 01: 80
...
class 16: 80

数据划分结果：
Train: 1004
Val  : 153
Test : 203
```

**模型参数**：

```
DenseNetFusionClassifier
可训练参数量: 7.12 M
```

**训练日志**（示例）：

```
Epoch 01/08 | Train Loss: 2.5342, Train Acc: 0.2510 | Val Loss: 2.1234, Val Acc: 0.3456
Epoch 02/08 | Train Loss: 1.8932, Train Acc: 0.4321 | Val Loss: 1.6543, Val Acc: 0.5012
...
Epoch 08/08 | Train Loss: 0.4521, Train Acc: 0.8765 | Val Loss: 0.6234, Val Acc: 0.8234

Best Val Acc: 0.8234
```

### 7.2 可视化输出

1. **随机样本**：12 张花卉图像，带类别标签
2. **训练/验证曲线**：2 张图（损失曲线、准确率曲线）
3. **混淆矩阵**：17×17 热力图
4. **预测样例**：8 张测试图，显示真实标签 vs 预测标签

### 7.3 评估指标

**测试集准确率**：通常 78~85%（取决于训练轮数）

**分类报告**（precision / recall / F1 per class）

---

## 8. 学生拓展与思考题

### 题 1：融合与非融合的对比

**问题**：如果不用特征融合，只用 DenseNet 最后一层，准确率会如何变化？

**解题思路**：

1. 创建标准 DenseNet121（`models.densenet121`）
2. 保持其他条件不变（数据、优化器、epoch）
3. 比较：
   - Val Acc / Test Acc 的改变（通常降低 2~5%）
   - 训练是否更快（通常快 20%）
   - 哪些类别准确率下降最多（通常是细粒度差异的类别）

**参考答案**：融合通常比单层提升 3~5% 准确率，代价是训练时间增加 ~20%。

---

### 题 2：消融实验 - 哪三层融合最优？

**问题**：融合 `[f2, f3, f4]` vs `[f3, f4]` vs `[f4]`，哪个组合最优？

**解题思路**：

1. 修改 `DenseNetFusionClassifier.__init__()` 中的 `fusion_dim` 和 forward 逻辑
2. 训练三个模型版本
3. 记录：
   - 验证集准确率
   - 测试集准确率
   - 训练时间
4. 绘制表格或柱状图对比

**参考答案**：`[f2,f3,f4]` 通常最优；`[f3,f4]` 接近但参数少；`[f4]` 最快但准确率最低。

---

### 题 3：如何进一步提升性能？

**问题**：给定当前已有 ~82% 准确率，如何冲刺 90%+？

**解题思路**：

1. **训练策略**：
   - 增大 epoch（16-32）
   - 加入 warmup（前 2 epoch 线性升学习率）
   - 尝试 label smoothing（CrossEntropyLoss 中 label_smoothing=0.1）

2. **数据增强**：
   - 加入 `RandAugment` (magnitude=9, num_ops=2)
   - 尝试 `MixUp` 或 `CutMix`

3. **模型改进**：
   - 在融合后加入 SE 块（Squeeze-Excitation）
   - 使用更深的网络（DenseNet161）
   - 多头融合（不同权重融合不同层）

4. **集成方法**：
   - K 折交叉验证（K=5）
   - 模型集成（多个不同随机种子的模型投票）

**参考答案**：ep增加 + mixup + SE 块通常可提升 3~8%。

---

### 题 4（进阶）：可解释化 - 花卉类别名称映射

**问题**：当前标签是 0~16 的数字，如何显示真实花卉名字？

**解题思路**：

1. **获取官方类别名**：

   ```python
   class_names = [
       "Tulip", "Primula", "Cowslip", "Wild Pansy", "Lilyvalley",
       "Iris", "Buttercup", "Lungwort", "Bluebell", "Crocus",
       "Fritillary", "Snowdrop", "Daffodil", "Windflower", "Tigerlily",
       "Sunflower", "Daisy"
   ]
   ```

2. **修改预测显示**：

   ```python
   true_name = class_names[labels_batch[i].item()]
   pred_name = class_names[pred_batch[i].item()]
   plt.title(f"T:{true_name} P:{pred_name}")
   ```

3. **修改分类报告**：

   ```python
   print(classification_report(all_targets, all_preds,
                              target_names=class_names, digits=4))
   ```

4. **分析难分类别**：
   - 哪两类最容易混淆（混淆矩阵最大非对角元）
   - 查看这两类的视觉相似性
   - 思考是否需要特殊增强策略

**参考答案**：通常 `Iris` 与 `Bluebell` 混淆率较高（都是蓝紫色小花）。

---

## 9. 常见问题 (FAQ)

### Q1: 运行时 "CUDA out of memory" 错误

**A**：减少批大小：

```python
batch_size = 16  # 改为 16（默认 32）
train_loader = DataLoader(train_ds, batch_size=batch_size, ...)
```

### Q2: 数据读取失败 "FileNotFoundError"

**A**：检查数据路径：

```python
# 确认以下任一存在：
# D:\xiangmu\j20-DenseNet\data\image_0001.jpg
# D:\xiangmu\j20-DenseNet\data\jpg\image_0001.jpg
import os
print(os.listdir(r"D:\xiangmu\j20-DenseNet\data"))
```

### Q3: 模型精度低于预期

**A**：

- 增加训练 epoch（改为 16 或 32）
- 检查学习率（可尝试 5e-5 或 2e-4）
- 确认 SEED 是否设定（保证可复现性）

### Q4: 训练很慢

**A**：

- 检查是否使用 GPU：`print(DEVICE)`
- 确保安装了 `torch-cuda` 版本：`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

---

## 10. 参考资源

### 官方文档

- [DenseNet 论文](https://arxiv.org/abs/1608.06993)
- [PyTorch Vision Models](https://pytorch.org/vision/stable/models.html)
- [Oxford Flowers-17 官网](https://www.robots.ox.ac.uk/~vgg/data/flowers/17/)

### 扩展阅读

- 迁移学习：使用预训练权重的最佳实践
- 特征融合：FPN、PAN 等多尺度融合方法
- 花卉分类：细粒度分类的技巧

---

## 11. 许可与引用

**数据集引用**：

```
@inproceedings{nilsback08,
  author = {Nilsback, M-E. and Zisserman, A.},
  title = {A Visual Vocabulary for Flower Classification},
  booktitle = {CVPR},
  year = {2008}
}
```

**本项目**：

- 教学用途，可自由修改和使用
- 若用于学术发表，请注明来源

---

## 12. 联系与反馈

如有问题、建议或改进意见，欢迎反馈！

---

**最后更新**：2026-02-19

**版本**：v1.0 - 初版发布（DenseNet 特征融合、Flowers-17、教学版）
