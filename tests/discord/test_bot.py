"""Tests for Discord bot functionality."""

import io
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from PIL import Image


@pytest.fixture
def mock_banana_client(sample_image):
    """Mock NanoBananaClient."""
    mock_client = MagicMock()
    mock_client.generate = AsyncMock(
        return_value=('Generated text', sample_image),
    )
    return mock_client


class TestDiscordBot:
    """Test Discord bot commands and listeners."""

    @pytest.mark.asyncio
    async def test_draw_command_success(
        self,
        mock_env_vars,
        sample_image,
    ):
        """Test /畫圖 slash command with successful generation."""
        # Import here to use mocked environment
        with patch('nano_banana.discord.bot.banana') as mock_banana:
            mock_banana.generate = AsyncMock(
                return_value=('Test response', sample_image),
            )

            from nano_banana.discord.bot import draw

            mock_ctx = MagicMock()
            mock_ctx.defer = AsyncMock()
            mock_ctx.respond = AsyncMock()
            mock_ctx.author = MagicMock()
            mock_ctx.author.name = 'test_user'

            await draw(mock_ctx, prompt='A beautiful landscape')

            mock_ctx.defer.assert_called_once()
            mock_banana.generate.assert_called_once()
            mock_ctx.respond.assert_called_once()

            # Verify file was created
            call_args = mock_ctx.respond.call_args
            assert 'file' in call_args.kwargs or len(call_args.args) > 1

    @pytest.mark.asyncio
    async def test_on_message_ignores_bot_messages(self, mock_env_vars):
        """Test on_message ignores messages from bots."""
        from nano_banana.discord.bot import on_message

        mock_message = MagicMock()
        mock_message.author.bot = True
        mock_message.content = 'Bot message'

        # Should return early without processing
        result = await on_message(mock_message)
        assert result is None

    @pytest.mark.asyncio
    async def test_on_message_ignores_wrong_guild(self, mock_env_vars):
        """Test on_message ignores messages from wrong guild."""
        from nano_banana.discord.bot import on_message

        mock_message = MagicMock()
        mock_message.author.bot = False
        mock_message.guild = MagicMock()
        mock_message.guild.id = 999999999  # Different from test guild

        result = await on_message(mock_message)
        assert result is None

    @pytest.mark.asyncio
    async def test_on_message_text_only(self, mock_env_vars, sample_image):
        """Test on_message with text-only message."""
        with patch('nano_banana.discord.bot.banana') as mock_banana:
            mock_banana.generate = AsyncMock(
                return_value=('Generated text', sample_image),
            )

            from nano_banana.discord.bot import on_message

            mock_message = MagicMock()
            mock_message.author.bot = False
            mock_message.guild = MagicMock()
            mock_message.guild.id = 123456789
            mock_message.content = 'Generate an image'
            mock_message.attachments = []
            mock_message.channel = MagicMock()
            mock_message.channel.typing = MagicMock()
            mock_message.channel.typing.return_value.__aenter__ = AsyncMock()
            mock_message.channel.typing.return_value.__aexit__ = AsyncMock()
            mock_message.reply = AsyncMock()

            await on_message(mock_message)

            mock_banana.generate.assert_called_once()
            mock_message.reply.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_message_with_image_attachment(
        self,
        mock_env_vars,
        sample_image,
    ):
        """Test on_message with image attachment."""
        with patch('nano_banana.discord.bot.banana') as mock_banana, patch(
            'nano_banana.discord.bot.utils.download_image',
        ) as mock_download:
            mock_banana.generate = AsyncMock(
                return_value=('Transformed', sample_image),
            )
            mock_download.return_value = sample_image

            from nano_banana.discord.bot import on_message

            mock_attachment = MagicMock()
            mock_attachment.url = 'https://example.com/image.png'
            mock_attachment.content_type = 'image/png'

            mock_message = MagicMock()
            mock_message.author.bot = False
            mock_message.guild = MagicMock()
            mock_message.guild.id = 123456789
            mock_message.content = 'Transform this image'
            mock_message.attachments = [mock_attachment]
            mock_message.channel = MagicMock()
            mock_message.channel.typing = MagicMock()
            mock_message.channel.typing.return_value.__aenter__ = AsyncMock()
            mock_message.channel.typing.return_value.__aexit__ = AsyncMock()
            mock_message.reply = AsyncMock()

            await on_message(mock_message)

            mock_download.assert_called_once_with(
                'https://example.com/image.png',
            )
            mock_banana.generate.assert_called_once()
            # Verify images were passed
            call_args = mock_banana.generate.call_args
            assert call_args.kwargs.get('images') is not None

    @pytest.mark.asyncio
    async def test_on_message_multiple_attachments(
        self,
        mock_env_vars,
        sample_image,
    ):
        """Test on_message with multiple image attachments."""
        with patch('nano_banana.discord.bot.banana') as mock_banana, patch(
            'nano_banana.discord.bot.utils.download_image',
        ) as mock_download:
            mock_banana.generate = AsyncMock(
                return_value=('Combined', sample_image),
            )
            mock_download.return_value = sample_image

            from nano_banana.discord.bot import on_message

            mock_att1 = MagicMock()
            mock_att1.url = 'https://example.com/image1.png'
            mock_att1.content_type = 'image/png'

            mock_att2 = MagicMock()
            mock_att2.url = 'https://example.com/image2.png'
            mock_att2.content_type = 'image/jpeg'

            mock_message = MagicMock()
            mock_message.author.bot = False
            mock_message.guild = MagicMock()
            mock_message.guild.id = 123456789
            mock_message.content = 'Combine these'
            mock_message.attachments = [mock_att1, mock_att2]
            mock_message.channel = MagicMock()
            mock_message.channel.typing = MagicMock()
            mock_message.channel.typing.return_value.__aenter__ = AsyncMock()
            mock_message.channel.typing.return_value.__aexit__ = AsyncMock()
            mock_message.reply = AsyncMock()

            await on_message(mock_message)

            assert mock_download.call_count == 2
            mock_banana.generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_message_error_handling(self, mock_env_vars):
        """Test on_message error handling."""
        with patch('nano_banana.discord.bot.banana') as mock_banana:
            mock_banana.generate = AsyncMock(
                side_effect=Exception('Generation failed'),
            )

            from nano_banana.discord.bot import on_message

            mock_message = MagicMock()
            mock_message.author.bot = False
            mock_message.guild = MagicMock()
            mock_message.guild.id = 123456789
            mock_message.content = 'Test'
            mock_message.attachments = []
            mock_message.channel = MagicMock()
            mock_message.channel.typing = MagicMock()
            mock_message.channel.typing.return_value.__aenter__ = AsyncMock()
            mock_message.channel.typing.return_value.__aexit__ = AsyncMock()
            mock_message.channel.send = AsyncMock()

            await on_message(mock_message)

            mock_message.channel.send.assert_called_once()
            call_args = mock_message.channel.send.call_args
            assert '發生錯誤' in str(call_args)

    @pytest.mark.asyncio
    async def test_on_message_non_image_attachment(
        self,
        mock_env_vars,
        sample_image,
    ):
        """Test on_message ignores non-image attachments."""
        with patch('nano_banana.discord.bot.banana') as mock_banana:
            mock_banana.generate = AsyncMock(
                return_value=('Text', sample_image),
            )

            from nano_banana.discord.bot import on_message

            mock_att_text = MagicMock()
            mock_att_text.url = 'https://example.com/file.txt'
            mock_att_text.content_type = 'text/plain'

            mock_att_image = MagicMock()
            mock_att_image.url = 'https://example.com/image.png'
            mock_att_image.content_type = 'image/png'

            mock_message = MagicMock()
            mock_message.author.bot = False
            mock_message.guild = MagicMock()
            mock_message.guild.id = 123456789
            mock_message.content = 'Test'
            mock_message.attachments = [
                mock_att_text,
                mock_att_image,
            ]  # Mixed attachments
            mock_message.channel = MagicMock()
            mock_message.channel.typing = MagicMock()
            mock_message.channel.typing.return_value.__aenter__ = AsyncMock()
            mock_message.channel.typing.return_value.__aexit__ = AsyncMock()
            mock_message.reply = AsyncMock()

            with patch(
                'nano_banana.discord.bot.utils.download_image',
            ) as mock_download:
                mock_download.return_value = sample_image

                await on_message(mock_message)

                # Only image attachment should be downloaded
                mock_download.assert_called_once_with(
                    'https://example.com/image.png',
                )

    @pytest.mark.asyncio
    async def test_on_ready(self, mock_env_vars):
        """Test on_ready event."""
        from nano_banana.discord.bot import on_ready

        # Should log without error
        await on_ready()
