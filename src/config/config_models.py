from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class BotConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='TGBOT_')
    token: str


load_dotenv()
bot_config = BotConfig()