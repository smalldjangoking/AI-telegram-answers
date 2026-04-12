import time
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable
from bot.helpers.messages import MiddlewareAssistant

class ThrottlingMiddleware(BaseMiddleware, MiddlewareAssistant):
    def __init__(self, slow_mode_delay: int = 1200):
        self.users: Dict[int, float] = {}
        self.delay = slow_mode_delay
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
            current_time = time.time()
            last_time = self.users.get(user_id, 0.0)

            if current_time - last_time < self.delay:
                time_left = int(self.delay - (current_time - last_time))
                minutes_left = time_left // 60
                
                await self._reject(event,
                    f"⏳ Подожди {minutes_left} мин. перед следующим сообщением.")
                return
            
            self.users[user_id] = current_time
        
        return await handler(event, data)