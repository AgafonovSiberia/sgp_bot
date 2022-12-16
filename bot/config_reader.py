from pydantic import BaseSettings, BaseModel


class ServiceKey(BaseModel):
    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str

class Settings(BaseSettings):
    bot_token: str
    channel_id: str
    GSAPI_ID: str
    GSAPI_URL: str
    GSAPI_SERVICE_KEY: ServiceKey
    postgres_user: str
    postgres_password: str
    postgres_db: str

    class Config:
        env_file = './.env_dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()



