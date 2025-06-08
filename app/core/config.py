from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class Setting(BaseSettings):
    MY_DB_URL: str

    model_config = SettingsConfigDict(
        env_file = BASE_DIR / '.env'
    )


settings = Setting()
print(settings.MY_DB_URL)
