"""Tests for Discord bot commands and event handlers."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock, patch

import discord
import pytest
from PIL import Image

# Ensure src is at the very beginning of path for proper imports
src_path = Path(__file__).parent.parent.parent.parent / 'src'


def _load_bot_module() -> ModuleType:
    """Load the bot module from source path directly."""
    # Ensure src is at the very front of sys.path
    src_str = str(src_path)
    if src_str in sys.path:
        sys.path.remove(src_str)
    sys.path.insert(0, src_str)

    # Clear any cached nano_banana modules to force reimport from src
    keys_to_remove = [k for k in sys.modules if k.startswith('nano_banana')]
    for key in keys_to_remove:
        del sys.modules[key]

    bot_path = src_path / 'nano_banana' / 'discord' / 'bot.py'
    spec = importlib.util.spec_from_file_location(
        'nano_banana.discord.bot',
        bot_path,
    )
    if spec is None or spec.loader is None:
        msg = f'Cannot load bot module from {bot_path}'
        raise ImportError(msg)
    bot = importlib.util.module_from_spec(spec)
    sys.modules['nano_banana.discord.bot'] = bot
    spec.loader.exec_module(bot)
    return bot


# The bot module has module-level initialization that requires env vars.
# We use pytest fixtures from conftest.py (mock_env_vars) to handle this.
# Import the bot functions inside each test or use lazy import.
@pytest.fixture
def bot_module(mock_env_vars: None) -> ModuleType:
    """Import bot module with proper environment setup."""
    return _load_bot_module()


class TestExtractImageUrls:
    """Test _extract_image_urls function."""

    def test_extract_image_urls_with_images(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test extracting URLs from message with image attachments."""
        mock_attachment_1 = MagicMock()
        mock_attachment_1.url = 'https://example.com/image1.png'
        mock_attachment_1.content_type = '/image/png'

        mock_attachment_2 = MagicMock()
        mock_attachment_2.url = 'https://example.com/image2.jpg'
        mock_attachment_2.content_type = '/image/jpeg'

        mock_message = MagicMock()
        mock_message.attachments = [mock_attachment_1, mock_attachment_2]

        urls = bot_module._extract_image_urls(mock_message)

        assert len(urls) == 2
        assert 'https://example.com/image1.png' in urls
        assert 'https://example.com/image2.jpg' in urls

    def test_extract_image_urls_no_images(self, bot_module: ModuleType) -> None:
        """Test extracting URLs from message without attachments."""
        mock_message = MagicMock()
        mock_message.attachments = []

        urls = bot_module._extract_image_urls(mock_message)

        assert urls == []

    def test_extract_image_urls_non_image_attachments(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test filtering out non-image attachments."""
        mock_attachment_1 = MagicMock()
        mock_attachment_1.url = 'https://example.com/document.pdf'
        mock_attachment_1.content_type = 'application/pdf'

        mock_attachment_2 = MagicMock()
        mock_attachment_2.url = 'https://example.com/image.png'
        mock_attachment_2.content_type = '/image/png'

        mock_message = MagicMock()
        mock_message.attachments = [mock_attachment_1, mock_attachment_2]

        urls = bot_module._extract_image_urls(mock_message)

        assert len(urls) == 1
        assert 'https://example.com/image.png' in urls

    def test_extract_image_urls_none_content_type(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling attachments with None content_type."""
        mock_attachment = MagicMock()
        mock_attachment.url = 'https://example.com/unknown'
        mock_attachment.content_type = None

        mock_message = MagicMock()
        mock_message.attachments = [mock_attachment]

        urls = bot_module._extract_image_urls(mock_message)

        assert urls == []


class TestFetchReferenceImages:
    """Test _fetch_reference_images function."""

    @pytest.mark.asyncio
    async def test_fetch_reference_images_with_reference(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test fetching images from referenced message."""
        mock_ref_attachment = MagicMock()
        mock_ref_attachment.url = 'https://example.com/ref_image.png'
        mock_ref_attachment.content_type = '/image/png'

        mock_ref_msg = MagicMock()
        mock_ref_msg.attachments = [mock_ref_attachment]

        mock_channel = AsyncMock()
        mock_channel.fetch_message = AsyncMock(return_value=mock_ref_msg)

        mock_reference = MagicMock()
        mock_reference.message_id = 123456

        mock_message = MagicMock()
        mock_message.reference = mock_reference
        mock_message.channel = mock_channel

        urls = await bot_module._fetch_reference_images(mock_message)

        assert len(urls) == 1
        assert 'https://example.com/ref_image.png' in urls

    @pytest.mark.asyncio
    async def test_fetch_reference_images_no_reference(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test with no message reference."""
        mock_message = MagicMock()
        mock_message.reference = None

        urls = await bot_module._fetch_reference_images(mock_message)

        assert urls == []

    @pytest.mark.asyncio
    async def test_fetch_reference_images_no_message_id(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test with reference but no message_id."""
        mock_reference = MagicMock()
        mock_reference.message_id = None

        mock_message = MagicMock()
        mock_message.reference = mock_reference

        urls = await bot_module._fetch_reference_images(mock_message)

        assert urls == []

    @pytest.mark.asyncio
    async def test_fetch_reference_images_http_exception(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling HTTP exception when fetching reference."""
        mock_channel = AsyncMock()
        mock_channel.fetch_message = AsyncMock(
            side_effect=discord.HTTPException(MagicMock(), 'Error'),
        )
        mock_channel.send = AsyncMock()

        mock_reference = MagicMock()
        mock_reference.message_id = 123456

        mock_message = MagicMock()
        mock_message.reference = mock_reference
        mock_message.channel = mock_channel

        urls = await bot_module._fetch_reference_images(mock_message)

        assert urls == []
        mock_channel.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_reference_images_unexpected_exception(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling unexpected exception when fetching reference."""
        mock_channel = AsyncMock()
        mock_channel.fetch_message = AsyncMock(
            side_effect=RuntimeError('Unexpected error'),
        )
        mock_channel.send = AsyncMock()

        mock_reference = MagicMock()
        mock_reference.message_id = 123456

        mock_message = MagicMock()
        mock_message.reference = mock_reference
        mock_message.channel = mock_channel

        urls = await bot_module._fetch_reference_images(mock_message)

        assert urls == []
        mock_channel.send.assert_called_once()


class TestGenerateResponse:
    """Test _generate_response function."""

    @pytest.mark.asyncio
    async def test_generate_response_success(
        self,
        bot_module: ModuleType,
        sample_image: Image.Image,
    ) -> None:
        """Test successful response generation."""
        mock_channel = AsyncMock()
        mock_message = MagicMock()
        mock_message.reply = AsyncMock()
        mock_message.channel = mock_channel

        with (
            patch.object(
                bot_module.banana,
                'generate',
                new_callable=AsyncMock,
                return_value=('Generated text', sample_image),
            ),
            patch.object(
                bot_module.utils,
                'respond',
                new_callable=AsyncMock,
            ) as mock_respond,
        ):
            await bot_module._generate_response(
                mock_message,
                'test prompt',
                [],
            )

            mock_respond.assert_called_once_with(
                mock_message.reply,
                'Generated text',
                sample_image,
            )

    @pytest.mark.asyncio
    async def test_generate_response_with_images(
        self,
        bot_module: ModuleType,
        sample_image: Image.Image,
    ) -> None:
        """Test response generation with input images."""
        mock_channel = AsyncMock()
        mock_message = MagicMock()
        mock_message.reply = AsyncMock()
        mock_message.channel = mock_channel

        pil_images = [sample_image]

        with (
            patch.object(
                bot_module.banana,
                'generate',
                new_callable=AsyncMock,
                return_value=('Transformed', sample_image),
            ) as mock_generate,
            patch.object(
                bot_module.utils,
                'respond',
                new_callable=AsyncMock,
            ),
        ):
            await bot_module._generate_response(
                mock_message,
                'transform',
                pil_images,
            )

            mock_generate.assert_called_once_with(
                prompt='transform',
                images=pil_images,
            )

    @pytest.mark.asyncio
    async def test_generate_response_http_exception(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling HTTP exception during generation."""
        mock_channel = AsyncMock()
        mock_channel.send = AsyncMock()
        mock_message = MagicMock()
        mock_message.channel = mock_channel

        with patch.object(
            bot_module.banana,
            'generate',
            new_callable=AsyncMock,
            side_effect=discord.HTTPException(MagicMock(), 'HTTP Error'),
        ):
            await bot_module._generate_response(mock_message, 'test', [])

            mock_channel.send.assert_called_once()
            assert '發生錯誤' in mock_channel.send.call_args[0][0]

    @pytest.mark.asyncio
    async def test_generate_response_value_error(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling ValueError during generation."""
        mock_channel = AsyncMock()
        mock_channel.send = AsyncMock()
        mock_message = MagicMock()
        mock_message.channel = mock_channel

        with patch.object(
            bot_module.banana,
            'generate',
            new_callable=AsyncMock,
            side_effect=ValueError('Invalid input'),
        ):
            await bot_module._generate_response(mock_message, 'test', [])

            mock_channel.send.assert_called_once()
            assert '發生錯誤' in mock_channel.send.call_args[0][0]

    @pytest.mark.asyncio
    async def test_generate_response_runtime_error(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling RuntimeError during generation."""
        mock_channel = AsyncMock()
        mock_channel.send = AsyncMock()
        mock_message = MagicMock()
        mock_message.channel = mock_channel

        with patch.object(
            bot_module.banana,
            'generate',
            new_callable=AsyncMock,
            side_effect=RuntimeError('Runtime error'),
        ):
            await bot_module._generate_response(mock_message, 'test', [])

            mock_channel.send.assert_called_once()
            assert '發生錯誤' in mock_channel.send.call_args[0][0]

    @pytest.mark.asyncio
    async def test_generate_response_unexpected_exception(
        self,
        bot_module: ModuleType,
    ) -> None:
        """Test handling unexpected exception during generation."""
        mock_channel = AsyncMock()
        mock_channel.send = AsyncMock()
        mock_message = MagicMock()
        mock_message.channel = mock_channel

        with patch.object(
            bot_module.banana,
            'generate',
            new_callable=AsyncMock,
            side_effect=KeyError('unexpected'),
        ):
            await bot_module._generate_response(mock_message, 'test', [])

            mock_channel.send.assert_called_once()
            assert '發生未預期的錯誤' in mock_channel.send.call_args[0][0]


class TestDrawCommand:
    """Test draw slash command."""

    @pytest.mark.asyncio
    async def test_draw_command_success(
        self,
        bot_module: ModuleType,
        mock_discord_context,
        sample_image: Image.Image,
    ) -> None:
        """Test successful draw command execution."""
        mock_discord_context.defer = AsyncMock()
        mock_discord_context.respond = AsyncMock()

        with (
            patch.object(
                bot_module.banana,
                'generate',
                new_callable=AsyncMock,
                return_value=('Generated!', sample_image),
            ),
            patch.object(
                bot_module.utils,
                'respond',
                new_callable=AsyncMock,
            ) as mock_respond,
        ):
            await bot_module.draw(mock_discord_context, 'a beautiful sunset')

            mock_discord_context.defer.assert_called_once()
            mock_respond.assert_called_once_with(
                mock_discord_context.respond,
                'Generated!',
                sample_image,
            )


class TestOnMessage:
    """Test on_message event handler."""

    @pytest.mark.asyncio
    async def test_on_message_ignore_bot(
        self,
        bot_module: ModuleType,
        mock_discord_message: MagicMock,
    ) -> None:
        """Test that bot messages are ignored."""
        mock_discord_message.author.bot = True

        with patch.object(
            bot_module,
            '_generate_response',
            new_callable=AsyncMock,
        ) as mock_generate:
            await bot_module.on_message(mock_discord_message)

            mock_generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_on_message_ignore_other_guild(
        self,
        bot_module: ModuleType,
        mock_discord_message: MagicMock,
    ) -> None:
        """Test that messages from other guilds are ignored."""
        mock_discord_message.author.bot = False
        mock_discord_message.guild.id = 999999999

        with patch.object(
            bot_module,
            '_generate_response',
            new_callable=AsyncMock,
        ) as mock_generate:
            await bot_module.on_message(mock_discord_message)

            mock_generate.assert_not_called()

    @pytest.mark.asyncio
    async def test_on_message_too_many_images(
        self,
        bot_module: ModuleType,
        mock_discord_message: MagicMock,
    ) -> None:
        """Test rejection when too many images are sent."""
        mock_discord_message.author.bot = False
        mock_discord_message.guild.id = bot_module.settings.discord_guild_id

        # Create more attachments than allowed
        attachments = []
        for i in range(bot_module.settings.MAX_IMAGE_PER_REQUEST + 5):
            mock_att = MagicMock()
            mock_att.url = f'https://example.com/image{i}.png'
            mock_att.content_type = '/image/png'
            attachments.append(mock_att)
        mock_discord_message.attachments = attachments
        mock_discord_message.reference = None
        mock_discord_message.channel.send = AsyncMock()

        await bot_module.on_message(mock_discord_message)

        mock_discord_message.channel.send.assert_called_once()
        assert (
            '一次最多只能處理'
            in mock_discord_message.channel.send.call_args[0][0]
        )

    @pytest.mark.asyncio
    async def test_on_message_with_text_only(
        self,
        bot_module: ModuleType,
        mock_discord_message: MagicMock,
    ) -> None:
        """Test message processing with text only."""
        mock_discord_message.author.bot = False
        mock_discord_message.guild.id = bot_module.settings.discord_guild_id
        mock_discord_message.content = 'Hello, bot!'
        mock_discord_message.attachments = []
        mock_discord_message.reference = None
        mock_discord_message.channel.typing = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(),
                __aexit__=AsyncMock(),
            ),
        )

        with patch.object(
            bot_module,
            '_generate_response',
            new_callable=AsyncMock,
        ) as mock_generate:
            await bot_module.on_message(mock_discord_message)

            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_on_message_with_images(
        self,
        bot_module: ModuleType,
        mock_discord_message: MagicMock,
    ) -> None:
        """Test message processing with images."""
        mock_discord_message.author.bot = False
        mock_discord_message.guild.id = bot_module.settings.discord_guild_id
        mock_discord_message.content = 'transform this'
        mock_discord_message.reference = None

        # Create image attachment
        mock_att = MagicMock()
        mock_att.url = 'https://example.com/image.png'
        mock_att.content_type = '/image/png'
        mock_discord_message.attachments = [mock_att]

        mock_discord_message.channel.typing = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(),
                __aexit__=AsyncMock(),
            ),
        )

        with (
            patch.object(
                bot_module.utils,
                'download_image',
                new_callable=AsyncMock,
                return_value=MagicMock(),
            ),
            patch.object(
                bot_module,
                '_generate_response',
                new_callable=AsyncMock,
            ) as mock_generate,
        ):
            await bot_module.on_message(mock_discord_message)

            mock_generate.assert_called_once()


class TestOnReady:
    """Test on_ready event handler."""

    @pytest.mark.asyncio
    async def test_on_ready_logs_message(self, bot_module) -> None:
        """Test that on_ready logs the ready message."""
        with patch.object(bot_module.logger, 'info') as mock_logger:
            await bot_module.on_ready()

            mock_logger.assert_called_once_with('Client is ready!')
