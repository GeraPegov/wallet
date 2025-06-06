from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path('D:/проекты/Wallet')


class Setting(BaseSettings):
    MY_DB_URL: str

    class Config:
        env_file = BASE_DIR / '.env'


settings = Setting()