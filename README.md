自用的一些小脚本，针对Bert_VITS2的中文，稍微改改输出格式也可以用在其他VITS，有些参数写死但懒得改了……

使用的是FunASR以及modelscope模型仓库

任务1：重采样和格式转换->标注->简单清洗->标点恢复

任务2：重采样和格式转换->标注（带标点）和将长音视频切分短音频->简单清洗

推荐一个切成短音频的项目[Dataset_Generator_For_VITS](https://github.com/Fatfish588/Dataset_Generator_For_VITS)

# 安装依赖

建议使用python 3.8

```
conda create -n datasets_tools python==3.8
conda activate datasets_tools
```

使用cuda加速，需要提前装好cuda环境

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
pip install funasr -i https://mirror.sjtu.edu.cn/pypi/web/simple
pip install modelscope -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install hdbscan umap joblib==1.1.0 --index-url https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://pypi.artrajz.cn/simple --prefer-binary
```

依赖可能没写完整，缺啥装啥

# 使用

可以分开执行需要的脚本，也可以直接运行main.py全部执行
