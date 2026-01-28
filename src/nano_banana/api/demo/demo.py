#!/usr/bin/env -S uv run

import argparse
import asyncio
import uuid
from pathlib import Path

from PIL import Image

from nano_banana.api.client import NanoBananaClient
from nano_banana.core.config import Settings, logging

parser = argparse.ArgumentParser(
    description='A simple example of argparse usage.',
)
parser.add_argument(
    '-k',
    '--key',
    type=str,
    help='API key for authentication.',
)
parser.add_argument(
    '-p',
    '--prompt',
    type=str,
    help='Text prompt for image generation.',
)
parser.add_argument(
    '-i',
    '--image',
    type=str,
    nargs='*',
    help='Path(s) to input image(s) for transformation.',
)


def ensure_output_dir(base_dir: Path) -> Path:
    """Ensure the output directory exists.

    Args:
        base_dir: Target directory path.

    Returns:
        The ensured directory path.
    """

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def mock_image_path(output_dir: Path, suffix: str = 'png') -> Path:
    """Build a mock file path for generated images.

    Args:
        output_dir: Directory in which to place the mock file.
        suffix: File suffix to use.

    Returns:
        A path pointing to the mock image file.
    """

    return output_dir / f'nano-banana-{uuid.uuid4().hex}.{suffix}'


async def main() -> None:
    args = parser.parse_args()
    settings = Settings()
    logger = logging.getLogger(__name__)

    if not (api_key := args.key or settings.GOOGLE_API_KEY):
        msg = 'API key is required.'
        raise ValueError(msg)

    prompt = args.prompt or ''
    image_paths = args.image or []
    if image_paths and len(image_paths) > settings.MAX_IMAGE_PER_REQUEST:
        msg = f'Number of input images exceeds the maximum of {settings.MAX_IMAGE_PER_REQUEST}.'
        raise ValueError(msg)

    output_dir = ensure_output_dir(Path(__file__).parent / 'outputs')

    images = []
    for p in image_paths:
        with Image.open(p) as img:
            images.append(img.convert('RGB').copy())

    nano_banana = NanoBananaClient(
        api_key=api_key,
        model_name=settings.MODEL_NAME,
        system_prompt=settings.SYSTEM_PROMPT,
    )
    try:
        resp_text, resp_image = await nano_banana.generate(
            prompt=prompt,
            images=images,
        )
    except Exception:
        logger.exception('Error occurred during generation:')
        return

    if not resp_text and not resp_image:
        logger.warning('No response generated from the model.')
        return

    if resp_text:
        logger.info('Generated text response: %s', resp_text)
    if resp_image:
        output_path = mock_image_path(output_dir)
        resp_image.save(output_path)
        logger.info('Generated image saved to: %s', output_path)
        resp_image.show()

if __name__ == '__main__':
    asyncio.run(main())
