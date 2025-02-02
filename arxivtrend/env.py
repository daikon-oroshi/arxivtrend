from typing import List
from pydantic_settings import (
    BaseSettings, SettingsConfigDict
)


class Env(BaseSettings):

    MONGO_HOST: str
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = 'arxiv'
    MONGO_USER: str
    MONGO_PASSWORD: str

    TEMPLATE_PATH: str
    REPORT_SAVE_DIR: str

    STOP_WORD_DIR: str
    STOP_WORD_FILES: List[str] = []

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file='.env'
    )


env = Env()
