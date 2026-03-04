# 数据集等文件网盘下载：若需要整个yolov5-master文件，将yolov5-master下载即可，内部有数据集；runs和data文件下载后放在正确路径下

# YOLOv5n 水果检测（教学 Notebook）

本项目包含一个教学用 Notebook，用于训练与评估自定义水果数据集上的 YOLOv5n 模型。流程涵盖数据集检查、标注可视化、训练、指标可视化与推理（图片 + 摄像头）。

## 项目结构（树状）

```
.
├─ yolov5.ipynb
├─ data/
│  ├─ dataset.yaml
│  ├─ images/
│  │  ├─ train/
│  │  ├─ val/
│  │  └─ test/
│  └─ labels/
│     ├─ train/
│     ├─ val/
│     └─ test/
├─ yolov5-master/
│  ├─ train.py
│  ├─ val.py
│  ├─ detect.py
│  └─ models/
└─ runs/
   ├─ fruit_yolov5n_teaching/
   └─ detect/
      └─ fruit_teaching_demo/
```

## Notebook 中使用的路径

Notebook 默认使用如下路径（如有不同，请在 Notebook 中修改）：

- 项目根目录：`D:/xiangmu/j28-Yolov5`
- YOLOv5 代码：`D:/xiangmu/j28-Yolov5/yolov5-master`
- 数据集目录：`D:/xiangmu/j28-Yolov5/data`
- 训练输出：`D:/xiangmu/j28-Yolov5/runs`

## 流程概览

1. **环境与路径配置**
   - 配置 matplotlib 中文字体与项目路径。

2. **数据集完整性检查**
   - 校验 `images/{train,val,test}` 与 `labels/{train,val,test}`。
   - 校验 `data/dataset.yaml` 关键字段。

3. **标注可视化**
   - 抽样绘制标注框，检查类别与坐标。

4. **训练（直接 Python 调用）**
   - 使用 `yolov5-master/train.py` 的 `run(...)`。
   - 避免 subprocess，复用当前 PyTorch 环境。

5. **训练指标可视化**
   - 读取 `results.csv` 绘制损失与指标。
   - 展示 PR/P/R/F1 曲线与混淆矩阵。

6. **验证与预测**
   - 运行 `val.py` 与 `detect.py`。
   - 可视化预测结果。

7. **实时检测**
   - 使用摄像头实时推理。

## 关键输出

- 训练指标：`runs/fruit_yolov5n_teaching/results.csv`
- 曲线图：`runs/fruit_yolov5n_teaching/{PR_curve.png,P_curve.png,R_curve.png,F1_curve.png}`
- 混淆矩阵：`runs/fruit_yolov5n_teaching/confusion_matrix.png`
- 标签样图：`runs/fruit_yolov5n_teaching/val_batch2_labels.jpg`
- 预测输出：`runs/detect/fruit_teaching_demo/`

## 备注

- GPU 使用：设置 `DEVICE = "0"` 使用 CUDA，或设为 `"cpu"`。
- Windows 建议 `workers=0` 以避免多进程数据加载问题。
- 若只想可视化结果，可跳过训练单元。

## 使用方法

1. 在 VS Code 打开 `yolov5.ipynb`。
2. 按顺序运行各单元。
3. 快速验证可将 `EPOCHS` 调小（如 10）。
