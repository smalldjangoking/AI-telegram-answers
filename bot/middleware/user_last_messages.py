from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable


class UserLastMessagesMiddleware(BaseMiddleware):
    def __init__(self):
        self.messages: Dict[int, list[Dict]] = {}
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Caches user message history within a one-hour rolling window into temp dictionary, 
        filtering out expired entries for AI context.
        """
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id

            if user_id not in self.messages:
                self.messages[user_id] = []

            self.messages[user_id] = [
                msg for msg in self.messages[user_id] if msg["time"] > hour_ago
            ]

            data["user_history"] = self.messages[user_id]

            self.messages[user_id].append({"text": data["cleaned_text"], "time": now})

        return await handler(event, data)
