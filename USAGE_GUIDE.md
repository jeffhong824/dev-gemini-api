# 🎨 使用指南 - Gemini Image Generation API

## 🚀 快速開始

### 1. 設置 API 密鑰
```bash
# 方法1: 使用設置助手
python setup_api_key.py

# 方法2: 手動設置
# 編輯 .env 文件，設置你的 GEMINI_API_KEY
```

### 2. 驗證設置
```bash
# 運行測試
python test_setup.py

# 查看功能演示
python demo.py
```

## 📚 各功能詳細用法

### 1. 基本文字轉圖片

#### 簡單用法
```python
from ai import ImageGenerator

# 初始化
generator = ImageGenerator()

# 生成圖片
result = generator.generate_text_to_image(
    prompt="一隻可愛的橘貓在花園裡",
    output_filename="my_cat",
    save_image=True
)

if result["success"]:
    print(f"圖片已保存到: {result['image_path']}")
```

#### 專業用法（使用模板）
```python
from ai import ImageGenerator, ImageStyle, CameraAngle

generator = ImageGenerator()

# 使用專業模板
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="高級無線耳機",
    style=ImageStyle.PHOTOREALISTIC,
    context="電商產品攝影",
    camera_angle=CameraAngle.MACRO,
    lighting="柔和的專業攝影棚燈光",
    composition="乾淨的白色背景，帶有微妙的陰影"
)
```

### 2. 圖片編輯和修復

#### 基本圖片編輯
```python
from PIL import Image

# 載入現有圖片
input_image = Image.open("path/to/your/image.png")

# 編輯圖片
result = generator.generate_image_editing(
    prompt="添加一隻貓咪在沙發上睡覺",
    input_image=input_image,
    output_filename="edited_image"
)
```

#### Inpainting（語義遮罩）
```python
# 使用 inpainting 模板
result = generator.generate_with_template(
    template_type="inpainting",
    base_image_description="一張專業肖像照片",
    mask_area="單調的白色背景",
    replacement_content="現代辦公室環境，透過窗戶可以看到城市天際線",
    input_image="path/to/portrait.png",
    output_filename="inpainted_portrait"
)
```

#### 風格轉換
```python
# 將圖片轉換為動漫風格
result = generator.generate_with_template(
    template_type="style_transfer",
    source_image_description="一棟簡單的房子",
    target_style=ImageStyle.ANIME,
    preserve_subject=True,
    input_image="path/to/house.png",
    output_filename="anime_house"
)
```

### 3. 進階合成功能

#### 多圖片合成
```python
# 合成多個元素
result = generator.generate_with_template(
    template_type="multi_image_composition",
    images=[
        "神秘森林背景",
        "智慧巫師角色", 
        "魔法閃光效果"
    ],
    composition_goal="完整的奇幻場景，巫師在森林中被魔法效果包圍",
    blending_style="無縫且富有氛圍感",
    input_image="path/to/background.png",
    output_filename="fantasy_scene"
)
```

#### 迭代精煉
```python
# 第一次生成
result1 = generator.generate_text_to_image(
    prompt="現代廚房，白色櫥櫃，不鏽鋼家電",
    output_filename="kitchen_v1"
)

# 第一次精煉
result2 = generator.generate_image_editing(
    prompt="添加溫暖舒適的燈光和櫃檯上的新鮮水果",
    input_image=result1["image_path"],
    output_filename="kitchen_v2"
)

# 第二次精煉
result3 = generator.generate_image_editing(
    prompt="改為夜晚氛圍，添加蠟燭和櫃檯上的貓咪",
    input_image=result2["image_path"],
    output_filename="kitchen_v3"
)
```

### 4. 專業用例

#### 標誌設計
```python
from ai.prompt_templates import PromptTemplates

# 創建標誌
logo_prompt = PromptTemplates.text_rendering(
    text_content="TECHNOVA",
    design_style="現代極簡主義，帶有幾何元素",
    context="專業科技公司標誌"
)

result = generator.generate_text_to_image(
    prompt=logo_prompt,
    output_filename="company_logo"
)
```

#### 產品攝影
```python
# 專業產品攝影
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="高級咖啡杯",
    style=ImageStyle.PHOTOREALISTIC,
    context="專業產品攝影，電商使用",
    camera_angle=CameraAngle.MACRO,
    lighting="柔和的專業攝影棚燈光",
    composition="乾淨的白色背景，帶有微妙的陰影"
)
```

#### 室內設計視覺化
```python
# 室內設計
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="現代客廳",
    style=ImageStyle.PHOTOREALISTIC,
    context="室內設計視覺化，客戶展示",
    camera_angle=CameraAngle.WIDE_ANGLE,
    lighting="自然光和環境光",
    composition="現代家具，中性色彩，植物裝飾"
)
```

#### 角色設計
```python
# 角色設計
result = generator.generate_with_template(
    template_type="text_to_image",
    subject="奇幻戰士角色",
    style=ImageStyle.ARTISTIC,
    context="角色設計，電玩遊戲使用",
    camera_angle=CameraAngle.CLOSE_UP,
    lighting="戲劇性角色燈光",
    composition="華麗盔甲，魔法劍，神秘森林背景"
)
```

### 5. 批量生成

```python
# 批量生成多張圖片
prompts = [
    "寧靜的山湖日出",
    "夜晚霓虹燈城市街道",
    "和平的花園，盛開的花朵",
    "冬季森林中的舒適小屋",
    "熱帶海灘，棕櫚樹和清澈海水"
]

results = generator.batch_generate(
    prompts=prompts,
    output_prefix="batch_scene"
)

# 檢查結果
successful = sum(1 for r in results if r["success"])
print(f"成功生成 {successful}/{len(prompts)} 張圖片")
```

## 🎯 實際使用範例

### 範例1: 電商產品攝影
```python
from ai import ImageGenerator, ImageStyle, CameraAngle

generator = ImageGenerator()

# 生成產品攝影
products = [
    {
        "name": "無線耳機",
        "style": "現代科技",
        "color": "黑色"
    },
    {
        "name": "智能手錶", 
        "style": "時尚運動",
        "color": "銀色"
    },
    {
        "name": "咖啡機",
        "style": "復古工業",
        "color": "銅色"
    }
]

for i, product in enumerate(products, 1):
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject=f"{product['color']} {product['name']}",
        style=ImageStyle.PHOTOREALISTIC,
        context="電商產品攝影",
        camera_angle=CameraAngle.MACRO,
        lighting="專業攝影棚燈光",
        composition=f"乾淨背景，{product['style']}風格"
    )
    
    if result["success"]:
        print(f"✅ {product['name']} 圖片已生成")
```

### 範例2: 室內設計項目
```python
# 室內設計項目
rooms = [
    {
        "name": "客廳",
        "style": "現代極簡",
        "elements": "灰色沙發，大理石茶几，落地窗"
    },
    {
        "name": "臥室", 
        "style": "北歐風格",
        "elements": "木質家具，白色床單，綠色植物"
    },
    {
        "name": "廚房",
        "style": "工業風",
        "elements": "不鏽鋼家電，混凝土檯面，吊燈"
    }
]

for room in rooms:
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject=f"{room['name']}",
        style=ImageStyle.PHOTOREALISTIC,
        context="室內設計視覺化",
        camera_angle=CameraAngle.WIDE_ANGLE,
        lighting="自然光",
        composition=f"{room['style']}風格，{room['elements']}"
    )
```

### 範例3: 遊戲角色設計
```python
# 遊戲角色設計
characters = [
    {
        "name": "戰士",
        "class": "重裝戰士",
        "weapon": "雙手劍",
        "armor": "板甲"
    },
    {
        "name": "法師",
        "class": "元素法師", 
        "weapon": "法杖",
        "armor": "法袍"
    },
    {
        "name": "盜賊",
        "class": "暗影刺客",
        "weapon": "雙匕首",
        "armor": "皮甲"
    }
]

for char in characters:
    result = generator.generate_with_template(
        template_type="text_to_image",
        subject=f"{char['class']}角色，{char['weapon']}，{char['armor']}",
        style=ImageStyle.ARTISTIC,
        context="遊戲角色設計",
        camera_angle=CameraAngle.CLOSE_UP,
        lighting="戲劇性燈光",
        composition="奇幻背景，魔法效果"
    )
```

## 🛠️ 高級技巧

### 1. 提示詞優化
```python
# 好的提示詞：具體且詳細
good_prompt = "專業產品攝影，高級無線耳機，乾淨白色背景，柔和攝影棚燈光，宏觀角度，電商使用"

# 避免的提示詞：過於簡單
bad_prompt = "耳機照片"
```

### 2. 風格控制
```python
# 使用不同的風格
styles = [
    ImageStyle.PHOTOREALISTIC,  # 照片級真實
    ImageStyle.ARTISTIC,        # 藝術風格
    ImageStyle.ANIME,           # 動漫風格
    ImageStyle.SKETCH,          # 素描風格
    ImageStyle.PAINTING         # 繪畫風格
]
```

### 3. 相機角度控制
```python
# 使用不同的相機角度
angles = [
    CameraAngle.WIDE_ANGLE,     # 廣角
    CameraAngle.MACRO,          # 微距
    CameraAngle.CLOSE_UP,       # 特寫
    CameraAngle.LOW_ANGLE,      # 低角度
    CameraAngle.BIRD_EYE        # 鳥瞰
]
```

### 4. 錯誤處理
```python
try:
    result = generator.generate_text_to_image(
        prompt="你的提示詞",
        output_filename="test"
    )
    
    if result["success"]:
        print("✅ 生成成功")
        print(f"圖片路徑: {result['image_path']}")
    else:
        print(f"❌ 生成失敗: {result['error']}")
        
except Exception as e:
    print(f"❌ 發生錯誤: {e}")
```

## 📁 輸出管理

### 查看生成的圖片
```bash
# 查看 outputs 目錄
ls -la outputs/

# 使用 Finder 打開（Mac）
open outputs/

# 使用文件管理器打開（Windows）
explorer outputs
```

### 清理輸出文件
```bash
# 清理所有生成的圖片
rm outputs/*.png

# 或使用 Makefile
make clean
```

## 🎉 完整工作流程

### 1. 項目設置
```bash
# 克隆項目
git clone <your-repo>
cd dev-gemini-api

# 安裝依賴
pip install -r requirements.txt

# 設置 API 密鑰
python setup_api_key.py
```

### 2. 開發和測試
```bash
# 運行測試
python test_setup.py

# 查看演示
python demo.py

# 運行教程
python tutorials/01_text_to_image.py
```

### 3. 生產使用
```bash
# 使用 Docker
make docker-run

# 或直接運行
python your_script.py
```

## 🆘 常見問題解決

### 1. API 密鑰問題
```bash
# 檢查密鑰設置
cat .env

# 重新設置
python setup_api_key.py
```

### 2. 圖片生成失敗
- 檢查提示詞是否過於複雜
- 嘗試簡化描述
- 檢查 API 密鑰是否有效

### 3. 記憶體不足
- 減少批量生成數量
- 使用 Docker 限制記憶體使用

### 4. 圖片質量問題
- 使用更詳細的提示詞
- 選擇合適的風格和角度
- 提供更多上下文信息

---

**現在你已經掌握了所有功能的使用方法！開始創建你的圖片吧！** 🎨✨
