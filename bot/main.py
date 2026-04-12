import asyncio
from aiogram import Bot, Dispatcher
from bot.core.config import Settings
from bot.handlers import routers
from bot.middleware import (
    CleanTextMiddleware,
    LengthCheckMiddleware,
    ThrottlingMiddleware,
)

async def main():
    bot = Bot(token=Settings.BOT_TOKEN)
    dp = Dispatcher()

    dp.message.middleware(
        ThrottlingMiddleware(slow_mode_delay=Settings.SLOW_MODE_DELAY),
    )
    dp.message.middleware(
        CleanTextMiddleware(bot_username=Settings.BOT_USERNAME),
    )
    dp.message.middleware(
        LengthCheckMiddleware(max_length=Settings.MAX_MESSAGE_LENGTH),
    )

    dp.include_routers(*routers)

    await bot.delete_webhook(drop_pending_updates=True)
    await asyncio.gather(
        dp.start_polling(bot),
    )

if __name__ == "__main__":
    asyncio.run(main())