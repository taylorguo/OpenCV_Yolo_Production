# OpenCV Yolo Object Detect

Using CV2.dnn module & Yolo COCO dataset pre-trained weights & configure for object detection.


## Download .weights, .cfg, .names files

go to "models" folder

下载类别coco名称
```
wget https://github.com/pjreddie/darknet/blob/master/data/coco.names
```

yolov3-tiny 网络结构和权重参数
```python
wget https://github.com/pjreddie/darknet/blob/master/cfg/yolov3-tiny.cfg
wget https://pjreddie.com/media/files/yolov3-tiny.weights
```

或者下载
yolov3 网络结构和权重参数
```
wget https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
wget https://pjreddie.com/media/files/yolov3.weights
```

## Dev python & dependencies ：

- Python3.6
- opencv-python >= 3.4
- yolov3 coco dataset pretrained weights & configure


## 安装
- Python3.6 & pip 请自行安装

- 依赖项安装：
```python
pip install opencv-python, numpy, imutils
```
