"""Tests for demo script."""

import argparse
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PIL import Image

from nano_banana.api.demo.demo import ensure_output_dir, main, mock_image_path


class TestDemoUtilities:
    """Test demo utility functions."""

    def test_ensure_output_dir_creates_directory(self, tmp_path):
        """Test ensure_output_dir creates directory if it doesn't exist."""
        new_dir = tmp_path / 'new_output'
        assert not new_dir.exists()

        result = ensure_output_dir(new_dir)

        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir

    def test_ensure_output_dir_existing_directory(self, tmp_path):
        """Test ensure_output_dir with existing directory."""
        existing_dir = tmp_path / 'existing'
        existing_dir.mkdir()

        result = ensure_output_dir(existing_dir)

        assert existing_dir.exists()
        assert result == existing_dir

    def test_ensure_output_dir_creates_parent_dirs(self, tmp_path):
        """Test ensure_output_dir creates parent directories."""
        nested_dir = tmp_path / 'parent' / 'child' / 'output'

        result = ensure_output_dir(nested_dir)

        assert nested_dir.exists()
        assert result == nested_dir

    def test_mock_image_path_format(self, tmp_path):
        """Test mock_image_path generates correct format."""
        output_dir = tmp_path

        result = mock_image_path(output_dir)

        assert result.parent == output_dir
        assert result.name.startswith('nano-banana-')
        assert result.suffix == '.png'

    def test_mock_image_path_custom_suffix(self, tmp_path):
        """Test mock_image_path with custom suffix."""
        output_dir = tmp_path

        result = mock_image_path(output_dir, suffix='jpg')

        assert result.suffix == '.jpg'

    def test_mock_image_path_unique(self, tmp_path):
        """Test mock_image_path generates unique paths."""
        output_dir = tmp_path

        path1 = mock_image_path(output_dir)
        path2 = mock_image_path(output_dir)

        assert path1 != path2


class TestDemoMain:
    """Test demo main function."""

    @pytest.mark.asyncio
    async def test_main_text_to_image(
        self,
        mock_env_vars,
        sample_image,
        tmp_path,
    ):
        """Test main function with text-to-image generation."""
        test_args = [
            'demo.py',
            '-p',
            'A beautiful sunset',
        ]

        with patch(
            'sys.argv',
            test_args,
        ), patch(
            'nano_banana.api.demo.demo.NanoBananaClient',
        ) as mock_client_class, patch(
            'nano_banana.api.demo.demo.Path',
        ) as mock_path:
            # Setup mocks
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Generated text', sample_image),
            )
            mock_client_class.return_value = mock_client

            # Mock Path to use tmp_path
            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with patch(
                'nano_banana.api.demo.demo.ensure_output_dir',
                return_value=mock_output_dir,
            ), patch(
                'nano_banana.api.demo.demo.mock_image_path',
                return_value=mock_output_dir / 'test.png',
            ):
                await main()

                mock_client.generate.assert_called_once()
                call_kwargs = mock_client.generate.call_args.kwargs
                assert call_kwargs['prompt'] == 'A beautiful sunset'
                assert call_kwargs['images'] == []

    @pytest.mark.asyncio
    async def test_main_image_transformation(
        self,
        mock_env_vars,
        sample_image,
        tmp_path,
        temp_image_path,
    ):
        """Test main function with image transformation."""
        test_args = [
            'demo.py',
            '-p',
            'Make it colorful',
            '-i',
            str(temp_image_path),
        ]

        with patch(
            'sys.argv',
            test_args,
        ), patch(
            'nano_banana.api.demo.demo.NanoBananaClient',
        ) as mock_client_class, patch(
            'nano_banana.api.demo.demo.Path',
        ) as mock_path:
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Transformed', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with patch(
                'nano_banana.api.demo.demo.ensure_output_dir',
                return_value=mock_output_dir,
            ), patch(
                'nano_banana.api.demo.demo.mock_image_path',
                return_value=mock_output_dir / 'test.png',
            ):
                await main()

                mock_client.generate.assert_called_once()
                call_kwargs = mock_client.generate.call_args.kwargs
                assert len(call_kwargs['images']) == 1

    @pytest.mark.asyncio
    async def test_main_multiple_images(
        self,
        mock_env_vars,
        sample_image,
        tmp_path,
    ):
        """Test main function with multiple input images."""
        # Create two test images
        img1_path = tmp_path / 'img1.png'
        img2_path = tmp_path / 'img2.png'
        sample_image.save(img1_path)
        sample_image.save(img2_path)

        test_args = [
            'demo.py',
            '-p',
            'Combine these',
            '-i',
            str(img1_path),
            str(img2_path),
        ]

        with patch(
            'sys.argv',
            test_args,
        ), patch(
            'nano_banana.api.demo.demo.NanoBananaClient',
        ) as mock_client_class, patch(
            'nano_banana.api.demo.demo.Path',
        ) as mock_path:
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Combined', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with patch(
                'nano_banana.api.demo.demo.ensure_output_dir',
                return_value=mock_output_dir,
            ), patch(
                'nano_banana.api.demo.demo.mock_image_path',
                return_value=mock_output_dir / 'test.png',
            ):
                await main()

                call_kwargs = mock_client.generate.call_args.kwargs
                assert len(call_kwargs['images']) == 2

    @pytest.mark.asyncio
    async def test_main_custom_api_key(self, sample_image, tmp_path):
        """Test main function with custom API key."""
        test_args = [
            'demo.py',
            '-k',
            'custom_api_key',
            '-p',
            'Test prompt',
        ]

        with patch(
            'sys.argv',
            test_args,
        ), patch(
            'nano_banana.api.demo.demo.NanoBananaClient',
        ) as mock_client_class, patch(
            'nano_banana.api.demo.demo.Path',
        ) as mock_path:
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Text', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with patch(
                'nano_banana.api.demo.demo.ensure_output_dir',
                return_value=mock_output_dir,
            ), patch(
                'nano_banana.api.demo.demo.mock_image_path',
                return_value=mock_output_dir / 'test.png',
            ), patch(
                'nano_banana.api.demo.demo.Settings',
            ) as mock_settings_class:
                mock_settings = MagicMock()
                mock_settings.GOOGLE_API_KEY = ''
                mock_settings.MODEL_NAME = 'test-model'
                mock_settings_class.return_value = mock_settings

                await main()

                # Verify custom API key was used
                mock_client_class.assert_called_once_with(
                    api_key='custom_api_key',
                    model_name='test-model',
                )

    @pytest.mark.asyncio
    async def test_main_missing_api_key(self, monkeypatch):
        """Test main function fails without API key."""
        test_args = [
            'demo.py',
            '-p',
            'Test prompt',
        ]

        # Remove API key from environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)

        with patch(
            'sys.argv',
            test_args,
        ), patch(
            'nano_banana.api.demo.demo.Settings',
        ) as mock_settings_class:
            mock_settings = MagicMock()
            mock_settings.GOOGLE_API_KEY = ''
            mock_settings_class.return_value = mock_settings

            with pytest.raises(ValueError, match='API key is required'):
                await main()

    @pytest.mark.asyncio
    async def test_main_missing_prompt(self, mock_env_vars):
        """Test main function fails without prompt."""
        test_args = ['demo.py']

        with patch('sys.argv', test_args):
            with pytest.raises((SystemExit, ValueError)):
                await main()
