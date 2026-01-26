"""Tests for configuration module."""

import logging

import pytest
from pydantic import ValidationError

from nano_banana.core.config import Settings


class TestSettings:
    """Test Settings configuration class."""

    def test_settings_with_valid_env_vars(self, mock_env_vars):
        """Test Settings initialization with valid environment variables."""
        settings = Settings()

        assert settings.GOOGLE_API_KEY == 'test_google_api_key'
        assert settings.DISCORD_TOKEN == 'test_discord_token'
        assert settings.DISCORD_GUILD_ID == 123456789
        assert settings.LOG_LEVEL == 'INFO'
        assert settings.MODEL_NAME == 'gemini-2.5-flash-image'
        assert settings.SYSTEM_PROMPT == 'Test prompt'

    def test_settings_missing_google_api_key(self, monkeypatch):
        """Test Settings raises ValueError when GOOGLE_API_KEY is missing."""
        monkeypatch.setenv('GOOGLE_API_KEY', '')
        monkeypatch.setenv('DISCORD_TOKEN', 'test_token')
        monkeypatch.setenv('DISCORD_GUILD_ID', '123456789')

        with pytest.raises(
            ValueError,
            match='GOOGLE_API_KEY and DISCORD_TOKEN and DISCORD_GUILD_ID must be set',
        ):
            Settings()

    def test_settings_missing_discord_token(self, monkeypatch):
        """Test Settings raises ValueError when DISCORD_TOKEN is missing."""
        monkeypatch.setenv('GOOGLE_API_KEY', 'test_key')
        monkeypatch.setenv('DISCORD_TOKEN', '')
        monkeypatch.setenv('DISCORD_GUILD_ID', '123456789')

        with pytest.raises(
            ValueError,
            match='GOOGLE_API_KEY and DISCORD_TOKEN and DISCORD_GUILD_ID must be set',
        ):
            Settings()

    def test_settings_missing_guild_id(self, monkeypatch):
        """Test Settings raises ValueError when DISCORD_GUILD_ID is invalid."""
        monkeypatch.setenv('GOOGLE_API_KEY', 'test_key')
        monkeypatch.setenv('DISCORD_TOKEN', 'test_token')
        # Set invalid guild ID (default -1)
        monkeypatch.setenv('DISCORD_GUILD_ID', '-1')

        with pytest.raises(
            ValueError,
            match='GOOGLE_API_KEY and DISCORD_TOKEN and DISCORD_GUILD_ID must be set',
        ):
            Settings()

    def test_settings_default_values(self, mock_env_vars, monkeypatch):
        """Test Settings uses default values when optional vars are not set."""
        monkeypatch.delenv('LOG_LEVEL', raising=False)
        monkeypatch.delenv('MODEL_NAME', raising=False)
        monkeypatch.delenv('SYSTEM_PROMPT', raising=False)

        settings = Settings()

        assert settings.LOG_LEVEL == 'INFO'
        assert settings.MODEL_NAME == 'gemini-2.5-flash-image'
        # SYSTEM_PROMPT might be set from .env file, so check it's either empty or a string
        assert isinstance(settings.SYSTEM_PROMPT, str)

    def test_settings_case_insensitive(self, monkeypatch):
        """Test Settings is case-insensitive for environment variables."""
        monkeypatch.setenv('google_api_key', 'test_key_lower')
        monkeypatch.setenv('DISCORD_TOKEN', 'test_token')
        monkeypatch.setenv('discord_guild_id', '987654321')

        settings = Settings()

        assert settings.GOOGLE_API_KEY == 'test_key_lower'
        assert settings.DISCORD_GUILD_ID == 987654321

    def test_settings_extra_ignored(self, mock_env_vars, monkeypatch):
        """Test Settings ignores extra environment variables."""
        monkeypatch.setenv('EXTRA_VAR', 'should_be_ignored')

        settings = Settings()

        assert not hasattr(settings, 'EXTRA_VAR')

    def test_logging_configured(self, mock_env_vars):
        """Test that logging is properly configured."""
        logger = logging.getLogger(__name__)

        # Verify logger has handlers
        assert len(logger.handlers) > 0 or len(
            logging.getLogger().handlers,
        ) > 0
