import asyncio

import discord

from nano_banana.api.client import NanoBananaClient
from nano_banana.core.config import Settings, logging
from nano_banana.discord import utils

logger = logging.getLogger(__name__)
settings = Settings()
banana = NanoBananaClient(
    api_key=settings.GOOGLE_API_KEY,
    model_name=settings.MODEL_NAME,
    system_prompt=settings.SYSTEM_PROMPT,
)
bot = discord.Bot(
    intents=discord.Intents.all(),
    member_cache_flags=discord.MemberCacheFlags.all(),
)


@bot.slash_command(
    name='draw',
    description='draw me a image from prompt',
    name_localizations={'zh-TW': '畫圖', 'zh-CN': '画图'},
    description_localizations={
        'zh-TW': '由提示詞生成一張圖片',
        'zh-CN': '由提示词生成一张图片',
    },
)
async def draw(ctx: discord.ApplicationContext, prompt: str) -> None:
    await ctx.defer()
    logger.info('Receive draw command from %s: %s', ctx.author, prompt)
    resp_text, resp_image = await banana.generate(
        prompt=prompt,
    )

    await utils.respond(ctx.respond, resp_text, resp_image)


def _extract_image_urls(message: discord.Message) -> list[str]:
    """Extract image URLs from message attachments."""
    return [
        att.url
        for att in message.attachments
        if att.content_type and att.content_type.startswith('/image')
    ]


async def _fetch_reference_images(message: discord.Message) -> list[str]:
    """Fetch image URLs from referenced message."""
    img_urls = []
    if (ref := message.reference) and (ref_message_id := ref.message_id):
        try:
            ref_msg = await message.channel.fetch_message(ref_message_id)
            img_urls.extend(
                att.url
                for att in ref_msg.attachments
                if att.content_type and att.content_type.startswith('image/')
            )
        except discord.HTTPException as e:
            logger.warning('Cannot fetch reference message: %s', e)
            await message.channel.send(f'發生錯誤: {e}')
        except Exception as e:
            logger.exception('Unexpected error occurred:')
            await message.channel.send(f'發生未預期的錯誤: {e}')
    return img_urls


async def _generate_response(message: discord.Message, prompt: str, pil_images: list) -> None:
    """Generate and send AI response."""
    try:
        resp_text, resp_image = await banana.generate(
            prompt=prompt,
            images=pil_images if pil_images else None,
        )
        await utils.respond(message.reply, resp_text, resp_image)
    except (discord.HTTPException, ValueError, RuntimeError) as e:
        logger.exception('Error occurred during generation:')
        await message.channel.send(f'發生錯誤: {e}')
    except Exception as e:
        logger.exception('Unexpected error occurred:')
        await message.channel.send(f'發生未預期的錯誤: {e}')


@bot.listen()
async def on_message(message: discord.Message) -> None:
    if message.author.bot or (
        message.guild and message.guild.id != settings.discord_guild_id
    ):
        return

    prompt = message.content or ''
    img_urls = _extract_image_urls(message)
    img_urls.extend(await _fetch_reference_images(message))

    if len(img_urls) > settings.MAX_IMAGE_PER_REQUEST:
        await message.channel.send(
            f'一次最多只能處理 {settings.MAX_IMAGE_PER_REQUEST} 張圖片喔！',
        )
        return

    logger.info(
        'Receive message from %s: Content="%s", Images=%d',
        message.author,
        prompt,
        len(img_urls),
    )

    pil_images = []
    if img_urls:
        logger.info('Downloading %d images...', len(img_urls))
        pil_images = await asyncio.gather(*map(utils.download_image, img_urls))

    async with message.channel.typing():
        await _generate_response(message, prompt, pil_images)


@bot.listen(once=True)
async def on_ready() -> None:
    logger.info('Client is ready!')
