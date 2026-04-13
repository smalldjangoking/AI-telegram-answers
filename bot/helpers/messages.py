import asyncio
import logging
from aiogram.types import Message

class MiddlewareAssistant:
    """
    A helper class providing utility methods for middlewares, 
    such as temporary message rejection.
    """

    async def _delete_message_after_delay(self, message: Message, delay: int):
        """
        Internal method to wait and delete a message.
        """
        await asyncio.sleep(delay)
        try:
            await message.delete()
        except Exception as e:
            # Silent fail if message is already deleted
            logging.info(f"Temporary message deletion failed: {e}")

    async def _reject(self, event: Message, text: str, delay: int = 60) -> None:
        """
        Sends a rejection message to the user and schedules its automatic deletion.

        This method is used to notify the user about a validation failure 
        without cluttering the chat history.

        :param event: The original Message object from the user.
        :param text: The error message text to be sent.
        :param delay: Delay in seconds before the message is deleted.
        :return: Always returns None to stop the middleware chain.
        """
        notification = await event.reply(
            f"{text}\n\n(This message will be deleted in {delay}s.)"
        )
        
        # Schedule deletion in the background
        asyncio.create_task(self._delete_message_after_delay(notification, delay))
        
        return None