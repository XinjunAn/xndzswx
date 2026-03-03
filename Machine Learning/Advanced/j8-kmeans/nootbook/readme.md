Project
│
├── nootbook\                    # 存放代码文件
│    ├── lab_cv_kmeans_fruit_design.ipynb  # 主实验代码
│    └── README.md                # 项目说明文档 (当前文件)
│
└── requirements.txt             # 依赖库列表


实验数据集 (Synthetic Data)
为了模拟真实场景的复杂性，代码内置了一个生成器，生成以下 10 类 水果/蔬菜（共 500 张）：

🔴 红色系：Apple (圆), Tomato (稍扁), Cherry (小圆)

🟡 黄色系：Banana (长弯), Lemon (椭圆), Corn (长矩形)

🟢 绿色系：Cucumber (细长), Pear (上小下大), Grape (多圆组合)

🟣 紫色系：Eggplant (长椭圆)

特征设计： 每张图片被转换为一个 4 维向量：[R_mean, G_mean, B_mean, Aspect_Ratio]。

快速安装:
在终端运行 pip install -r requirements.txt 