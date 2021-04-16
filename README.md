# jigsaw

一个锯齿拼图的生成器与恢复器

## 环境

需要安装 ImageMagick，以及 Python 的 pillow、argparse、tqdm 库

```bash
sudo apt install imagemagick
pip3 install pillow argparse tqdm
```

## 用法

生成拼图

```bash
python3 jigsaw_create.py -i [原图片] -pw [每块的横向像素数] -ph [每块的纵向像素数] -sw [锯齿的像素数]
```

恢复拼图

```bash
python3 jigsaw_restore.py -px [横向的块数] -py [纵向的块数] -sw [锯齿的宽度]
```

## 样例

example.png 的分辨率是 1000x1000

以每一块 50x50，锯齿宽度 15px 生成拼图

```bash
python3 jigsaw_create.py -i example/example.png -pw 50 -ph 50 -sw 15
```

以横向 20 块，纵向 20 块，锯齿宽度 15px 恢复拼图

```bash
python3 jigsaw_restore.py -px 20 -py 20 -sw 15
```
