from pydantic import BaseSettings, BaseModel
from typing import Optional, Dict, Any, List
from pydantic import BaseSettings, Field, PostgresDsn, validator, RedisDsn

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

    POSTGRES_USER: str = Field(default="user")
    POSTGRES_PASSWORD: str = Field(default="postgres_password")
    POSTGRES_DB: str = Field(default="database")
    POSTGRES_HOST: str = Field(default="127.0.0.1")
    POSTGRES_PORT: str = Field(default="5432")

    CELERY_DBURI: Optional[PostgresDsn] = None

    @validator("CELERY_DBURI", pre=True)
    def assemble_celery_dburi(cls, v: Optional[str], values: [str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=f"{values.get('POSTGRES_PORT') or ''}",
        )

    REDIS_HOST: str = Field(default="127.0.0.1")
    REDIS_PORT: int = Field(default=6379)

    REDIS_URI: Optional[RedisDsn] = None

    @validator("REDIS_URI", pre=True)
    def assemble_redis_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_HOST"),
            port=str(values.get("REDIS_PORT")),
            path="/0",
        )

    class Config:
        env_file = './.env_dev'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'


config = Settings()



