import os
from ultralytics.models import YOLOv10



if __name__=='__main__':
    model = YOLOv10('yolov10n.pt')
    model.train(data='C:/Users/aa321/Desktop/fin/data.yaml', seed=42, epochs=200, device="cuda")