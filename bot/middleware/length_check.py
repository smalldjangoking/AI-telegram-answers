from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

from bot.helpers.messages import MiddlewareAssistant

class LengthCheckMiddleware(BaseMiddleware, MiddlewareAssistant):
    def __init__(self, max_length: int):
        self.max_length = max_length
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            user_message = data.get("cleaned_text") or event.text or event.caption or ""
            user_message_reply = None

            if event.reply_to_message:
                user_message_reply = event.reply_to_message.text or event.reply_to_message.caption or ""

            if len(user_message) > self.max_length:
                return await self._reject(event, 
                f"❌ Ты дал длинный текст.\n"
                f"Получено: {len(user_message)} симв. (Лимит: {self.max_length})")
            
            if len(user_message) <= 5:
                return await self._reject(event,
                f"❌ Текст слишком короткий.\n"
                f"Получено: {len(user_message)} симв. (Минимум: 5)")

            if user_message_reply and len(user_message_reply) <= 15:
                return await self._reject(event,
                    f"❌ Текст в реплае слишком короткий ({len(user_message_reply)} симв.).\n"
                    f"Нужно минимум 25 симв. для внятного анализа.")
            
            if user_message_reply and len(user_message_reply) > self.max_length:
                return await self._reject(event, 
                    f"❌ Текст в реплае слишком длинный ({len(user_message_reply)} симв.).\n"
                    f"Лимит: {self.max_length}.")
            
        return await handler(event, data)