# 本项目缺少数据集和一些必要的权重文件，涉及的权重文件较多，如j27-RT-DETR\runs\neu_rtdetr_teaching\weights，j27-RT-DETR\runs\neu_rtdetr_teaching2\weights或j27-RT-DETR\rtdetr-l.pt等，下载时注意路径

# RT-DETR 工业表面缺陷检测教学案例（NEU-DET）

本项目基于 **RT-DETR + 弱监督伪框生成**，演示如何把仅有图像级类别标签的数据（NEU-DET）转换为目标检测训练数据，并完成训练、评估与可视化。

> 核心思路：先用传统图像处理生成伪框（pseudo bounding boxes），再导出 COCO/YOLO 格式供 RT-DETR 训练。

---

## 1. 项目亮点

- 从分类标签迁移到检测任务的完整工程闭环
- 自动生成伪框并导出 COCO 标注
- 自动转换 YOLO 标签，避免训练时 `no labels found`
- 使用 Ultralytics RT-DETR 进行训练、验证与推理可视化

---

## 2. 环境要求

- Python 3.9+（建议 3.10）
- Windows（当前工程路径示例）
- 建议使用 NVIDIA GPU（无 GPU 也可用 CPU）

安装依赖：

```bash
pip install -r requirements.txt
```

---

## 3. 目录结构（树状）

```text
j30-RT-DETR/
├─ neu_rtdetr.yaml
├─ requirements.txt
├─ rtdetr-l.pt
├─ yolo26n.pt
├─ rtdetr.ipynb
├─ data/
│  ├─ NEU-DET/
│  │  ├─ ANNOTATIONS/
│  │  └─ IMAGES/
│  └─ neu_pseudo_det/
│     ├─ annotations/
│     │  ├─ all_pseudo_coco.json
│     │  ├─ train.json
│     │  ├─ val.json
│     │  ├─ test.json
│     │  └─ pseudo_boxes_preview.csv
│     ├─ splits/
│     │  ├─ train.txt
│     │  ├─ val.txt
│     │  └─ test.txt
│     ├─ visualizations/
│     └─ yolo/
│        ├─ images/
│        │  ├─ train/
│        │  ├─ val/
│        │  └─ test/
│        └─ labels/
│           ├─ train/
│           ├─ val/
│           └─ test/
└─ runs/
   └─ detect/
      ├─ val/
      ├─ neu_rtdetr_teaching/
      └─ neu_rtdetr_teaching2/
```

---

## 4. 数据与标签说明

- 原始图像目录：`data/NEU-DET/IMAGES`
- 类别来源：从文件名解析（如 `crazing_1.jpg` → `crazing`）
- 伪框算法（Notebook 第 5 节）：
  1. 灰度化 + 高斯滤波
  2. Laplacian 增强纹理
  3. Otsu 阈值分割
  4. 形态学开闭运算
  5. 最大连通域外接框
  6. 异常面积时使用保底框

---

## 5. Notebook 执行流程

按 `rtdetr.ipynb` 从上到下执行：

1. 环境与路径初始化
2. 扫描图像并统计类别分布
3. 生成伪框并导出全量 COCO（`all_pseudo_coco.json`）
4. 抽样可视化伪框与中间掩码
5. 划分 train/val/test 并导出 COCO 子集
6. 生成 YOLO 数据（`images/` + `labels/`）
7. 生成 `neu_rtdetr.yaml`
8. 训练 RT-DETR（默认 10 epoch 教学参数）
9. 验证与测试样本推理可视化

---

## 6. 训练配置说明

默认关键参数（可在 Notebook 中调整）：

- `epochs=10`
- `imgsz=640`
- `batch=8`
- `workers=0`
- `device=0 or cpu`
- `pretrained=True`

本地权重文件：

- `rtdetr-l.pt`（RT-DETR）

---

## 7. 输出文件说明

- `data/neu_pseudo_det/annotations/all_pseudo_coco.json`：全量伪框 COCO 标注
- `data/neu_pseudo_det/annotations/train.json|val.json|test.json`：数据子集标注
- `data/neu_pseudo_det/annotations/pseudo_boxes_preview.csv`：伪框预览表
- `data/neu_pseudo_det/yolo/`：训练使用的 YOLO 图像与标签
- `neu_rtdetr.yaml`：Ultralytics 数据配置
- `runs/neu_rtdetr_teaching*/`：训练日志、权重、结果图

---

## 8. 常见问题

### 1）提示 `no labels found`

请确认已执行“生成 YOLO 格式标签”步骤，并检查：

- `data/neu_pseudo_det/yolo/labels/train/*.txt` 是否存在
- `neu_rtdetr.yaml` 中 `path/train/val/test` 是否指向正确

### 2）找不到权重文件

请确认根目录下存在：

- `rtdetr-l.pt`

### 3）CPU 训练过慢

可在 Notebook 里降低参数：

- `epochs` 减小
- `imgsz` 减小
- `batch` 减小

---

## 9. 教学建议

- 先小轮次（如 10 epoch）跑通流程，再做参数与算法对比实验
- 鼓励学生替换伪框策略并比较 mAP50 / mAP50-95
- 结合误检与漏检样本进行误差分析与改进设计

---

## 10. 致谢

- 数据集：NEU Surface Defect Dataset
- 模型与训练框架：Ultralytics RT-DETR
