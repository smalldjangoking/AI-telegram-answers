from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from typing import Callable, Dict, Any, Awaitable

class RestrictionMiddleware(BaseMiddleware):
    def __init__(self, allowed_chat_id: int):
        self.allowed_chat_id = allowed_chat_id
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        if not isinstance(event, Message):
            return await handler(event, data)
        
        if event.chat.id != self.allowed_chat_id:
            if event.chat.type == "private":
                await event.answer("⛔ Я приватный бот и работаю только в закрытой группе.")
        
            if event.chat.type in ["group", "supergroup"]:
                    bot = data.get("bot")
                    if bot:
                        await bot.leave_chat(event.chat.id)
            return
        
        return await handler(event, data)
            
        
