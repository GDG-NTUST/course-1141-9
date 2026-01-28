"""Tests for demo script."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from PIL import Image

# Ensure src is at the very beginning of path for proper imports
src_path = Path(__file__).parent.parent.parent.parent / 'src'


def _load_demo_module() -> ModuleType:
    """Load the demo module from source path directly."""
    # Ensure src is at the very front of sys.path
    src_str = str(src_path)
    if src_str in sys.path:
        sys.path.remove(src_str)
    sys.path.insert(0, src_str)

    # Clear any cached nano_banana modules to force reimport from src
    keys_to_remove = [k for k in sys.modules if k.startswith('nano_banana')]
    for key in keys_to_remove:
        del sys.modules[key]

    demo_path = src_path / 'nano_banana' / 'api' / 'demo' / 'demo.py'
    spec = importlib.util.spec_from_file_location(
        'nano_banana.api.demo.demo',
        demo_path,
    )
    if spec is None or spec.loader is None:
        msg = f'Cannot load demo module from {demo_path}'
        raise ImportError(msg)
    demo = importlib.util.module_from_spec(spec)
    sys.modules['nano_banana.api.demo.demo'] = demo
    spec.loader.exec_module(demo)
    return demo


@pytest.fixture
def demo_module(mock_env_vars: None) -> ModuleType:
    """Import demo module with proper environment setup."""
    _ = mock_env_vars  # Required for environment setup
    return _load_demo_module()


class TestDemoUtilities:
    """Test demo utility functions."""

    def test_ensure_output_dir_creates_directory(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test ensure_output_dir creates directory if it doesn't exist."""
        new_dir = tmp_path / 'new_output'
        assert not new_dir.exists()

        result = demo_module.ensure_output_dir(new_dir)

        assert new_dir.exists()
        assert new_dir.is_dir()
        assert result == new_dir

    def test_ensure_output_dir_existing_directory(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test ensure_output_dir with existing directory."""
        existing_dir = tmp_path / 'existing'
        existing_dir.mkdir()

        result = demo_module.ensure_output_dir(existing_dir)

        assert existing_dir.exists()
        assert result == existing_dir

    def test_ensure_output_dir_creates_parent_dirs(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test ensure_output_dir creates parent directories."""
        nested_dir = tmp_path / 'parent' / 'child' / 'output'

        result = demo_module.ensure_output_dir(nested_dir)

        assert nested_dir.exists()
        assert result == nested_dir

    def test_mock_image_path_format(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test mock_image_path generates correct format."""
        output_dir = tmp_path

        result = demo_module.mock_image_path(output_dir)

        assert result.parent == output_dir
        assert result.name.startswith('nano-banana-')
        assert result.suffix == '.png'

    def test_mock_image_path_custom_suffix(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test mock_image_path with custom suffix."""
        output_dir = tmp_path

        result = demo_module.mock_image_path(output_dir, suffix='jpg')

        assert result.suffix == '.jpg'

    def test_mock_image_path_unique(
        self,
        demo_module: ModuleType,
        tmp_path: Path,
    ) -> None:
        """Test mock_image_path generates unique paths."""
        output_dir = tmp_path

        path1 = demo_module.mock_image_path(output_dir)
        path2 = demo_module.mock_image_path(output_dir)

        assert path1 != path2


class TestDemoMain:
    """Test demo main function."""

    @pytest.mark.asyncio
    async def test_main_text_to_image(
        self,
        demo_module: ModuleType,
        sample_image: Image.Image,
        tmp_path: Path,
    ) -> None:
        """Test main function with text-to-image generation."""
        test_args = [
            'demo.py',
            '-p',
            'A beautiful sunset',
        ]

        with (
            patch(
                'sys.argv',
                test_args,
            ),
            patch(
                'nano_banana.api.demo.demo.NanoBananaClient',
            ) as mock_client_class,
            patch(
                'nano_banana.api.demo.demo.Path',
            ) as mock_path,
        ):
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

            with (
                patch(
                    'nano_banana.api.demo.demo.ensure_output_dir',
                    return_value=mock_output_dir,
                ),
                patch(
                    'nano_banana.api.demo.demo.mock_image_path',
                    return_value=mock_output_dir / 'test.png',
                ),
            ):
                await demo_module.main()

                mock_client.generate.assert_called_once()
                call_kwargs = mock_client.generate.call_args.kwargs
                assert call_kwargs['prompt'] == 'A beautiful sunset'
                assert call_kwargs['images'] == []

    @pytest.mark.asyncio
    async def test_main_image_transformation(
        self,
        demo_module: ModuleType,
        sample_image: Image.Image,
        tmp_path: Path,
        temp_image_path: Path,
    ) -> None:
        """Test main function with image transformation."""
        test_args = [
            'demo.py',
            '-p',
            'Make it colorful',
            '-i',
            str(temp_image_path),
        ]

        with (
            patch(
                'sys.argv',
                test_args,
            ),
            patch(
                'nano_banana.api.demo.demo.NanoBananaClient',
            ) as mock_client_class,
            patch(
                'nano_banana.api.demo.demo.Path',
            ) as mock_path,
        ):
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Transformed', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with (
                patch(
                    'nano_banana.api.demo.demo.ensure_output_dir',
                    return_value=mock_output_dir,
                ),
                patch(
                    'nano_banana.api.demo.demo.mock_image_path',
                    return_value=mock_output_dir / 'test.png',
                ),
            ):
                await demo_module.main()

                mock_client.generate.assert_called_once()
                call_kwargs = mock_client.generate.call_args.kwargs
                assert len(call_kwargs['images']) == 1

    @pytest.mark.asyncio
    async def test_main_multiple_images(
        self,
        demo_module: ModuleType,
        sample_image: Image.Image,
        tmp_path: Path,
    ) -> None:
        """Test main function with multiple input images."""
        # Create two test images
        img_count = 2
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

        with (
            patch(
                'sys.argv',
                test_args,
            ),
            patch(
                'nano_banana.api.demo.demo.NanoBananaClient',
            ) as mock_client_class,
            patch(
                'nano_banana.api.demo.demo.Path',
            ) as mock_path,
        ):
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Combined', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with (
                patch(
                    'nano_banana.api.demo.demo.ensure_output_dir',
                    return_value=mock_output_dir,
                ),
                patch(
                    'nano_banana.api.demo.demo.mock_image_path',
                    return_value=mock_output_dir / 'test.png',
                ),
            ):
                await demo_module.main()

                call_kwargs = mock_client.generate.call_args.kwargs
                assert len(call_kwargs['images']) == img_count

    @pytest.mark.asyncio
    async def test_main_custom_api_key(
        self,
        demo_module: ModuleType,
        sample_image: Image.Image,
        tmp_path: Path,
    ) -> None:
        """Test main function with custom API key."""
        test_args = [
            'demo.py',
            '-k',
            'custom_api_key',
            '-p',
            'Test prompt',
        ]

        with (
            patch(
                'sys.argv',
                test_args,
            ),
            patch(
                'nano_banana.api.demo.demo.NanoBananaClient',
            ) as mock_client_class,
            patch(
                'nano_banana.api.demo.demo.Path',
            ) as mock_path,
        ):
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Text', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with (
                patch(
                    'nano_banana.api.demo.demo.ensure_output_dir',
                    return_value=mock_output_dir,
                ),
                patch(
                    'nano_banana.api.demo.demo.mock_image_path',
                    return_value=mock_output_dir / 'test.png',
                ),
                patch(
                    'nano_banana.api.demo.demo.Settings',
                ) as mock_settings_class,
            ):
                mock_settings = MagicMock()
                mock_settings.GOOGLE_API_KEY = ''
                mock_settings.MODEL_NAME = 'test-model'
                mock_settings_class.return_value = mock_settings

                await demo_module.main()

                # Verify custom API key was used
                mock_client_class.assert_called_once()
                call_kwargs = mock_client_class.call_args.kwargs
                assert call_kwargs['api_key'] == 'custom_api_key'
                assert call_kwargs['model_name'] == 'test-model'

    @pytest.mark.asyncio
    async def test_main_missing_api_key(
        self,
        demo_module: ModuleType,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test main function fails without API key."""
        test_args = [
            'demo.py',
            '-p',
            'Test prompt',
        ]

        # Remove API key from environment
        monkeypatch.delenv('GOOGLE_API_KEY', raising=False)

        with (
            patch(
                'sys.argv',
                test_args,
            ),
            patch(
                'nano_banana.api.demo.demo.Settings',
            ) as mock_settings_class,
        ):
            mock_settings = MagicMock()
            mock_settings.GOOGLE_API_KEY = ''
            mock_settings_class.return_value = mock_settings

            with pytest.raises(ValueError, match='API key is required'):
                await demo_module.main()

    @pytest.mark.asyncio
    async def test_main_empty_prompt(
        self,
        demo_module: ModuleType,
        sample_image: Image.Image,
        tmp_path: Path,
    ) -> None:
        """Test main function with empty prompt uses empty string."""
        test_args = ['demo.py', '-k', 'test_key']

        with (
            patch('sys.argv', test_args),
            patch(
                'nano_banana.api.demo.demo.NanoBananaClient',
            ) as mock_client_class,
            patch(
                'nano_banana.api.demo.demo.Path',
            ) as mock_path,
        ):
            mock_client = MagicMock()
            mock_client.generate = AsyncMock(
                return_value=('Response', sample_image),
            )
            mock_client_class.return_value = mock_client

            mock_path.return_value.parent = tmp_path
            mock_output_dir = tmp_path / 'outputs'
            mock_output_dir.mkdir()

            with (
                patch(
                    'nano_banana.api.demo.demo.ensure_output_dir',
                    return_value=mock_output_dir,
                ),
                patch(
                    'nano_banana.api.demo.demo.mock_image_path',
                    return_value=mock_output_dir / 'test.png',
                ),
            ):
                await demo_module.main()

                # Verify generate was called with empty prompt
                call_kwargs = mock_client.generate.call_args.kwargs
                assert call_kwargs['prompt'] == ''
