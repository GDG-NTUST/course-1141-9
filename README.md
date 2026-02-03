<div align="center">

# 🍌 Playing with Nano Banana on Discord Together 🍌

[<img src=".github/assets/gdg-logo.png" width="400" alt="GDG | NTUST">](https://gdg-ntust.org/)

<br>[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Nano Banana](https://img.shields.io/badge/Nano%20Banana-yellow?style=for-the-badge&logo=gamebanana&logoColor=white)](https://ai.google.dev/)
[![Google Gemini](https://img.shields.io/badge/gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)](https://ai.google.dev/)

[![Python 3.13+](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python&logoColor=ffffff)](https://www.python.org/)
[![py-cord](https://img.shields.io/badge/pycord-2.7+-blue?style=for-the-badge&logo=discord&logoColor=ffffff)](https://github.com/Pycord-Development/pycord)
[![pydantic-settings](https://img.shields.io/badge/pydantic--settings-2.12+-blue?style=for-the-badge&logo=pydantic)](https://pydantic.dev/latest/)

**[繁體中文](README_zh-TW.md)** | English

</div>

## Overview

Nano Banana is a tutorial project demonstrating how to use Google Gemini API for AI image generation. Through a Discord bot interface, users can:

- 🎨 **Text-to-Image** - Create images from text descriptions
- 🔄 **Image Transformation** - Modify existing images based on prompts
- 💬 **Discord Integration** - Interact via slash commands or messages

### Technical Highlights

- Clean modular architecture (config, API, Discord layers separated)
- Full async programming implementation
- Configuration management with Pydantic
- Complete test coverage (pytest + pytest-asyncio)
- Fast dependency management with uv

## Quick Start

### Prerequisites

- Python 3.13+
- [Google Gemini API Key](https://ai.google.dev/)
- [Discord Bot Token](https://discord.com/developers/applications)

### Installation

```bash
# Install uv package manager
pip install uv

# Clone the repository
git clone https://github.com/GDG-NTUST/course-1141-9.git
cd course-1141-9

# Install dependencies
uv sync
```

### Configuration

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
DISCORD_TOKEN=your_discord_bot_token
DISCORD_GUILD_ID=your_server_id

# Optional settings
LOG_LEVEL=INFO
MODEL_NAME=gemini-2.5-flash-image
SYSTEM_PROMPT=You are a helpful AI assistant.
```

### Running

```bash
# Start the Discord bot
cd src/
uv run nano_banana
```

## Usage

### Discord Bot

**Slash Command:**
```
/draw a cat wearing a hat
```

**Message Interaction:**
- Send text messages directly to generate images
- Attach images with text prompts for image transformation
- Reply to messages containing images

### Command-Line Demo

```bash
cd src/

# Text-to-Image
uv run nano_banana_cli -p "beautiful sunset"

# Image Transformation
uv run nano_banana_cli -p "make it more vibrant" -i image.png

# Multiple Images
uv run nano_banana_cli -p "combine these styles" -i img1.png img2.png
```

Generated images are saved in `src/nano_banana/api/demo/outputs/`

## Project Architecture

```
nano_banana/
├── core/
│   └── config.py          # Pydantic configuration management
├── api/
│   ├── client.py          # Google Gemini API client
│   └── demo/
│       └── demo.py        # Command-line demo
└── discord/
    ├── bot.py             # Discord bot
    └── utils.py           # Utility functions
```

### Core Modules

- **`config.py`** - Environment variable loading, logging configuration, settings validation
- **`client.py`** - Async Gemini API client supporting text-to-image and image transformation
- **`bot.py`** - Discord bot handling slash commands and message events
- **`utils.py`** - Image download and response handling utilities

## Testing

```bash
# Install development dependencies
uv sync

# Run all tests
uv run pytest

# Run tests with coverage report
uv run pytest --cov=nano_banana --cov-report=html

# Run specific tests
uv run pytest tests/api/test_client.py
```

Test Coverage:
- ✅ Configuration management (environment variables, validation, defaults)
- ✅ API client (text-to-image, image transformation, error handling)
- ✅ Discord bot (command handling, message listening, image attachments)
- ✅ Utility functions (image download, response formatting)

## Development

### Code Quality

```bash
# Format code
uv run ruff format .

# Run linter
uv run ruff check . --fix
```

### Project Configuration

- **Ruff** - Code linting and formatting
- **pytest** - Testing framework
- **pytest-asyncio** - Async testing support
- **pytest-cov** - Test coverage

See `pyproject.toml` for detailed configuration

## Supported Models

| Model Name | Max Images |
|-----------|-----------|
| `gemini-2.5-flash-image` | 3 |
| `gemini-3-pro-image-preview` | 14 |

Set `MODEL_NAME` in `.env` to switch models.

## Troubleshooting

**API Key Error:**
- Verify `.env` file exists and is properly formatted
- Check if API key is valid and has quota

**Discord Bot Not Responding:**
- Confirm bot is online
- Check if Discord Token is correct
- Ensure Message Content Intent is enabled
- Verify DISCORD_GUILD_ID is set correctly

**Enable Debug Logging:**
```env
LOG_LEVEL=DEBUG
```

## License

This project is licensed under the [MIT License](LICENSE)

## Contributing

Pull requests and issues are welcome!

---

<div align="center">

Made with ❤️ by [GDG NTUST](https://gdg-ntust.org/)

</div>
