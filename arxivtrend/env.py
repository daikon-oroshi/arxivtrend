from pydantic import (
    BaseSettings, validator
)


class Env(BaseSettings):

    MONGO_HOST: str
    MONGO_PORT: int = 27017
    MONGO_DB_NAME: str = 'arxiv'
    MONGO_USER: str
    MONGO_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = '.env'


env = Env()
