# 測試指南 - Gemini Image Generation API

## 🎯 測試結果總結

### ✅ 已通過的測試
1. **環境設置** - Python 3.12.8，所有必要目錄和文件存在
2. **模組導入** - 所有 Python 模組正確導入
3. **API 密鑰設置** - .env 文件已創建，API 密鑰格式正確
4. **基本功能** - 提示詞模板和 ImageGenerator 類別正常工作

### ⚠️ 需要真實 API 密鑰的測試
- **API 連接測試** - 需要有效的 Gemini API 密鑰才能生成真實圖片

## 🚀 如何完成設置

### 1. 獲取 Gemini API 密鑰
1. 訪問 [Google AI Studio](https://aistudio.google.com/)
2. 登入你的 Google 帳戶
3. 創建新的 API 密鑰
4. 複製生成的 API 密鑰

### 2. 設置 API 密鑰
```bash
# 編輯 .env 文件
nano .env

# 將 your_gemini_api_key_here 替換為你的真實 API 密鑰
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. 驗證設置
```bash
# 運行完整測試
python test_setup.py

# 運行功能演示（不需要 API 密鑰）
python demo.py
```

## 🧪 測試腳本說明

### test_setup.py
- **用途**: 驗證環境設置和基本功能
- **運行**: `python test_setup.py`
- **包含測試**:
  - Python 版本檢查
  - 目錄和文件存在性
  - 模組導入測試
  - API 密鑰格式檢查
  - 基本功能測試
  - API 連接測試（需要真實密鑰）

### demo.py
- **用途**: 展示代碼結構和功能
- **運行**: `python demo.py`
- **特點**: 不需要真實 API 密鑰
- **展示內容**:
  - 提示詞模板生成
  - 類別結構
  - 教程組織
  - 專案結構

## 🎨 功能測試

### 1. 基本文字轉圖片
```python
from ai import ImageGenerator

generator = ImageGenerator()
result = generator.generate_text_to_image(
    prompt="一隻可愛的橘貓在花園裡",
    output_filename="test_cat",
    save_image=True
)
```

### 2. 專業模板使用
```python
from ai import ImageGenerator, ImageStyle, CameraAngle

generator = ImageGenerator()
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="高級無線耳機",
    style=ImageStyle.PHOTOREALISTIC,
    context="電商產品攝影",
    camera_angle=CameraAngle.MACRO
)
```

### 3. 圖片編輯
```python
from PIL import Image

# 載入現有圖片
input_image = Image.open("path/to/image.png")

# 編輯圖片
result = generator.generate_image_editing(
    prompt="添加一隻貓咪在沙發上睡覺",
    input_image=input_image,
    output_filename="edited_image"
)
```

## 📚 教程測試

### 運行所有教程
```bash
# 基本文字轉圖片
python tutorials/01_text_to_image.py

# 圖片編輯和修復
python tutorials/02_image_editing.py

# 進階合成
python tutorials/03_advanced_composition.py

# 專業用例
python tutorials/04_specialized_use_cases.py
```

### 快速開始
```bash
python examples/quick_start.py
```

## 🐳 Docker 測試

### 使用 Docker Compose
```bash
# 構建並運行
make docker-run

# 運行特定教程
docker-compose run gemini-api python tutorials/01_text_to_image.py
```

### 手動 Docker
```bash
# 構建鏡像
docker build -t gemini-api .

# 運行容器
docker run -v $(pwd)/outputs:/app/outputs \
  -e GEMINI_API_KEY=your_key_here \
  gemini-api
```

## 🔧 開發測試

### 代碼格式檢查
```bash
make format
make lint
```

### 運行測試套件
```bash
make test
```

### 專案狀態檢查
```bash
make status
```

## 🚨 常見問題

### 1. API 密鑰無效
- **錯誤**: `API key not valid`
- **解決**: 檢查 .env 文件中的 GEMINI_API_KEY 是否正確

### 2. 模組導入失敗
- **錯誤**: `ModuleNotFoundError`
- **解決**: 運行 `pip install -r requirements.txt`

### 3. 權限錯誤
- **錯誤**: `Permission denied`
- **解決**: 確保 outputs 目錄有寫入權限

### 4. 圖片生成失敗
- **錯誤**: 生成結果為空
- **解決**: 檢查提示詞是否過於複雜，嘗試簡化

## 📊 性能基準

### 預期性能
- **文字轉圖片**: 5-15 秒
- **圖片編輯**: 10-20 秒
- **批量生成**: 每張圖片 5-15 秒

### 限制
- 最大 3 張輸入圖片
- 每次請求最多 1 張輸出圖片
- 所有生成圖片包含 SynthID 浮水印

## 🎉 成功指標

當你看到以下結果時，表示設置成功：

1. ✅ 所有測試通過
2. ✅ 能夠生成圖片並保存到 outputs/ 目錄
3. ✅ 提示詞模板正常工作
4. ✅ 所有教程可以正常運行
5. ✅ Docker 容器可以正常啟動

## 📞 支援

如果遇到問題：

1. 檢查 [README.md](README.md) 獲取完整文檔
2. 查看 [API_REFERENCE.md](docs/API_REFERENCE.md) 了解 API 詳情
3. 運行 `python demo.py` 查看功能演示
4. 檢查 [Gemini API 文檔](https://ai.google.dev/gemini-api/docs/image-generation)

---

**測試完成！你的 Gemini Image Generation API 已經準備就緒！** 🚀
