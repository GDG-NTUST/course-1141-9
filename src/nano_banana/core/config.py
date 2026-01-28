"""Application configuration using Pydantic settings."""

import logging

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration loaded from environment variables."""

    GOOGLE_API_KEY: str = ''
    DISCORD_TOKEN: str = ''
    DISCORD_GUILD_ID: int = -1
    LOG_LEVEL: str = 'INFO'
    MODEL_NAME: str = 'gemini-2.5-flash-image'
    MAX_IMAGE_PER_REQUEST: int = -1
    SYSTEM_PROMPT: str = ''

    model_config = SettingsConfigDict(
        env_file=('.env', '../.env'),
        env_prefix='',
        case_sensitive=False,
        extra='ignore',
    )

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s.%(msecs)03d | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    @property
    def discord_token(self) -> str:
        if self.DISCORD_TOKEN:
            return self.DISCORD_TOKEN
        msg = 'DISCORD_TOKEN is not set'
        raise ValueError(msg)

    @property
    def discord_guild_id(self) -> int:
        if self.DISCORD_GUILD_ID != -1:
            return self.DISCORD_GUILD_ID
        msg = 'DISCORD_GUILD_ID is not set'
        raise ValueError(msg)

    def __init__(self) -> None:
        super().__init__()
        logger = logging.getLogger(__name__)

        if not self.GOOGLE_API_KEY:
            msg = 'GOOGLE_API_KEY must be set in environment variables.'
            logger.error(msg)
            raise ValueError(msg)

        match self.MODEL_NAME:
            case 'gemini-2.5-flash-image':
                self.MAX_IMAGE_PER_REQUEST = 3
            case 'gemini-3-pro-image-preview':
                self.MAX_IMAGE_PER_REQUEST = 14
            case _:
                msg = f'Unsupported MODEL_NAME: {self.MODEL_NAME}'
                logger.error(msg)
                raise ValueError(msg)
