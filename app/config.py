from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SLACK_BOT_TOKEN:str
    SLACK_SIGNING_SECRET:str
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DATABASE_URL:str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
