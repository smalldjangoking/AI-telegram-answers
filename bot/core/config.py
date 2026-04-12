from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str = "YOUR_BOT_TOKEN"
    BOT_USERNAME: str = "YOUR_BOT_USERNAME"
    MAX_MESSAGE_LENGTH: int = 4000
    SLOW_MODE_DELAY: int = 1200  # 20 minutes in seconds