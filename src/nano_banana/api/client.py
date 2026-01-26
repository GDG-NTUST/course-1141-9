"""Google Gemini image generator client (Async Version)."""

import asyncio
import io
import logging
from typing import NoReturn

from google import genai
from PIL import Image, ImageFile


class NanoBananaClient:
    """Google Gemini image generator client."""

    def __init__(
        self,
        api_key: str,
        model_name: str,
        system_prompt: str = '',
    ) -> None:
        if not api_key:
            msg = 'Google API key is required'
            self._raise_value_error(msg)

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.logger = logging.getLogger(__name__)
        self.logger.info(
            'NanoBananaClient initialized with model=%s',
            self.model_name,
        )

    async def generate(
        self,
        prompt: str,
        images: list[Image.Image | ImageFile.ImageFile] | None = None,
    ) -> tuple[str, Image.Image | None]:
        """Generate or transform an image using Gemini asynchronously.

        If images are provided, transforms them based on the prompt.
        Otherwise, generates an image from the text prompt.
        """

        if not prompt and not self.system_prompt:
            self._raise_value_error('Prompt is required.')

        contents: list[str | Image.Image | ImageFile.ImageFile] = (
            [self.system_prompt, prompt, *images]
            if images
            else [self.system_prompt, prompt]
        )

        self.logger.info(
            "Sending request to Gemini (Mode: %s)",
            "Image Transform" if images else "Text to Image",
        )
        try:
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=contents,
            )

            if not response.parts:
                self._raise_value_error('Empty response from Gemini model.')

            resp_texts: list[str] = []
            resp_image: Image.Image | None = None
            for part in response.parts:
                if part.text:
                    resp_texts.append(part.text)

                if (part.inline_data) and (image_bytes := part.inline_data.data):
                    resp_image = await asyncio.to_thread(
                        self._bytes_to_pil,
                        image_bytes,
                    )

            return ''.join(resp_texts), resp_image

        except Exception:
            self.logger.exception('Failed to generate image')
            raise

    @staticmethod
    def _bytes_to_pil(data: bytes) -> Image.Image:
        """Converts raw bytes to a PIL Image ensuring data is loaded."""
        with io.BytesIO(data) as bio:
            img = Image.open(bio)
            img.load()
            return img

    @staticmethod
    def _raise_value_error(msg: str) -> NoReturn:
        raise ValueError(msg)
