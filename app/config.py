import os

from celery import Celery
from starlette.config import Config
from pydantic_settings import BaseSettings, SettingsConfigDict


dir_path = os.path.dirname(os.path.realpath(__file__))
root_dir = dir_path[:-3]
config = Config(f'{root_dir}.env')

DB_USER = config('DB_USER', cast=str)
PASSWORD = config('PASSWORD', cast=str)
DB_HOST = config('DB_HOST', cast=str)
DB_PORT = config('DB_PORT', cast=str)
DB_NAME = config('DB_NAME', cast=str)

PATH_TO_ENV_FILE = root_dir + '.env'


class Settings(BaseSettings):
    db_user: str
    password: str
    db_host: str
    db_port: str
    db_name: str
    test_db_name: str
    db_test_port: str
    redis_host: str
    redis_port: str
    path_to_table: str
    broker_url: str
    check_interval: str
    app_host: str
    app_port: str
    model_config = SettingsConfigDict(
        env_file='.env', extra='ignore', env_file_encoding='utf-8')


settings = Settings(
    _env_file=PATH_TO_ENV_FILE,
    extra='ignore',
    env_file_encoding='utf-8',
)
DB_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_port}/{settings.db_name}'
TEST_DB_URL = f'postgresql+asyncpg://{settings.db_user}:{settings.password}@{settings.db_host}:{settings.db_test_port}/{settings.test_db_name}'
celery = Celery('table_monitoring', broker=settings.broker_url)
