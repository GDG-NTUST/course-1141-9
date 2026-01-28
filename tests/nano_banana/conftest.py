"""Pytest configuration and shared fixtures."""

import io
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image


@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock environment variables for testing."""
    monkeypatch.setenv('GOOGLE_API_KEY', 'test_google_api_key')
    monkeypatch.setenv('DISCORD_TOKEN', 'test_discord_token')
    monkeypatch.setenv('DISCORD_GUILD_ID', '123456789')
    monkeypatch.setenv('LOG_LEVEL', 'INFO')
    monkeypatch.setenv('MODEL_NAME', 'gemini-2.5-flash-image')
    monkeypatch.setenv('SYSTEM_PROMPT', 'Test prompt')


@pytest.fixture
def sample_image() -> Image.Image:
    """Create a sample PIL image for testing."""
    return Image.new('RGB', (100, 100), color='red')


@pytest.fixture
def sample_image_bytes(sample_image: Image.Image) -> bytes:
    """Convert sample image to bytes."""

    buffer = io.BytesIO()
    sample_image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.read()


@pytest.fixture
def temp_image_path(tmp_path: Path, sample_image: Image.Image) -> str:
    """Create a temporary image file."""
    image_path = tmp_path / 'test_image.png'
    sample_image.save(image_path)
    return str(image_path)


@pytest.fixture
def mock_genai_client() -> MagicMock:
    """Mock Google GenAI client."""
    return MagicMock()


@pytest.fixture
def mock_discord_context() -> MagicMock:
    """Mock Discord application context."""
    mock_ctx = MagicMock()
    mock_ctx.author = MagicMock()
    mock_ctx.author.name = 'test_user'
    return mock_ctx


@pytest.fixture
def mock_discord_message() -> MagicMock:
    """Mock Discord message."""
    mock_msg = MagicMock()
    mock_msg.author = MagicMock()
    mock_msg.author.bot = False
    mock_msg.author.name = 'test_user'
    mock_msg.content = 'test message'
    mock_msg.attachments = []
    mock_msg.guild = MagicMock()
    mock_msg.guild.id = 123456789
    mock_msg.channel = MagicMock()
    return mock_msg
