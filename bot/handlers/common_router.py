from aiogram import Router, F
from aiogram.types import Message
from bot.core.config import settings
from bot.services.openai_service import OpenAIService
from bot.core.constants import waiting_messages, aggressive_waiting_messages
import random

router = Router()

@router.message(
    F.text.contains(settings.BOT_USERNAME)
)
async def ai_reply_handler(
    message: Message, 
    cleaned_text: str,
    user_history: list[dict[str, str]],
    openai_service: OpenAIService):
    """
    Handler for messages that mention the bot. 
    
    It processes the message, optionally includes the context from a replied message, 
    and sends a request to the OpenAI service for an answer. The response is then sent back to the user.
    """
    reply_context = None
    if message.reply_to_message:
        reply_context = message.reply_to_message.text or message.reply_to_message.caption

    wait_msg = await message.reply("⏳ Думаю..." + random.choice(waiting_messages))

    answer = await openai_service.get_answer(
        prompt=cleaned_text,
        context=reply_context,
        user_history=user_history

    )

    await wait_msg.edit_text(answer)


@router.message(
    F.reply_to_message,
    F.reply_to_message.from_user.id == F.bot.id
)
async def ai_reply_to_bot_handler(
    message: Message, 
    cleaned_text: str, 
    user_history: list[dict[str, str]],
    openai_service: OpenAIService
    ):
    """Handler for messages that are replies to the bot."""

    bot_old_message = None
    if message.reply_to_message:
        bot_old_message = message.reply_to_message.text or message.reply_to_message.caption

    wait_msg = await message.reply("⏳ Думаю..." + random.choice(aggressive_waiting_messages))

    answer = await openai_service.get_answer(
        prompt=cleaned_text,
        context=f"Твой предыдущий ответ: {bot_old_message}",
        user_history=user_history
    )

    await wait_msg.edit_text(answer)

