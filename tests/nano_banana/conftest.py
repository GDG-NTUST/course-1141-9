"""Pytest configuration and shared fixtures."""

import os
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    monkeypatch.setenv('GOOGLE_API_KEY', 'test_google_api_key')
    monkeypatch.setenv('DISCORD_TOKEN', 'test_discord_token')
    monkeypatch.setenv('DISCORD_GUILD_ID', '123456789')
    monkeypatch.setenv('LOG_LEVEL', 'INFO')
    monkeypatch.setenv('MODEL_NAME', 'gemini-2.5-flash-image')
    monkeypatch.setenv('SYSTEM_PROMPT', 'Test prompt')


@pytest.fixture
def sample_image():
    """Create a sample PIL image for testing."""
    img = Image.new('RGB', (100, 100), color='red')
    return img


@pytest.fixture
def sample_image_bytes(sample_image):
    """Convert sample image to bytes."""
    import io

    buffer = io.BytesIO()
    sample_image.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer.read()


@pytest.fixture
def temp_image_path(tmp_path, sample_image):
    """Create a temporary image file."""
    image_path = tmp_path / 'test_image.png'
    sample_image.save(image_path)
    return image_path


@pytest.fixture
def mock_genai_client():
    """Mock Google GenAI client."""
    mock_client = MagicMock()
    return mock_client


@pytest.fixture
def mock_discord_context():
    """Mock Discord application context."""
    mock_ctx = MagicMock()
    mock_ctx.author = MagicMock()
    mock_ctx.author.name = 'test_user'
    return mock_ctx


@pytest.fixture
def mock_discord_message():
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
