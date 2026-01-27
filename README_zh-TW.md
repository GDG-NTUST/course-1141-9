<div align="center">

# 🍌 一起在 Discord 玩 AI 奈米香蕉 🍌

[<img src=".github/assets/gdg-logo.png" width="400" alt="GDG | NTUST">](https://gdg-ntust.org/)

<br>[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Nano Banana](https://img.shields.io/badge/Nano%20Banana-yellow?style=for-the-badge&logo=gamebanana&logoColor=white)](https://ai.google.dev/)
[![Google Gemini](https://img.shields.io/badge/gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)](https://ai.google.dev/)

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/)
[![py-cord](https://img.shields.io/badge/pycord-2.7+-blue?style=for-the-badge&logo=discord&logoColor=ffffff)](https://github.com/Pycord-Development/pycord)
[![pydantic-settings](https://img.shields.io/badge/pydantic--settings-2.12+-blue?style=for-the-badge&logo=pydantic)](https://pydantic.dev/latest/)

**[English](README.md)**

</div>

這是一個學習專案，教您怎麼用 Google Gemini 的 **Nano Banana** 做影像生成。
您可以學到模組化的程式架構、標準的 Python 寫作風格、Discord 機器人和非同步程式設計的實用技巧。

## 📋 目錄

- [專案概述](#專案概述)
- [功能特性](#功能特性)
- [專案架構](#專案架構)
- [系統需求](#系統需求)
- [安裝與設定](#安裝與設定)
- [環境配置](#環境配置)
- [使用方法](#使用方法)
- [測試](#測試)
- [模組詳情](#模組詳情)
- [開發指南](#開發指南)

## 專案概述

**Nano Banana** 是 Google 開發的人工智慧影像生成與編輯工具，建立在 Gemini 的基礎之上，我們可以在這個專案學到：

- 遵循簡潔架構原則的模組化程式設計
- Python 非同步程式設計（`asyncio`）
- Google Gemini API 進行 AI 影像生成與轉換
- Discord 機器人實現互動式影像生成
- 環境變數配置
- 結構化日誌記錄和錯誤處理

## 功能特性

- 🎨 **文字轉影像生成** - 使用文字提示生成圖像
- 🔄 **圖像轉換** - 根據文字指令轉換現有圖像
- 💬 **Discord 互動** - 支援斜線命令和訊息型互動
- 📨 **非同步處理** - 採用 async / await 模式實現非阻塞互動
- ⚙️ **可配置 AI 模型** - 支援切換不同的 Gemini 模型
- 📊 **結構化日誌記錄** - 具有時間戳和級別的詳細日誌
- 🔐 **環境變數配置** - 安全管理 API 金鑰和權杖

## 專案架構

```bash
nano_banana/
├── __init__.py
├── main.py                # 應用程式入口點
├── core/
│   ├── __init__.py
│   └── config.py          # 配置和日誌設定
├── api/
│   ├── __init__.py
│   ├── client.py          # Google Gemini API 客戶端（非同步）
│   └── demo/
│       ├── __init__.py
│       ├── demo.py        # 命令行演示腳本
│       └── outputs/       # 生成圖像目錄
└── discord/
    ├── __init__.py
    ├── bot.py             # Discord 機器人實作
    └── utils.py           # Discord 機器人輔助工具
```

### 架構層次說明

**配置層（`core/`）**

- `config.py`：基於 Pydantic 的設定管理
- 從 `.env` 檔案載入環境變數
- 統一管理 API 金鑰、權杖和模型設定
- 內置日誌配置，支援自訂級別

**API 層（`api/`）**

- `client.py`：Google Gemini API 非同步客戶端
- 同時支援文字轉圖像和圖像轉圖像操作
- 完整的錯誤處理和響應解析
- 使用 PIL（Pillow）進行圖像處理
- `demo.py`：獨立演示腳本，支援命令行參數

**Discord 整合層（`discord/`）**

- `bot.py`：支援斜線命令和訊息監聽的 Discord 機器人
- 同時支援命令型（`/畫圖`）和訊息型互動
- 圖像附件處理和轉換
- 豐富的文字和圖像回應
- `utils.py`：非同步下載 Discord CDN 圖像

## 系統需求

| 需求項 | 版本 |
| -------- | ------ |
| Python | 3.13+ |
| uv | 最新版本（套件管理器） |

### 相依套件

- **google-genai** (≥1.60.0) - Google Gemini API 客戶端
- **pydantic-settings** (≥2.12.0) - 配置管理
- **py-cord** (≥2.7.0) - Discord 機器人
- **pillow** (≥12.1.0) - 圖像處理

## 安裝與設定

### 前置需求

確保已安裝 Python 3.13+ 和 pip：

```bash
python --version  # 應顯示 3.13 或更高版本
pip --version
```

### 分步安裝指南

#### 1. 安裝 uv 套件管理器

```bash
pip install uv
```

[uv](https://github.com/astral-sh/uv) 是一個快速的 Python 套件安裝工具，用 Rust 編寫。

#### 2. 複製專案儲存庫

```bash
git clone https://github.com/GDG-NTUST/course-1141-9.git
cd nano-banana
```

#### 3. 安裝相依套件

```bash
uv sync
```

此命令會安裝 `pyproject.toml` 中指定的所有相依套件，並生成 `uv.lock` 以確保可重複安裝。

## 環境配置

### 環境變數設定

在專案根目錄建立 `.env` 檔案（可從 `.env.example` 複製）：

```env
# Google Gemini API 配置
GOOGLE_API_KEY=your_google_api_key_here

# Discord 機器人配置
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_server_id

# 應用程式設定
LOG_LEVEL=INFO
MODEL_NAME=gemini-2.5-flash-image
SYSTEM_PROMPT=你是一個有幫助的 AI 助手，可以根據用戶的請求生成圖像。
```

#### 配置參數說明

| 變數名稱 | 必填 | 預設值 | 說明 |
| -------- | ------ | -------- | ------ |
| `GOOGLE_API_KEY` | ✅ 是 | - | [Google AI Studio](https://ai.dev) 的 API 金鑰 |
| `DISCORD_TOKEN` | ✅ 是 | - | Discord 開發者入口網站的機器人權杖 |
| `DISCORD_GUILD_ID` | ✅ 是 | - | 機器人執行的 Guild ID |
| `LOG_LEVEL` | ❌ 否 | INFO | 日誌級別（DEBUG、INFO、WARNING、ERROR、CRITICAL） |
| `MODEL_NAME` | ❌ 否 | gemini-2.5-flash-image | Gemini 模型識別符 |
| `SYSTEM_PROMPT` | ❌ 否 | 空 | 影像生成的系統提示字首 |

### 獲取 API 金鑰

**Google Gemini API 金鑰：**

1. 前往 [Google AI Studio](https://ai.dev)
2. 點選「取得 API 金鑰」
3. 建立新的 API 金鑰
4. 將金鑰複製到 `.env` 中的 `GOOGLE_API_KEY`

**Discord 機器人權杖：**

1. 前往 [Discord 開發者入口網站](https://discord.com/developers/applications)
2. 建立新應用程式
3. 前往「Bot」部分並建立機器人
4. 複製權杖到 `.env` 中的 `DISCORD_TOKEN`
5. 啟用必要的意圖（訊息內容等）
6. 使用適當的權限邀請機器人加入您的伺服器

## 使用方法

### Discord 機器人

啟動 Discord 機器人：

```bash
# 使用 uv
cd src/
uv run python -m nano_banana.main
```

機器人將連線到 Discord 並回應命令和訊息。

#### Discord 命令

**斜線命令：**

```bash
/畫圖 <提示詞>
```

根據您的文字提示生成圖像。

範例：

```bash
/畫圖 一個寧靜的山湖景色，夕陽下山
```

**訊息型（限制於指定的伺服器）：**

- 發送一條文字訊息，可選擇附上圖像
- 機器人會根據您的文字轉換圖像或生成新圖像
- 自動下載並處理附件圖像

### 命令行演示

執行互動式演示腳本，支援各種選項：

```bash
# 基本文字轉影像生成
cd src/
uv run python -m nano_banana.api.demo.demo -p "一個美麗的海邊日落"

# 圖像轉換
uv run python -m nano_banana.api.demo.demo -p "讓它更鮮豔" -i ./image.png

# 多張圖像
uv run python -m nano_banana.api.demo.demo -p "結合這些風格" -i image1.png image2.png

# 自訂 API 金鑰
uv run python -m nano_banana.api.demo.demo -k "your-api-key" -p "您的提示詞"
```

#### 演示腳本參數

| 短旗 | 長旗 | 必需 | 說明 |
| ---- | ---- | ---- | ---- |
| `-p` | `--prompt` | ✅ 是 | 影像生成或轉換的文字提示 |
| `-i` | `--image` | ❌ 否 | 輸入圖像的路徑（可多個） |
| `-k` | `--key` | ❌ 否 | Google API 金鑰（覆蓋環境變數） |

**輸出：** 生成的圖像保存到 `src/nano_banana/api/demo/outputs/`，檔名使用 UUID 格式。

## 測試

此專案包含所有模組的全面測試覆蓋。

### 測試結構

```bash
tests/
├── __init__.py
├── conftest.py           # 共用夹具和配置
├── core/
│   ├── __init__.py
│   └── test_config.py    # 配置模組測試
├── api/
│   ├── __init__.py
│   ├── test_client.py    # API 客戶端測試
│   └── test_demo.py      # Demo 腳本測試
└── discord/
    ├── __init__.py
    ├── test_bot.py       # Discord 機器人測試
    └── test_utils.py     # 工具函數測試
```

### 執行測試

#### 安裝測試依賴

```bash
# 安裝開發依賴，包含 pytest
uv sync --extra dev
```

#### 執行所有測試

```bash
# 執行所有測試並生成覆蓋率報告
pytest

# 執行測試並顯示詳細輸出
pytest -v

# 執行特定測試檔案
pytest tests/core/test_config.py

# 執行特定測試類別
pytest tests/api/test_client.py::TestNanoBananaClient

# 執行特定測試函數
pytest tests/api/test_client.py::TestNanoBananaClient::test_generate_text_to_image
```

#### 覆蓋率報告

```bash
# 生成 HTML 覆蓋率報告
pytest --cov=nano_banana --cov-report=html

# 查看覆蓋率報告
# 在瀏覽器中開啟 htmlcov/index.html

# 生成終端機覆蓋率報告
pytest --cov=nano_banana --cov-report=term-missing

# 生成 XML 覆蓋率報告（用於 CI/CD）
pytest --cov=nano_banana --cov-report=xml
```

### 測試類別

#### 配置測試（`test_config.py`）

- ✅ 有效環境變數載入
- ✅ 缺少必要認證處理
- ✅ 預設值備援
- ✅ 不區分大小寫的環境變數
- ✅ 額外變數過濾
- ✅ 日誌配置

#### API 客戶端測試（`test_client.py`）

- ✅ 客戶端初始化
- ✅ 文字轉圖像生成
- ✅ 圖像轉圖像轉換
- ✅ 多張圖像處理
- ✅ 空響應處理
- ✅ 缺少圖像資料處理
- ✅ API 異常處理
- ✅ 圖像位元組處理

#### Discord 機器人測試（`test_bot.py`）

- ✅ 斜線命令處理
- ✅ 機器人訊息過濾
- ✅ 伺服器 ID 過濾
- ✅ 純文字訊息處理
- ✅ 單張圖像附件處理
- ✅ 多張圖像附件
- ✅ 非圖像附件過濾
- ✅ 錯誤處理和用戶反饋
- ✅ 機器人就緒事件

#### 工具測試（`test_utils.py`）

- ✅ 成功下載圖像
- ✅ 網路錯誤處理
- ✅ 無效圖像資料處理
- ✅ 空內容處理
- ✅ 不同圖像格式支援

#### Demo 腳本測試（`test_demo.py`）

- ✅ 輸出目錄創建
- ✅ 唯一路徑生成
- ✅ 文字轉圖像 CLI
- ✅ 圖像轉換 CLI
- ✅ 多張圖像輸入
- ✅ 自定義 API 金鑰覆寫
- ✅ 缺少認證處理

### 測試固件

`conftest.py` 中的共用固件：

- `mock_env_vars`：模擬環境變數
- `sample_image`：創建測試 PIL 圖像
- `sample_image_bytes`：將圖像轉換為位元組
- `temp_image_path`：臨時圖像檔案
- `mock_genai_client`：模擬 Google GenAI 客戶端
- `mock_discord_context`：模擬 Discord 上下文
- `mock_discord_message`：模擬 Discord 訊息

### 編寫新測試

添加新功能時，請遵循以下指南：

1. **創建測試檔案**與模組名稱匹配：

   ```python
   src/nano_banana/new_module.py → tests/test_new_module.py
   ```

2. **使用描述性測試名稱：**

   ```python
   def test_function_name_expected_behavior():
       """測試描述。"""
   ```

3. **遵循 AAA 模式：**

   ```python
   def test_example():
       # Arrange: 設置測試資料
       client = Client(api_key="test")
       
       # Act: 執行代碼
       result = client.do_something()
       
       # Assert: 驗證結果
       assert result == expected_value
   ```

4. **模擬外部依賴：**

   ```python
   @patch('module.external_api')
   def test_with_mock(mock_api):
       mock_api.return_value = "mocked_data"
       # 測試代碼
   ```

5. **測試非同步函數：**

   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_function()
       assert result is not None
   ```

### 持續整合

GitHub Actions 工作流程示例：

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install uv
          uv sync --extra dev
      - name: Run tests
        run: pytest --cov=nano_banana --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 模組詳情

### `config.py` - 配置管理

```python
from nano_banana.core.config import Settings, logger

settings = Settings()
logger.info(f"使用模型: {settings.MODEL_NAME}")
```

**特性：**

- 基於 Pydantic 的設定驗證
- 從 `.env`、`../.env` 檔案載入
- 環境變數名稱不區分大小寫
- 自動日誌設定，帶有時間戳格式
- 啟動時驗證必需的認證資訊

### `client.py` - Gemini API 客戶端

```python
from nano_banana.api.client import NanoBananaClient

client = NanoBananaClient(api_key=settings.GOOGLE_API_KEY)

# 文字轉圖像
text, image = await client.generate(prompt="一隻戴著帽子的貓")

# 圖像轉換
text, image = await client.generate(
    prompt="讓它呈現賽博龐克風格",
    images=[pil_image]
)
```

**主要方法：**

- `__init__(api_key, model_name)` - 初始化客戶端
- `generate(prompt, images=None)` - 非同步生成/轉換
  - 返回：`Tuple[str, PIL.Image.Image]`（響應文字和圖像）
  - 支援單個或多個輸入圖像

**特性：**

- 完全非同步，基於 `asyncio`
- 自動從 API 響應中提取圖像資料
- 使用 `asyncio.to_thread()` 進行線程安全的圖像處理
- 全面的錯誤日誌記錄
- 支援單個和批次圖像操作

### `bot.py` - Discord 機器人

**斜線命令處理器：**

```python
@bot.slash_command(name='畫圖', description='畫圖給我')
async def draw(ctx: discord.ApplicationContext, prompt: str) -> None:
```

**訊息監聽器：**

- 處理直接訊息和伺服器訊息（可按伺服器 ID 過濾）
- 檢測圖像附件並下載
- 在用戶輸入前加上系統提示
- 發送格式化回應，包含生成的圖像

**特性：**

- 非阻塞式非同步操作
- 從 Discord CDN 下載圖像
- 用戶友好的錯誤訊息處理
- 就緒事件日誌記錄
- 可配置的伺服器過濾

### `demo.py` - CLI 演示腳本

獨立腳本展示帶有 CLI 參數的影像生成：

- 使用 `argparse` 進行參數解析
- 支援多個輸入圖像
- 自動建立輸出目錄
- 將圖像格式轉換為 RGB
- 使用唯一命名保存生成的圖像

## 開發指南

### 專案結構最佳實踐

1. **關注點分離**
   - 配置隔離在 `core/`
   - API 邏輯與 Discord 整合分離
   - 演示腳本在專用的 `demo/` 子目錄

2. **非同步優先設計**
   - 所有 I/O 操作都是非阻塞的
   - 整個專案貫徹 async/await 模式
   - 對 CPU 密集型任務使用線程池

3. **錯誤處理**
   - 每層都有全面的日誌記錄
   - 驗證必需的認證資訊
   - 向用戶提供友好的錯誤訊息

4. **程式碼品質**
   - `pyproject.toml` 中的 Ruff linter 配置
   - Black formatter 確保風格一致
   - McCabe 複雜度限制
   - 全面的型別提示

### 執行 Lint 和格式化

```bash
# 格式化程式碼
ruff format .

# 執行 Lint 並自動修復
ruff check . --fix
```

### 專案配置（`pyproject.toml`）

- **Python 版本：** 3.13+
- **Ruff 設定：** 嚴格 Lint，自訂忽略規則
- **Black：** 80 字符行長度，單引號
- **McCabe：** 最大複雜度 10

## 常見問題排除

### 常見問題

**"GOOGLE_API_KEY, DISCORD_TOKEN and DISCORD_GUILD_ID
must be set in environment variables." 錯誤：**

- 確保 `.env` 檔案存在於專案根目錄
- 驗證 API 金鑰和權杖正確貼上
- 檢查環境變數是否正確載入

**"Empty response from Gemini model." 錯誤：**

- 驗證 API 金鑰配額是否足夠
- 檢查網際網路連線
- 確保提示詞有效且非空

**Discord 機器人不回應：**

- 驗證機器人在 Discord 伺服器中處於線上
- 檢查 Discord 權杖是否正確
- 確保機器人啟用了訊息內容意圖
- 驗證伺服器設定中的機器人權限 (在該文字頻道是否有有權限？)

**圖像處理錯誤：**

- 確保輸入圖像格式有效（PNG、JPG 等）
- 檢查圖像檔案大小是否合理
- 驗證圖像路徑正確且可訪問

### 啟用調試日誌

在 `.env` 中新增：

```env
LOG_LEVEL=DEBUG
```

這將提供詳細的日誌資訊以供排除故障。

## 未來增強

- 使用 FastAPI 建立 REST API 以進行網路整合
- 資料庫整合以進行歷史記錄追蹤
- 進階圖像處理和濾鏡
- 速率限制和配額管理
- 帶有驗證的多用戶支援
- 圖像庫和共享功能
- 多張圖像的批次處理

## 授權

MIT

## 貢獻指南

歡迎貢獻！請隨時提交拉取請求或開啟問題。

## 支援

如有任何問題、疑問或建議，請在儲存庫中開啟問題。
