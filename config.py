from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

DOTENV = os.path.join(os.path.dirname(__file__), ".env")
class DbSettings(BaseSettings):
    DB_HOST: str = Field(default='localhost')
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default='postgres')
    DB_PASSWORD: str = Field(default='postgres')
    DB_NAME: str = Field(default='db')

    @property
    def DB_URL_ASYNCPG(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def DB_URL_PSYCOPG(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(env_file=DOTENV)


class Settings(BaseSettings):
    db: DbSettings = DbSettings()


settings = Settings()
