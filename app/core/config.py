# from pathlib import Path 
from pydantic_settings import BaseSettings 

# BASE_DIR = Path(__file__).parent.parent

class Setting(BaseSettings):
    DATABASE_URL: str 

    class Config:
        env_file = '.env'
# settings = Setting()