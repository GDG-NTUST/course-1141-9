# Nano Banana Test Suite

完整的測試套件，覆蓋所有模組功能。

## 快速開始

```bash
# 安裝測試依賴
uv sync --extra dev

# 執行所有測試
pytest

# 執行測試並生成覆蓋率報告
pytest --cov=nano_banana --cov-report=html
```

## 測試覆蓋範圍

### 核心模組 (core/)

- ✅ `test_config.py` - 配置管理測試 (9 個測試)
  - 環境變數載入
  - 必要參數驗證
  - 預設值處理
  - 日誌配置

### API 模組 (api/)

- ✅ `test_client.py` - Gemini API 客戶端測試 (11 個測試)
  - 客戶端初始化
  - 文字轉圖像生成
  - 圖像轉換
  - 錯誤處理
  - 多圖像處理

- ✅ `test_demo.py` - 命令列工具測試 (9 個測試)
  - 目錄管理
  - 路徑生成
  - CLI 參數處理
  - 多圖像輸入

### Discord 模組 (discord/)

- ✅ `test_bot.py` - Discord 機器人測試 (10 個測試)
  - 斜線命令
  - 訊息監聽
  - 圖像附件處理
  - 錯誤處理

- ✅ `test_utils.py` - 工具函數測試 (5 個測試)
  - 圖像下載
  - 網路錯誤處理
  - 格式支援

## 總計

**44 個測試** 覆蓋所有主要功能模組

## 執行特定測試

```bash
# 測試特定模組
pytest tests/core/

# 測試特定文件
pytest tests/api/test_client.py

# 測試特定類別
pytest tests/api/test_client.py::TestNanoBananaClient

# 測試特定函數
pytest tests/api/test_client.py::TestNanoBananaClient::test_generate_text_to_image

# 使用關鍵字過濾
pytest -k "client"
```

## 使用測試腳本

```bash
# 執行所有測試（詳細輸出）
python run_tests.py all

# 快速測試（無覆蓋率）
python run_tests.py fast

# 生成 HTML 覆蓋率報告
python run_tests.py coverage

# 執行特定測試
python run_tests.py specific tests/core/test_config.py
```

## 查看覆蓋率報告

生成 HTML 報告後：

```bash
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

## 測試編寫指南

### 測試命名規範

- 測試文件：`test_*.py`
- 測試類別：`Test*`
- 測試函數：`test_*`

### 測試結構（AAA 模式）

```python
def test_example():
    # Arrange - 準備測試資料
    client = Client(api_key="test")
    
    # Act - 執行測試
    result = client.method()
    
    # Assert - 驗證結果
    assert result == expected
```

### 異步測試

```python
@pytest.mark.asyncio
async def test_async_method():
    result = await async_method()
    assert result is not None
```

### 使用 Mock

```python
from unittest.mock import patch, MagicMock

@patch('module.external_api')
def test_with_mock(mock_api):
    mock_api.return_value = "mocked"
    result = function_using_api()
    assert result == "expected"
```

## 共用 Fixtures

在 `conftest.py` 中定義：

- `mock_env_vars` - 模擬環境變數
- `sample_image` - 測試用 PIL 圖像
- `sample_image_bytes` - 圖像位元組
- `temp_image_path` - 臨時圖像文件
- `mock_genai_client` - Mock GenAI 客戶端
- `mock_discord_context` - Mock Discord 上下文
- `mock_discord_message` - Mock Discord 訊息

## CI/CD 整合

### GitHub Actions 示例

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

## 故障排除

### 測試失敗

1. 確認已安裝測試依賴：`uv sync --extra dev`
2. 檢查環境變數是否正確設置
3. 確認 Python 版本 >= 3.13

### 覆蓋率問題

1. 確認源碼路徑正確：`src/nano_banana`
2. 檢查 `pytest.ini` 配置
3. 使用 `--cov-report=term-missing` 查看未覆蓋行

### Import 錯誤

1. 確認在專案根目錄執行測試
2. 檢查 `pythonpath` 設置：`pythonpath = ["src"]`
3. 確認 `__init__.py` 文件存在

## 貢獻

新增測試時：

1. 保持測試獨立性
2. 使用描述性測試名稱
3. 添加文檔字符串
4. Mock 外部依賴
5. 測試邊界情況
6. 保持測試簡潔

## 參考資源

- [Pytest 文檔](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Coverage.py](https://coverage.readthedocs.io/)
