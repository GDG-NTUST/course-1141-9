"""Entry point for the GDG tutorial application."""

from nano_banana.core.config import Settings
from nano_banana.discord.bot import bot

if __name__ == '__main__':
    settings = Settings()
    bot.run(settings.discord_token)
