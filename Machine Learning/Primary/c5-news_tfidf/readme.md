4-news_tfidf/            <-- 项目根目录
├── notebooks/
│  └── lab04_news_tfidf.ipynb
├──  data/
│    └── 20news_home/     <-- 必须叫这个名字
│       ├── 20news-bydate-train/  <-- 里面有很多子文件夹 (rec.autos 等)
│       └── 20news-bydate-test/   <-- 里面有很多子文件夹
│
└── requirements.txt         <-- 支持运行所需安装的库


先运行脚本lab04_news_tfidf.ipynb自动下载数据集，如果下载失败，再进行手动下载

数据集手动下载
首先，手动下载数据集文件。你可以从以下链接下载：
   链接：https://pan.baidu.com/s/1a0vQ4OIxpvKtc_rxLVKxvQ
   提取码：40m9
下载完成后，将文件名修改为：
   20newsbydate.tar.gz
将文件放置到指定目录
   按上面的项目目录存放，进行解压缩，再重命名为20news_home