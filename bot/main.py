import asyncio
from aiogram import Bot, Dispatcher
from bot.core.config import settings
from bot.handlers import routers
from bot.middleware import (
    CleanTextMiddleware,
    LengthCheckMiddleware,
    ThrottlingMiddleware,
    RestrictionMiddleware,
    UserLastMessagesMiddleware
)
from bot.services.openai_service import OpenAIService

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher()
    openai_service = OpenAIService(api_key=settings.OPENAI_API_KEY)

    middlewares = [
        RestrictionMiddleware(allowed_chat_id=settings.ALLOWED_CHAT_ID),
        #ThrottlingMiddleware(slow_mode_delay=settings.SLOW_MODE_DELAY),
        CleanTextMiddleware(bot_username=settings.BOT_USERNAME),
        LengthCheckMiddleware(max_length=settings.MAX_MESSAGE_LENGTH),
        UserLastMessagesMiddleware(),
    ]

    print("=================================")
    print("🤖 Bot started!")
    print("=================================")

    for middleware in middlewares:
        dp.message.middleware(middleware)

    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot, openai_service=openai_service),
    )

if __name__ == "__main__":
    asyncio.run(main())