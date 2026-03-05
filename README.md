# 🤖 人工智能导论案例库

本仓库包含 **50个** 精选的机器学习与深度学习实战案例，旨在帮助学习者从基础过渡到进阶应用。

### 📂 仓库概览

- **[primary](primary/) 初级案例 (20个)**：以 `c` 开头，涵盖经典算法与基础神经网络。
- **[advanced](advanced/) 进阶案例 (30个)**：以 `j` 开头，聚焦工业、医疗等领域的复杂应用及深度学习前沿模型。

> [!IMPORTANT]
> **资源获取说明**：若单个案例缺少数据集、权重文件、 README 中的下载链接失效，请前往 **[人工智能导论网盘](https://pan.baidu.com/s/1nCdmYK8fgUEvc0H_tkXF5g?pwd=x8cc 提取码: x8cc)** 下载，并按照网盘中的目录结构保存在本地路径中。若本地目录与说明不一致，以网盘内的目录结构及文件为准。

---

### 🛠️ 案例构成

每个案例项目通常包含以下核心部分：

- **📄 案例书.docx**：详细的项目背景、原理讲解与操作指南。
- **📓 程序.ipynb**：可直接运行的交互式 Jupyter Notebook 代码。
- **📋 requirements.txt**：项目运行所需的 Python 环境依赖清单。
- **📁 data/**：数据集文件夹。_（注意：部分超大文件或数据集需从网盘单独下载）_

---

### 🚀 快速开始

1. **获取源码**：下载并解压案例压缩包。
2. **定位目录**：使用 VSCode 打开项目根目录（例如 `primary/c1-yuanweihua_erfenlei`）。
3. **补全数据**：检查是否缺少 `data` 文件或权重文件。若缺失，请从网盘下载并按 README 中的目录结构存放。
4. **环境准备**：
   ```bash
   # 创建虚拟环境
   conda create -n ai_case python=3.10
   # 激活环境
   conda activate ai_case
   # 安装依赖
   pip install -r requirements.txt
   ```
5. **执行案例**：在 VSCode 中切换至对应的内核（Kernel），即可分步运行单元格（Cell）。

---

## 📚 项目目录 (Project Index)

- **机器学期 (Machine Learning)**
  - **监督学习 (Supervised Learning)**
    - **二分类**
      - 初级：[c1. 鸢尾花品种二分类（逻辑回归）](primary/c1-yuanweihua_erfenlei)
      - 初级：[c2. 垃圾邮件二分类（朴素贝叶斯）](primary/c2-Naive%20Bayes)
      - 进阶：[j1. 医疗影像：乳腺肿瘤良恶性二分类（SVM）](advanced/j1-Breast%20Cancer%20Diagnostic%20Classification)
      - 进阶：[j2. 工业：铣床设备故障预测与诊断（随机森林）](advanced/j2-binary%20classification)
    - **多分类**
      - 初级：[c3. 手写数字识别 (MNIST+KNN)](primary/c3-MNIST)
      - 初级：[c4. 水果类别识别 (5类+决策树)](primary/c4-duofenlei)
      - 进阶：[j3. 工业：精密光学元件表面缺陷监督学习多分类（轻量CNN）](advanced/j3-Supervised%20Learning)
      - 进阶：[j4. CV：植物叶片病害多分类（MobileNet）](advanced/j4-duofenlei_MobileNet)
    - **多标签**
      - 初级：[c5. 新闻文本多标签分类 (TF-IDF+LR)](primary/c5-news_tfidf)
      - 进阶：[j5. CV：图像多目标标签分类（如“猫+草地”，轻量CNN）](advanced/j5-CNN)
    - **回归问题**
      - 初级：[c6. 房价预测 (线性回归)](primary/c6-Linear%20Regression)
      - 初级：[c7. 气温预测 (Lasso回归)](primary/c7-Lasso_huigui)
      - 进阶：[j6. 工业：机床损耗预测 (LSTM)](advanced/j6-LSTM)
      - 进阶：[j7. 医疗：高血压预测 (逻辑回归+KNN)](advanced/j7-Logistic%20KNN-hypertension)
  - **无监督学习 (Unsupervised Learning)**
    - **k-means**
      - 初级：[c8. 鸢尾花数据集聚类 (k-means)](primary/c8-yuanweihua-julei)
      - 初级：[c9. 手写数字聚类 (k-means+t-SNE)](primary/c9-k-means%2Bt-SNE)
      - 进阶：[j8. CV：复杂农产品图像无监督聚类 (k-means+简单特征)](advanced/j8-kmeans)
    - **层次聚类**
      - 初级：[c10. 学生成绩层次聚类](primary/c10-xueshengcengci-julei)
      - 进阶：[j9. 工业：传感器数据层次聚类 (凝聚式)](advanced/j9-cengci_julei)
    - **密度聚类**
      - 初级：[c11. 异常点检测 (DBSCAN + 模拟数据)](primary/c11-DBSCAN_midu)
      - 进阶：[j10. 工业：啤酒种类分析 (kmeans+dbscan)](advanced/j10-beers-kmeans-dbscan)
    - **高斯混合模型 (GMM)**
      - 初级：[c12. 模拟数据的高斯混合拟合](primary/c12-GMM)
      - 进阶：[j11. 工业：工业传感器生产参数概率建模与状态识别](advanced/j11-GMM-Sensor%20Parameter%20Fitting)
    - **降维 (Dimensionality Reduction)**
      - 进阶：[j12. CV：基于CIFAR-10数据集的PCA特征降维](advanced/j12-jiangwei)

- **深度学习 (Deep Learning)**
  - **卷积神经网络 (CNN)**
    - **LeNet**
      - 初级：[c13. LeNet实现MNIST手写数字识别](primary/c13-LeNet)
      - 进阶：[j13. CV：LeNet改进实现手写数字+字母混合识别](advanced/j13-EMNIST-LeNet)
    - **AlexNet**
      - 初级：[c14. AlexNet复现 (简化版)](primary/c14-AlexNet)
      - 进阶：[j14. CV：AlexNet微调实现动物分类](advanced/j14-Alexnet)
    - **VGG**
      - 初级：[c15. VGG-11简化版实现CIFAR-10分类](primary/c15-VGG-11)
      - 进阶：[j15. CV：VGG-16轻量化适配边缘设备](advanced/j15-VGG)
    - **ResNet**
      - 初级：[c16. ResNet-18复现 (CIFAR-10)](primary/c16-Resnet)
      - 进阶：[j16. CV：ResNet-18微调的腹部肿瘤MRI影像分类](advanced/j16-resnet_18)
    - **DenseNet**
      - 初级：[c17. DenseNet-121简化版训练](primary/c17-DenseNet)
      - 进阶：[j17. CV：基于DenseNet特征融合的花卉分类实验](advanced/j17-DenseNet)
    - **MobileNet**
      - 初级：[c18. MobileNet实现移动端图像分类 (低资源)](primary/c18-mobilenet)
      - 进阶：[j18. CV：基于MobileNet的零件缺陷检测系统](advanced/j18-MobileNet)
  - **循环神经网络 (RNN)**
    - **LSTM**
      - 进阶：[j19. 自然语言：LSTM实现文本情感分类](advanced/j19-ziranyuyan-LSTM)
      - 进阶：[j20. 时序：工业传感器数据损耗预测 (LSTM)](advanced/j20-shixu-LSTM)
    - **GRU**
      - 进阶：[j21. 自然语言：GRU实现短文本生成](advanced/j21-GRU_shakespeare_sonnets)
  - **Transformer**
    - **ViT**
      - 进阶：[j22. CV：ViT实现图像分类](advanced/j22-ViT_Classification)
    - **Transformer**
      - 进阶：[j23. 自然语言：Transformer简化版实现翻译](advanced/j23-Transformer)
  - **目标检测 (Object Detection)**
    - **Faster R-CNN / YOLO / SSD / RT-DETR**
      - 进阶：[j24. CV：Faster R-CNN简化版实现行人检测](advanced/j24-Faster%20R_CNN)
      - 进阶：[j25. CV：YOLOv5n (轻量版) 实现实时水果检测](advanced/j25-Yolov5)
      - 进阶：[j26. CV：SSD实现目标检测 (Pascal VOC)](advanced/j26-SSD)
      - 进阶：[j27. CV：RT-DETR实现工业流水线零件缺陷检测](advanced/j27-RT-DETR)
  - **语义分割 (Semantic Segmentation)**
    - **FCN / U-Net**
      - 初级：[c19. 行人路面分割 (U-Net)](primary/c19-U-Net)
      - 进阶：[j28. CV：FCN-32s语义分割 (PASCAL VOC)](advanced/j28-FCN)
      - 进阶：[j29. CV：U-Net简化版实现卫星图像建筑物与道路分割](advanced/j29-yaoganfenge-U-Net)
      - 进阶：[j30. 医疗：U-Net实现眼底血管分割](advanced/j30-yixuefenge-U-Net)

- **推荐系统 (Recommendation System)**
  - 初级：[c20. 推荐：协同过滤+轻量MLP实现电影推荐](primary/c20-tuijian)
