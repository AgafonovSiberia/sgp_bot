from pydantic import BaseSettings, BaseModel
import json

def json_to_file(json_str):
    with open("google_sheets_api/access_keys/key.json", "w") as file:
        json.dump(json_str, file)


class DB(BaseModel):
    host: str
    user: str
    port: int
    name: str
    password: str


class GSAPI(BaseModel):
    id: str
    service_key: str


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
