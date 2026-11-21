import cv2
import supervision as sv
from ultralytics.models import YOLOv10

# 加載 YOLO 模型
model = YOLOv10('best2.pt')
bba = sv.BoundingBoxAnnotator()
la = sv.LabelAnnotator()

# 自定義類別標籤（根據你的模型定義的類別順序）
class_labels = {2: "Green", 0: "Red", 1: "Yellow"}

# 開啟攝影機
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

while True:
    # 讀取攝影機的影像
    ret, frame = cap.read()
    if not ret:
        print("無法接收畫面 (結束程式)")
        break

    # 模型推理
    result = model(frame)[0]
    detections = sv.Detections.from_ultralytics(result)

    # 偵測到的類別 ID
    detected_classes = detections.class_id.tolist() if len(detections.class_id) > 0 else []

    # 判定狀態
    if 0 in detected_classes:  # 紅燈
        status = "STOP"
        color = (0, 0, 255)  # 紅色
    elif 2 in detected_classes:  # 綠燈
        status = "DRIVE"
        color = (0, 255, 0)  # 綠色
    elif 1 in detected_classes:  # 黃燈
        status = "STOP"
        color = (0, 255, 255)  # 黃色
    else:  # 無偵測到
        status = "RUN"
        color = (255, 255, 255)  # 白色

    # 打印偵測資訊
    print(f"Detected classes: {detected_classes}")
    print(f"Status: {status}")

    # 在畫面左上角顯示狀態
    cv2.putText(
        frame,  # 圖像
        f"Status: {status}",  # 顯示文字
        (20, 50),  # 文字位置
        cv2.FONT_HERSHEY_SIMPLEX,  # 字型
        1,  # 字體大小
        color,  # 顏色
        2,  # 粗細
        cv2.LINE_AA  # 線條類型
    )

    # 繪製標註
    annotated_image = bba.annotate(scene=frame, detections=detections)
    annotated_image = la.annotate(scene=annotated_image, detections=detections)

    # 顯示影像
    cv2.imshow('Webcam', annotated_image)

    # 按下 'q' 鍵結束視窗
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 釋放攝影機並關閉所有視窗
cap.release()
cv2.destroyAllWindows()
