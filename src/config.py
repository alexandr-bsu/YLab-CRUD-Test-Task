from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from enum import Enum
import os

DOCKER_MODE = os.getenv("MODE")
DOTENV = os.path.join(os.path.dirname(__file__), "../.test.env")

if DOCKER_MODE == 'DEV':
    DOTENV = os.path.join(os.path.dirname(__file__), "../.prod.env")

if DOCKER_MODE == 'TEST':
    DOTENV = os.path.join(os.path.dirname(__file__), "../.test.env")


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

    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')


class RedisSettings(BaseSettings):
    REDIS_HOST: str = Field(default='localhost')

    @property
    def REDIS_URL(self):
        return f'redis://{self.REDIS_HOST}:6379/'

    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')


# Режимы работы приложения
class Mode(Enum):
    DEV = 'DEV'
    TEST = 'TEST'


class Settings(BaseSettings):
    db: DbSettings = DbSettings()
    redis: RedisSettings = RedisSettings()
    MODE: Mode

    model_config = SettingsConfigDict(env_file=DOTENV, extra='ignore')


settings = Settings()
