from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    broker_url:str
    ollama_url:str

    class Config:
        env_file = ".env"

settings = Settings()
