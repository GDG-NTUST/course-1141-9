#!/usr/bin/env -S uv run

"""Entry point for the GDG tutorial application."""

from nano_banana.core.config import Settings
from nano_banana.discord.bot import bot


def main() -> None:
    """Run the Nano Banana application."""
    settings = Settings()
    bot.run(settings.discord_token)
