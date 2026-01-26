import io
from collections.abc import Awaitable, Callable

import discord
import httpx
from PIL import Image


async def download_image(url: str) -> Image.Image:
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        return Image.open(io.BytesIO(resp.content))

async def respond(func: Callable[..., Awaitable], text: str, image: Image.Image | None) -> None:
    if not text and not image:
        await func('我不知道該說什麼')
        return

    if image:
        with io.BytesIO() as image_binary:
            image.save(image_binary, format='PNG')
            image_binary.seek(0)

            await func(
                content=text,
                file=discord.File(fp=image_binary, filename='image.png'),
            )
            return
    await func(content=text)
