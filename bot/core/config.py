from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BOT_TOKEN: str = "YOUR_BOT_TOKEN"
    BOT_USERNAME: str = "YOUR_BOT_USERNAME"
    MAX_MESSAGE_LENGTH: int = 4000
    SLOW_MODE_DELAY: int = 1200  # 20 minutes in seconds
    OPENAI_API_KEY: str = "YOUR_OPENAI_API_KEY"
    ALLOWED_CHAT_ID: int = 0  # Set to your allowed chat ID
    OPENAI_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()