<div align="center">

# 🍌 Playing with Nano Banana on Discord Together 🍌

[<img src=".github/assets/gdg-logo.png" width="400" alt="GDG | NTUST">](https://gdg-ntust.org/)

<br>[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Nano Banana](https://img.shields.io/badge/Nano%20Banana-yellow?style=for-the-badge&logo=gamebanana&logoColor=white)](https://ai.google.dev/)
[![Google Gemini](https://img.shields.io/badge/gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)](https://ai.google.dev/)

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/)
[![py-cord](https://img.shields.io/badge/pycord-2.7+-blue?style=for-the-badge&logo=discord&logoColor=ffffff)](https://github.com/Pycord-Development/pycord)
[![pydantic-settings](https://img.shields.io/badge/pydantic--settings-2.12+-blue?style=for-the-badge&logo=pydantic)](https://pydantic.dev/latest/)

**[Traditional Chinese](README_zh-TW.md)**

</div>

This is a tutorial project demonstrating clean architecture patterns for
**Nano Banana** image generation using Google Gemini.
This project showcases best practices for building scalable,
maintainable Python applications with Discord integration and async support.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Requirements](#requirements)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Testing](#testing)
- [Module Details](#module-details)
- [Development](#development)

## Overview

**Nano Banana** is an educational project that demonstrates:

- Clean architecture principles with interface-based design
- Asynchronous Python programming with `asyncio`
- Google Gemini API integration for AI image generation and transformation
- Discord bot integration for interactive image generation
- Environment-based configuration management
- Structured logging and error handling
- Async HTTP operations for image downloading

The project name "Nano Banana" references the Google Generative AI API,
highlighting the creative and experimental nature of the project.

## Features

✨ **Core Capabilities:**

- 🎨 **Text-to-Image Generation** - Create images from text prompts
- 🔄 **Image-to-Image Transformation** -
   Transform existing images based on text instructions
- 💬 **Discord Integration** - Use slash commands and message-based interactions
- 📨 **Async Processing** - Non-blocking async / await pattern for responsive interactions
- ⚙️ **Configurable AI Models** - Switch between different Gemini models
- 📊 **Structured Logging** - Detailed logging with timestamp and level information
- 🔐 **Environment-Based Configuration** - Secure management of API keys and tokens

## Project Architecture

```bash
nano_banana/
├── __init__.py
├── main.py                # Application entry point
├── core/
│   ├── __init__.py
│   └── config.py          # Configuration and logging setup
├── api/
│   ├── __init__.py
│   ├── client.py          # Google Gemini API client (async)
│   └── demo/
│       ├── __init__.py
│       ├── demo.py        # Command-line demo script
│       └── outputs/       # Generated images directory
└── discord/
    ├── __init__.py
    ├── bot.py             # Discord bot implementation
    └── utils.py           # Helper utilities for Discord bot
```

### Architecture Layers

**Configuration Layer (`core/`)**

- `config.py`: Pydantic-based settings management
- Loads environment variables from `.env` file
- Centralized configuration for API keys, tokens, discord, and model settings
- Logging configuration with customizable levels

**API Layer (`api/`)**

- `client.py`: Google Gemini API client with async support
- Handles both text-to-image and image-to-image operations
- Robust error handling and response parsing
- Image processing with PIL (Pillow)
- `demo.py`: Standalone demo script with CLI argument support

**Discord Integration Layer (`discord/`)**

- `bot.py`: Discord bot with slash commands and message listeners
- Supports both command-based (`/畫圖`) and message-based interactions
- Image attachment handling and transformation
- Rich text and image responses
- `utils.py`: Async image downloading from Discord CDN

## Requirements

| Requirement |          Version         |
|-------------|--------------------------|
|    Python   |           3.13+          |
|     uv      | Latest (package manager) |

### Dependencies

- **google-genai** (≥1.60.0) - Google Gemini API client
- **pillow** (≥12.1.0) - Image processing
- **pydantic-settings** (≥2.12.0) - Configuration management
- **py-cord** (≥2.7.0) - Discord bot

## Installation & Setup

### Prerequisites

Ensure Python 3.13+ and pip are installed:

```bash
python --version  # Should be 3.13 or higher
pip --version
```

### Step-by-Step Installation

#### 1. Install uv Package Manager

```bash
pip install uv
```

[uv](https://github.com/astral-sh/uv) is a fast Python package installer
and resolver, written in Rust.

#### 2. Clone the Repository

```bash
git clone <repository-url>
cd nano-banana
```

#### 3. Install Dependencies

```bash
uv sync
```

This installs all dependencies specified in `pyproject.toml`
and creates `uv.lock` for reproducible installs.

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_server_id

# Application Settings
LOG_LEVEL=INFO
MODEL_NAME=gemini-2.5-flash-image
SYSTEM_PROMPT=You are a helpful AI assistant
that generates images based on user requests.
```

#### Configuration Parameters

| Variable | Required | Default | Description |
| ---------- | ---------- | --------- | ------------- |
| `GOOGLE_API_KEY` | ✅ Yes | - | API key from [Google AI Studio](https://ai.dev/) |
| `DISCORD_TOKEN` | ✅ Yes | - | Bot token from Discord Developer Portal |
| `DISCORD_GUILD_ID` | ✅ Yes | - | Guild ID that the bot activate |
| `LOG_LEVEL` | ❌ No | INFO | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `MODEL_NAME` | ❌ No | gemini-2.5-flash-image | Gemini model identifier |
| `SYSTEM_PROMPT` | ❌ No | Empty | System prompt prefix for image generation |

### Getting API Keys

**Google Gemini API Key:**

1. Visit [Google AI Studio](https://ai.dev)
2. Click "Get API key"
3. Create a new API key
4. Copy the key to `GOOGLE_API_KEY` in `.env`

**Discord Bot Token:**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section and create a bot
4. Copy the token to `DISCORD_TOKEN` in `.env`
5. Enable necessary intents (Message Content, etc.)
6. Invite bot to your server with appropriate permissions

## Usage

### Discord Bot

Start the Discord bot:

```bash
# Using uv
cd src/
uv run python -m nano_banana.main
```

The bot will connect to Discord and respond to commands and messages.

#### Discord Commands

**Slash Command:**

```bash
/畫圖 <prompt>
```

Generates an image based on your text prompt.

Example:

```bash
/畫圖 A serene landscape with mountains and sunset
```

**Message-Based (in specific guild):**

- Send a text message with optional image attachments
- Bot will transform the images or generate new ones based on your text
- Automatically downloads and processes attached images

### Command-Line Demo

Run the interactive demo script with various options:

```bash
# Basic text-to-image generation
cd src/
uv run python -m nano_banana.api.demo.demo -p "A beautiful sunset over the ocean"

# Image transformation
uv run python -m nano_banana.api.demo.demo -p "Make it more vibrant" -i ./image.png

# Multiple images
uv run python -m nano_banana.api.demo.demo -p "Combine these styles" -i image1.png image2.png

# Custom API key
uv run python -m nano_banana.api.demo.demo -k "your-api-key" -p "Your prompt"
```

#### Demo Script Arguments

| Flag | Long Form | Required | Description |
| ------ | ----------- | ---------- | ------------- |
| `-p` | `--prompt` | ✅ Yes | Text prompt for generation or transformation |
| `-i` | `--image` | ❌ No | Path(s) to input image(s) |
| `-k` | `--key` | ❌ No | Google API key (overrides environment variable) |

**Output:** Generated images are saved to `src/nano_banana/api/demo/outputs/`
with UUID-based filenames.

## Testing

This project includes comprehensive test coverage for all modules.

### Test Structure

```bash
tests/
├── __init__.py
├── conftest.py           # Shared fixtures and configuration
├── core/
│   ├── __init__.py
│   └── test_config.py    # Configuration module tests
├── api/
│   ├── __init__.py
│   ├── test_client.py    # API client tests
│   └── test_demo.py      # Demo script tests
└── discord/
    ├── __init__.py
    ├── test_bot.py       # Discord bot tests
    └── test_utils.py     # Utility function tests
```

### Running Tests

#### Install Test Dependencies

```bash
# Install development dependencies including pytest
uv sync --extra dev
```

#### Run All Tests

```bash
# Run all tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/core/test_config.py

# Run specific test class
pytest tests/api/test_client.py::TestNanoBananaClient

# Run specific test function
pytest tests/api/test_client.py::TestNanoBananaClient::test_generate_text_to_image
```

#### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=nano_banana --cov-report=html

# View coverage report
# Open htmlcov/index.html in your browser

# Generate terminal coverage report
pytest --cov=nano_banana --cov-report=term-missing

# Generate XML coverage report (for CI/CD)
pytest --cov=nano_banana --cov-report=xml
```

### Test Categories

#### Configuration Tests (`test_config.py`)

- ✅ Valid environment variable loading
- ✅ Missing required credentials handling
- ✅ Default value fallbacks
- ✅ Case-insensitive environment variables
- ✅ Extra variable filtering
- ✅ Logging configuration

#### API Client Tests (`test_client.py`)

- ✅ Client initialization
- ✅ Text-to-image generation
- ✅ Image-to-image transformation
- ✅ Multiple image processing
- ✅ Empty response handling
- ✅ Missing image data handling
- ✅ API exception handling
- ✅ Image bytes processing

#### Discord Bot Tests (`test_bot.py`)

- ✅ Slash command handling
- ✅ Bot message filtering
- ✅ Guild ID filtering
- ✅ Text-only message processing
- ✅ Single image attachment handling
- ✅ Multiple image attachments
- ✅ Non-image attachment filtering
- ✅ Error handling and user feedback
- ✅ On-ready event

#### Utility Tests (`test_utils.py`)

- ✅ Successful image download
- ✅ Network error handling
- ✅ Invalid image data handling
- ✅ Empty content handling
- ✅ Different image format support

#### Demo Script Tests (`test_demo.py`)

- ✅ Output directory creation
- ✅ Unique path generation
- ✅ Text-to-image CLI
- ✅ Image transformation CLI
- ✅ Multiple image inputs
- ✅ Custom API key override
- ✅ Missing credentials handling

### Test Fixtures

Shared fixtures in `conftest.py`:

- `mock_env_vars`: Mock environment variables
- `sample_image`: Create test PIL images
- `sample_image_bytes`: Convert images to bytes
- `temp_image_path`: Temporary image files
- `mock_genai_client`: Mock Google GenAI client
- `mock_discord_context`: Mock Discord context
- `mock_discord_message`: Mock Discord messages

### Writing New Tests

When adding new features, follow these guidelines:

1. **Create test file** matching the module name:

   ```python
   src/nano_banana/new_module.py → tests/test_new_module.py
   ```

2. **Use descriptive test names:**

   ```python
   def test_function_name_expected_behavior():
       """Test description."""
   ```

3. **Follow AAA pattern:**

   ```python
   def test_example():
       # Arrange: Set up test data
       client = Client(api_key="test")
       
       # Act: Execute the code
       result = client.do_something()
       
       # Assert: Verify the results
       assert result == expected_value
   ```

4. **Mock external dependencies:**

   ```python
   @patch('module.external_api')
   def test_with_mock(mock_api):
       mock_api.return_value = "mocked_data"
       # Test code
   ```

5. **Test async functions:**

   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await async_function()
       assert result is not None
   ```

### Continuous Integration

Example GitHub Actions workflow:

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

## Module Details

### `config.py` - Configuration Management

```python
from nano_banana.core.config import Settings, logger

settings = Settings()
logger.info(f"Using model: {settings.MODEL_NAME}")
```

**Features:**

- Pydantic-based settings validation
- Loads from `.env`, `../.env` files
- Case-insensitive environment variable matching
- Automatic logging setup with timestamp format
- Validation of required credentials on startup

### `client.py` - Gemini API Client

```python
from nano_banana.api.client import NanoBananaClient

client = NanoBananaClient(api_key=settings.GOOGLE_API_KEY)

# Text-to-image
text, image = await client.generate(prompt="A cat wearing a hat")

# Image transformation
text, image = await client.generate(
    prompt="Make it cyberpunk style",
    images=[pil_image]
)
```

**Key Methods:**

- `__init__(api_key, model_name)` - Initialize the client
- `generate(prompt, images=None)` - Async generation/transformation
  - Returns: `Tuple[str, PIL.Image.Image]` (response text and image)
  - Supports single or multiple input images

**Features:**

- Fully asynchronous with `asyncio`
- Automatic image data extraction from API response
- Thread-safe image processing with `asyncio.to_thread()`
- Comprehensive error logging
- Handles both single and batch image operations

### `bot.py` - Discord Bot

**Slash Command Handler:**

```python
@bot.slash_command(name='畫圖', description='畫圖給我')
async def draw(ctx: discord.ApplicationContext, prompt: str) -> None:
```

**Message Listener:**

- Processes direct messages and guild messages (filtered by guild ID)
- Detects image attachments and downloads them
- Prepends system prompt to user input
- Sends formatted responses with generated images

**Features:**

- Non-blocking async operations
- Image downloading from Discord CDN
- Error handling with user-friendly messages
- Ready event logging
- Configurable guild filtering

### `demo.py` - CLI Demo Script

Standalone script demonstrating image generation with CLI arguments:

- Argument parsing with `argparse`
- Support for multiple input images
- Auto-creation of output directory
- Image format conversion to RGB
- Generated image persistence with unique naming

## Development

### Project Structure Best Practices

1. **Separation of Concerns**
   - Configuration isolated in `core/`
   - API logic separated from Discord integration
   - Demo script in dedicated `demo/` subdirectory

2. **Async-First Design**
   - All I/O operations are non-blocking
   - Proper async/await patterns throughout
   - Thread pool usage for CPU-bound tasks

3. **Error Handling**
   - Comprehensive logging at each layer
   - Validation of required credentials
   - Graceful error messages to users

4. **Code Quality**
   - Ruff linter configuration in `pyproject.toml`
   - Black formatter for consistent style
   - McCabe complexity limits
   - Type hints throughout

### Running Linting & Formatting

```bash
# Format code
ruff format .

# Lint with automatic fixes
ruff check . --fix
```

### Project Configuration (`pyproject.toml`)

- **Python Version:** 3.13+
- **Ruff Settings:** Strict linting with custom ignores
- **Black:** 80-character line length, single quotes
- **McCabe:** Max complexity of 10

## Troubleshooting

### Common Issues

**"GOOGLE_API_KEY and DISCORD_TOKEN must be set" Error:**

- Ensure `.env` file exists in project root
- Verify API key and token are correctly pasted
- Check environment variables are properly loaded

**"Empty response from Gemini model" Error:**

- Verify API key has quota remaining
- Check internet connection
- Ensure prompt is valid and not empty

**Discord Bot Not Responding:**

- Verify bot is online in Discord server
- Check Discord token is correct
- Ensure bot has Message Content intent enabled
- Verify bot permissions in server settings

**Image Processing Errors:**

- Ensure input images are valid formats (PNG, JPG, etc.)
- Check image file sizes are reasonable
- Verify image paths are correct and accessible (Have permission to read the textchannel?)

### Enabling Debug Logging

Add to `.env`:

```env
LOG_LEVEL=DEBUG
```

This provides detailed logging information for troubleshooting.

## Future Enhancements

- REST API with FastAPI for web integration
- Database integration for history tracking
- Advanced image processing and filtering
- Rate limiting and quota management
- Multi-user support with authentication
- Image gallery and sharing features
- Batch processing for multiple images

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## Support

For issues, questions, or suggestions, please open an issue in the repository.
