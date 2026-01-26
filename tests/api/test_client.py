"""Tests for NanoBananaClient."""

import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PIL import Image

from nano_banana.api.client import NanoBananaClient


class TestNanoBananaClient:
    """Test NanoBananaClient class."""

    def test_client_initialization_success(self):
        """Test successful client initialization."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        assert client.model_name == 'test-model'
        assert client.client is not None

    def test_client_initialization_no_api_key(self):
        """Test client initialization fails without API key."""
        with pytest.raises(ValueError, match='Google API key is required'):
            NanoBananaClient(api_key='', model_name='test-model')

    @pytest.mark.asyncio
    async def test_generate_text_to_image(self, sample_image_bytes):
        """Test text-to-image generation."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        # Mock the API response
        mock_part = MagicMock()
        mock_part.text = 'Generated image description'
        mock_part.inline_data = MagicMock()
        mock_part.inline_data.data = sample_image_bytes

        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ) as mock_generate:
            text, image = await client.generate(
                prompt='A beautiful sunset',
            )

            assert text == 'Generated image description'
            assert isinstance(image, Image.Image)
            assert image.size == (100, 100)
            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_image_transformation(
        self,
        sample_image,
        sample_image_bytes,
    ):
        """Test image transformation with prompt."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        # Mock the API response
        mock_part = MagicMock()
        mock_part.text = 'Transformed image'
        mock_part.inline_data = MagicMock()
        mock_part.inline_data.data = sample_image_bytes

        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ) as mock_generate:
            text, image = await client.generate(
                prompt='Make it more colorful',
                images=[sample_image],
            )

            assert text == 'Transformed image'
            assert isinstance(image, Image.Image)
            mock_generate.assert_called_once()

    @pytest.mark.asyncio
    async def test_generate_empty_response(self):
        """Test handling of empty response."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        mock_response = MagicMock()
        mock_response.parts = []

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ):
            with pytest.raises(
                ValueError,
                match='Empty response from Gemini model',
            ):
                await client.generate(prompt='Test prompt')

    @pytest.mark.asyncio
    async def test_generate_missing_image_data(self):
        """Test handling of response without image data."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        # Mock response with text but no image
        mock_part = MagicMock()
        mock_part.text = 'Some text'
        mock_part.inline_data = None

        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ):
            with pytest.raises(
                ValueError,
                match='Incomplete response: missing image data',
            ):
                await client.generate(prompt='Test prompt')

    @pytest.mark.asyncio
    async def test_generate_api_exception(self):
        """Test handling of API exceptions."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        with patch.object(
            client.client.aio.models,
            'generate_content',
            side_effect=Exception('API Error'),
        ):
            with pytest.raises(Exception, match='API Error'):
                await client.generate(prompt='Test prompt')

    @pytest.mark.asyncio
    async def test_generate_multiple_images(self, sample_image_bytes):
        """Test generation with multiple input images."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        image1 = Image.new('RGB', (50, 50), color='blue')
        image2 = Image.new('RGB', (50, 50), color='green')

        mock_part = MagicMock()
        mock_part.text = 'Combined image'
        mock_part.inline_data = MagicMock()
        mock_part.inline_data.data = sample_image_bytes

        mock_response = MagicMock()
        mock_response.parts = [mock_part]

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ) as mock_generate:
            text, image = await client.generate(
                prompt='Combine these',
                images=[image1, image2],
            )

            assert text == 'Combined image'
            assert isinstance(image, Image.Image)
            # Verify both images were passed
            call_args = mock_generate.call_args
            assert len(call_args.kwargs['contents']) == 3  # prompt + 2 images

    def test_process_image_bytes(self, sample_image_bytes):
        """Test _process_image_bytes static method."""
        image = NanoBananaClient._process_image_bytes(sample_image_bytes)

        assert isinstance(image, Image.Image)
        assert image.size == (100, 100)

    @pytest.mark.asyncio
    async def test_generate_with_multiple_text_parts(
        self,
        sample_image_bytes,
    ):
        """Test handling response with multiple text parts."""
        client = NanoBananaClient(
            api_key='test_api_key',
            model_name='test-model',
        )

        # Mock response with multiple text parts
        mock_part1 = MagicMock()
        mock_part1.text = 'Part 1 '
        mock_part1.inline_data = None

        mock_part2 = MagicMock()
        mock_part2.text = 'Part 2'
        mock_part2.inline_data = MagicMock()
        mock_part2.inline_data.data = sample_image_bytes

        mock_response = MagicMock()
        mock_response.parts = [mock_part1, mock_part2]

        with patch.object(
            client.client.aio.models,
            'generate_content',
            return_value=mock_response,
        ):
            text, image = await client.generate(prompt='Test')

            assert text == 'Part 1 Part 2'
            assert isinstance(image, Image.Image)
