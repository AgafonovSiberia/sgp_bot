import os


class Settings:
    bot_token = os.environ.get("BOT_TOKEN")
    db_url = os.environ.get("DB_URL")
    channel_id = os.environ.get("CHANNEL_ID")
    GSAPI_ID = os.environ.get("GSAPI_ID")
    GSAPI_SERVICE_KEY = os.environ.get("GSAPI_SERVICE_KEY").replace('\n', '')


config = Settings()