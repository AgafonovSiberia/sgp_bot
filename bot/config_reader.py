from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    db_url: str
    channel_id: str
    GSAPI_ID: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'

config = Settings()

