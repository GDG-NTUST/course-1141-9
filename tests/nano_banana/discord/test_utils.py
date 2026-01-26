"""Tests for Discord utility functions."""

from unittest.mock import AsyncMock, patch

import httpx
import pytest
from PIL import Image

from nano_banana.discord.utils import download_image


class TestUtils:
    """Test Discord utility functions."""

    @pytest.mark.asyncio
    async def test_download_image_success(self, sample_image_bytes):
        """Test successful image download."""
        mock_response = AsyncMock()
        mock_response.content = sample_image_bytes

        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            image = await download_image('https://example.com/image.png')

            assert isinstance(image, Image.Image)
            assert image.size == (100, 100)

    @pytest.mark.asyncio
    async def test_download_image_network_error(self):
        """Test handling of network errors during download."""
        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=httpx.HTTPError('Network error'),
            )

            with pytest.raises(httpx.HTTPError, match='Network error'):
                await download_image('https://example.com/image.png')

    @pytest.mark.asyncio
    async def test_download_image_invalid_image(self):
        """Test handling of invalid image data."""
        mock_response = AsyncMock()
        mock_response.content = b'invalid image data'

        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            with pytest.raises(Exception):  # PIL will raise an exception
                await download_image('https://example.com/invalid.png')

    @pytest.mark.asyncio
    async def test_download_image_empty_content(self):
        """Test handling of empty response content."""
        mock_response = AsyncMock()
        mock_response.content = b''

        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            with pytest.raises(Exception):  # PIL will raise an exception
                await download_image('https://example.com/empty.png')

    @pytest.mark.asyncio
    async def test_download_image_different_formats(self, sample_image):
        """Test downloading images in different formats."""
        import io

        # Test PNG format
        png_buffer = io.BytesIO()
        sample_image.save(png_buffer, format='PNG')
        png_bytes = png_buffer.getvalue()

        mock_response = AsyncMock()
        mock_response.content = png_bytes

        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
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

        with patch('nano_banana.discord.utils.httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response,
            )

            image = await download_image('https://example.com/test.jpg')
            assert isinstance(image, Image.Image)
