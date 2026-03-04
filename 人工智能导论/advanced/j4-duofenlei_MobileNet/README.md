# 此项目缺少数据集data和权重文件：mobilenetv2_plantvillage.pth，前往网盘下载后，分别放置在正确路径下

# 植物叶片病害多分类（MobileNet）教学案例

> 轻量级迁移学习完整教学流程

## 一、项目简介

本项目使用 PlantVillage 数据集进行植物叶片病害多分类，基于 MobileNetV2 进行迁移学习训练与评估，覆盖数据准备、训练、验证、测试、混淆矩阵与单图推理的完整流程。

## 二、目录结构

- README.md
- requirements.txt
- yepian.ipynb
- mobilenetv2_plantvillage.pth
- data/
  - Plant_leave_diseases_dataset_with_augmentation/
    - <class_name>/

## 三、环境与依赖

建议使用 Python 3.8+。依赖见 requirements.txt。

## 四、数据集准备

将 PlantVillage 数据集解压到 d:\xiangmu\j4-yepian\data 目录中，最终类别目录应为“文件夹名=类别名”的结构。

示例结构：
D:\xiangmu\j4-yepian\data\
 ├─ Tomato***Late_blight
├─ Tomato***healthy
└─ ...

如解压后多了一层目录，程序会自动识别包含类别子目录的根路径。

## 五、使用方法

1. 打开 yepian.ipynb
2. 从上到下依次运行各单元格
3. 查看训练日志、验证结果与测试集评估

## 六、主要流程

1. 环境与路径设置
2. 数据读取与类别查看
3. 数据集划分与数据增强
4. DataLoader 验证
5. MobileNetV2 构建与预训练权重加载
6. 训练与验证
7. 测试集评估与混淆矩阵
8. 保存模型
9. 单张图片推理示例

## 七、输出结果

- 训练与验证的损失、准确率
- 测试集整体准确率与分类报告
- 混淆矩阵可视化
- 训练后的模型权重文件（mobilenetv2_plantvillage.pth）

## 八、可扩展方向

- 更丰富的数据增强
- 学习率策略（如 Cosine Annealing）
- 更轻量或更强的模型（MobileNetV3、EfficientNet）
- 类别不平衡处理（加权损失或重采样）

## 九、说明

如需在 GPU 上训练，请确保已正确安装 CUDA 版本的 PyTorch 并配置驱动。
