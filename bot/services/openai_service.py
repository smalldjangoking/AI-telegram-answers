import logging
from openai import AsyncOpenAI, APITimeoutError, APIConnectionError, RateLimitError, InternalServerError
from openai.types.chat import ChatCompletionMessageParam
from bot.core.config import settings

from bot.services.base_prompt_service import UkrainianRealityBasePrompt

from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
    retry_if_exception_type
)

system_instruction = UkrainianRealityBasePrompt()

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = settings.OPENAI_MODEL

    @retry(
        wait=wait_random_exponential(min=1, max=10),
        stop=stop_after_attempt(3),
        retry=retry_if_exception_type(
            (APITimeoutError, APIConnectionError, 
             RateLimitError, InternalServerError)
        ),
        reraise=True
    )
    async def _make_openai_request(self, messages: list[ChatCompletionMessageParam]) -> str:
        """Private method to make OpenAI API requests with retry logic for transient errors."""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=100
        )
        content = response.choices[0].message.content
        return content if content is not None else ""

    async def get_answer(
        self, 
        prompt: str, 
        context: str | None = None,
        user_history: list[dict[str, str]] | None = None
        ) -> str:
        """Public method to get an answer from OpenAI based on the prompt and optional context."""

        #system base prompt
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": system_instruction.generate_system_prompt()}
        ]

        if context:
            messages.append(
                {
                    "role": "user", 
                    "content": f"Контекст на который ссылается пользователь "
                    f"(Сообщение пользователя или новость.):\n{context}"}
            )

        #New User message
        messages.append(
            {
                "role": "user", 
                "content": f"Новое сообщение от пользователя:\n{prompt}"}
        )

        if user_history:
            for message in user_history:
                messages.append(
                    {
                        "role": "user", 
                        "content": f"Предыдущее сообщение от пользователя:\n{message['text']}"}
                )

        try:
            content = await self._make_openai_request(messages)

            return content if content is not None else "❌ Извини, нейросеть сейчас недоступна. Попробуй позже."

        except Exception as e:
            logging.error(f"Ошибка OpenAI: {e}")
            return "❌ Произошла ошибка при обращении к нейросети. Попробуй позже."