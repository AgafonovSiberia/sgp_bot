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


class DB(BaseModel):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int


class Settings(BaseSettings):
    bot_token: str
    channel_id: str
    GSAPI_ID: str
    GSAPI_SERVICE_KEY: ServiceKey
    db: DB

    class Config:
        env_file = './.env_dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()



