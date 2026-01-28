"""Tests for Discord utility functions."""

import io
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from PIL import Image, UnidentifiedImageError

from src.nano_banana.discord.utils import download_image


class TestUtils:
    """Test Discord utility functions."""

    @pytest.mark.asyncio
    async def test_download_image_success(
        self,
        sample_image_bytes: bytes,
    ) -> None:
        """Test successful image download."""
        mock_response = AsyncMock()
        mock_response.content = sample_image_bytes

        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            image = await download_image('https://example.com/image.png')

            assert isinstance(image, Image.Image)
            assert image.size == (100, 100)

    @pytest.mark.asyncio
    async def test_download_image_network_error(self) -> None:
        """Test handling of network errors during download."""
        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.HTTPError('Network error'),
            )

            with pytest.raises(httpx.HTTPError, match='Network error'):
                await download_image('https://example.com/image.png')

    @pytest.mark.asyncio
    async def test_download_image_invalid_image(self) -> None:
        """Test handling of invalid image data."""
        mock_response = AsyncMock()
        mock_response.content = b'invalid image data'

        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            with pytest.raises(UnidentifiedImageError):
                await download_image('https://example.com/invalid.png')

    @pytest.mark.asyncio
    async def test_download_image_empty_content(self) -> None:
        """Test handling of empty response content."""
        mock_response = AsyncMock()
        mock_response.content = b''

        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            with pytest.raises(UnidentifiedImageError):
                await download_image('https://example.com/empty.png')

    @pytest.mark.asyncio
    async def test_download_image_different_formats(
        self,
        sample_image: Image.Image,
    ) -> None:
        """Test downloading images in different formats."""

        # Test PNG format
        png_buffer = io.BytesIO()
        sample_image.save(png_buffer, format='PNG')
        png_bytes = png_buffer.getvalue()

        mock_response = AsyncMock()
        mock_response.content = png_bytes

        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            image = await download_image('https://example.com/test.png')
            assert isinstance(image, Image.Image)

        # Test JPEG format
        jpeg_buffer = io.BytesIO()
        sample_image.save(jpeg_buffer, format='JPEG')
        jpeg_bytes = jpeg_buffer.getvalue()

        mock_response.content = jpeg_bytes

        with patch(
            'src.nano_banana.discord.utils.httpx.AsyncClient',
        ) as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            image = await download_image('https://example.com/test.jpg')
            assert isinstance(image, Image.Image)
