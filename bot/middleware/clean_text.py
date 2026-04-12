from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

class CleanTextMiddleware(BaseMiddleware):
    def __init__(self, bot_username: str):
        self.bot_username = bot_username
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        if not isinstance(event, Message):
            return await handler(event, data)

        text = event.text or event.caption or ""

        low_text = text.lower()
        cleaned = low_text.replace(f"@{self.bot_username.lower()}", "").strip()
        
        data["cleaned_text"] = cleaned

        return await handler(event, data)