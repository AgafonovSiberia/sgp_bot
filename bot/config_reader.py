from pydantic import BaseSettings, BaseModel

class DB(BaseModel):
    host: str
    user: str
    port: int
    name: str
    password: str


class GSAPI(BaseModel):
    key_path: str
    id: str


class Settings(BaseSettings):
    bot_token: str
    channel_id: str
    db: DB
    gsapi: GSAPI

    class Config:
        env_file = '../.env_dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()

