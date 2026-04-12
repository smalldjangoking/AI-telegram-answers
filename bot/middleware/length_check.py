from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

class LengthCheckMiddleware(BaseMiddleware):
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
                await event.reply(
                    f"❌ Ты дал длинный текст.\n"
                    f"Получено: {len(user_message)} симв.\n"
                    f"Лимит: {self.max_length} симв.\n"
                    f"Постарайся сократить его, чтобы я мог обработать запрос."
                )
                return
            
            if len(user_message) <= 5:
                await event.reply(
                    f"❌ Текст слишком короткий.\n"
                    f"Получено: {len(user_message)} симв.\n"
                    f"Минимум: 5 симв.\n"
                    f"Постарайся дать больше информации, чтобы я мог помочь."
                )
                return
            
            if user_message_reply and len(user_message_reply) <= 25:
                await event.reply(
                    f"❌ Текст, на который ты ссылаешься, слишком короткий.\n"
                    f"Получено: {len(user_message_reply)} симв.\n"
                    f"Минимум: 25 симв.\n"
                    f"Останавливаю анализ, так как слишком короткие тексты не дают достаточно контекста для ответа."
                )
                return
            
            if user_message_reply and len(user_message_reply) > self.max_length:
                await event.reply(
                    f"❌ Текст, на который ты ответил, слишком длинный.\n"
                    f"Получено: {len(user_message_reply)} симв.\n"
                    f"Лимит: {self.max_length} симв.\n"
                    f"Для экономии ресурсов, я не могу анализировать такие длинные тексты."
                )
                return
            
        return await handler(event, data)