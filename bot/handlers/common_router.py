from aiogram import Router, F
from aiogram.types import Message
from bot.core.config import Settings

router = Router()

@router.message(
    F.text.contains(Settings.BOT_USERNAME)
)
async def ai_reply_handler(message: Message, cleaned_text: str):
   """
   
   """

   

