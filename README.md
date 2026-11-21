# 紅綠燈辨識系統｜Traffic Light Detection

國立屏東大學資訊工程學系畢業專題，以 **YOLOv10** 進行紅綠燈物件偵測，結合 **OpenCV** 擷取攝影機影像與 **Supervision** 繪製偵測框、類別標籤，並依據偵測到的燈號顯示狀態提示。

- 作者：郭峻瑋
- GitHub：[AlanGuo0313](https://github.com/AlanGuo0313)
- 專案：[National-Pingtung-University-Capstone-Project](https://github.com/AlanGuo0313/National-Pingtung-University-Capstone-Project)

## 專案特色

- **攝影機影像辨識**：逐幀偵測紅燈、黃燈與綠燈。
- **視覺化結果**：在畫面上呈現物件框、類別標籤與狀態文字。
- **燈號判斷邏輯**：依據目前畫面中的偵測類別產生 `STOP`、`DRIVE` 或 `RUN` 提示。
- **自訂模型訓練**：提供 YOLOv10n 訓練程式、三類別資料設定與多次訓練紀錄。

本專案展示物件偵測模型訓練與攝影機推論的整合應用。目前未包含車道判定、目標交通號誌選擇、車輛控制或語音提醒。

## 技術組成

| 技術 | 用途 |
| --- | --- |
| Python | 主程式與訓練流程 |
| YOLOv10 / PyTorch | 模型訓練與物件偵測 |
| OpenCV | 攝影機讀取、文字繪製與視窗顯示 |
| Supervision | 偵測結果轉換、邊界框及標籤繪製 |
| YAML | 資料集路徑與類別設定 |

## 辨識流程與狀態規則

程式讀取預設攝影機，將每幀影像送入 `best2.pt`，再依偵測到的類別決定狀態，最後繪製結果並顯示於 `Webcam` 視窗。

| 類別 ID | 資料集類別 | 狀態提示 | 文字顏色 |
| --- | --- | --- | --- |
| 0 | red（紅燈） | `STOP` | 紅色 |
| 1 | yellow（黃燈） | `STOP` | 黃色 |
| 2 | green（綠燈） | `DRIVE` | 綠色 |
| 無偵測結果 | — | `RUN` | 白色 |

當畫面同時包含多種燈號時，現有程式的判斷優先順序為 **紅燈 → 綠燈 → 黃燈**。`RUN` 僅表示未偵測到上述類別，不能解讀為允許通行。

> 本系統為學習與專題展示用途，狀態提示不應作為實際駕駛或車輛控制依據。

## 專案檔案

以下路徑以儲存庫根目錄為基準，主要程式位於 `CBB110132郭峻瑋 紅綠燈辨識系統/`。

| 檔案／資料夾 | 說明 |
| --- | --- |
| `紅綠燈辨識系統.py` | 攝影機辨識主程式，預設載入 `best2.pt` |
| `yolov10訓練程式.py` | 以 `yolov10n.pt` 為起點進行模型訓練 |
| `data.yaml` | 訓練／驗證資料路徑與三種燈號類別 |
| `best1.pt`、`best2.pt` | 專案內保存的模型權重 |
| `yolov10n.pt`、`yolov8n.pt` | 其他模型權重；目前主程式使用 YOLOv10 |
| `train/`、`valid/` | 訓練與驗證影像、標註資料 |
| `runs/detect/` | 多次訓練產生的參數、評估數據、圖表與權重 |
| `test2.mp4` | 測試影片素材；目前主程式預設使用攝影機 |
| `ultralytics/` | 專案附帶的模型程式碼，包含 YOLOv10 |
| `yolov10/` | 附帶的 YOLOv10 原始碼、依賴設定與文件 |
| `wandb/` | 實驗紀錄 |

## 安裝與執行

以下以 Windows PowerShell 示範。需準備可用攝影機；訓練程式原始設定使用 CUDA。安裝流程依據專案內附的原始碼與依賴設定整理，尚未在全新環境完成執行驗證。

### 1. 下載專案並進入程式目錄

```powershell
git clone https://github.com/AlanGuo0313/National-Pingtung-University-Capstone-Project.git
cd National-Pingtung-University-Capstone-Project
cd "CBB110132郭峻瑋 紅綠燈辨識系統"
```

### 2. 建立環境與安裝依賴

建議使用 Python 3.10 的獨立環境。專案內附的 YOLOv10 依賴檔包含 `torch==2.0.1` 與 `torchvision==0.15.2`；實際 GPU 環境仍須搭配相容的驅動與 PyTorch 安裝版本。

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r .\yolov10\requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .\yolov10
.\.venv\Scripts\python.exe -m pip install supervision
```

本程式使用 `from ultralytics.models import YOLOv10`，請使用專案附帶的 YOLOv10 實作，避免直接以其他版本的 `ultralytics` 取代。原始專案未固定 Supervision 版本，若其 API 與主程式不相容，需調整版本或對應呼叫。

### 3. 啟動攝影機辨識

請保持目前工作目錄在主要程式所在的資料夾，讓相對路徑 `best2.pt` 能正確載入。

```powershell
.\.venv\Scripts\python.exe ".\紅綠燈辨識系統.py"
```

程式預設以 `cv2.VideoCapture(0)` 開啟攝影機，並在終端機輸出偵測類別與狀態。於影像視窗按下 **Q** 結束。

若需改用專案影片，請先將主程式中的輸入改為：

```python
cap = cv2.VideoCapture('test2.mp4')
```

## 模型訓練

### 1. 修正資料集路徑

現有 `data.yaml` 與訓練程式仍包含原開發電腦的絕對路徑。請先將 `data.yaml` 改成自己的資料位置，例如：

```yaml
path: C:/your-path/National-Pingtung-University-Capstone-Project/CBB110132郭峻瑋 紅綠燈辨識系統
train: train/images
val: valid/images
nc: 3
names: ['red', 'yellow', 'green']
```

影像與對應的 YOLO 格式 `.txt` 標註應具有相同檔名，並分別置於各資料集的 `images/` 與 `labels/` 資料夾。

### 2. 修改訓練程式

將 `yolov10訓練程式.py` 內的 `model.train(...)` 修改為以下形式；請從主要程式資料夾執行：

```python
model.train(data='data.yaml', seed=42, epochs=200, device='cuda')
```

原始訓練設定為 YOLOv10n、200 epochs、隨機種子 42，並使用 CUDA。沒有相容 GPU 時可將 `device` 改為 `'cpu'`，但訓練時間可能大幅增加。

```powershell
.\.venv\Scripts\python.exe ".\yolov10訓練程式.py"
```

訓練輸出位於 `runs/detect/train*/`。若要使用新模型，請將主程式的 `YOLOv10('best2.pt')` 改為新產生的 `weights/best.pt` 路徑。

## 訓練紀錄與成果

以下為 `runs/detect/train13/results.csv` **第 200 個 epoch** 的驗證紀錄，並非獨立測試集結果，也未確認此紀錄對應主程式載入的 `best2.pt`。

| 指標 | 紀錄數值 |
| --- | ---: |
| Precision | 0.82936 |
| Recall | 0.81258 |
| mAP@50 | 0.92256 |
| mAP@50–95 | 0.63169 |

**資料切分限制：**目前資料夾的 `train/images` 與 `valid/images` 各有 85 張圖片，經 SHA-256 比對，85 張圖片的內容皆在另一組出現。這代表目前提供的兩組資料有完整重疊；上述歷史紀錄的實際訓練資料快照則無法僅由現有檔案確認。因此，這些分數僅供檢視訓練過程，不能視為對未見場景的泛化能力證明。後續應依拍攝場景或影片來源重新切分互不重疊的訓練、驗證與測試集，再重新評估。

### 訓練曲線

![第 13 次訓練的損失與評估曲線](CBB110132郭峻瑋%20紅綠燈辨識系統/runs/detect/train13/results.png)

### 混淆矩陣

![第 13 次訓練的混淆矩陣](CBB110132郭峻瑋%20紅綠燈辨識系統/runs/detect/train13/confusion_matrix.png)

### 驗證影像預測範例

以下為訓練輸出中的驗證預測圖，並非攝影機實測截圖。

![驗證資料預測範例](CBB110132郭峻瑋%20紅綠燈辨識系統/runs/detect/train13/val_batch0_pred.jpg)

## 常見問題

| 問題 | 處理方式 |
| --- | --- |
| 無法開啟攝影機 | 確認攝影機權限、是否被其他程式占用，或調整 `VideoCapture(0)` 的裝置索引 |
| 找不到 `best2.pt` | 從主要程式資料夾啟動，或將模型路徑改為正確位置 |
| 無法匯入 `YOLOv10` | 確認使用專案環境及附帶的 YOLOv10 實作，並檢查 `ultralytics.__file__` 指向的模組位置 |
| Supervision 類別或方法不存在 | 核對 `BoundingBoxAnnotator`、`LabelAnnotator`、`Detections.from_ultralytics` 的 API 相容性 |
| 訓練找不到圖片 | 同時修正 `data.yaml` 的資料路徑及訓練程式的 YAML 路徑 |
| CUDA 無法使用 | 檢查 GPU、驅動與 PyTorch 相容性，或將訓練裝置改為 `cpu` |

## 後續改善方向

- 重新切分資料集，增加不同路口、距離、日夜與天候的獨立測試影像。
- 為多個號誌同時出現的場景加入目標選擇與區域判斷。
- 加入連續影格判斷，降低瞬間誤判造成的狀態跳動。
- 將模型、輸入來源與偵測門檻改為可設定參數。
- 固定可重現的依賴版本，補上實測環境、推論速度與攝影機展示影片。

## 致謝與授權

本專案使用 YOLOv10、Ultralytics、OpenCV 與 Supervision 等第三方元件。YOLOv10 原始專案資訊可參閱附帶的 [YOLOv10 README](CBB110132郭峻瑋%20紅綠燈辨識系統/yolov10/README.md)，第三方程式碼授權請以各元件隨附的授權文件為準。本 README 未替專題程式、模型或資料集新增授權條款。
