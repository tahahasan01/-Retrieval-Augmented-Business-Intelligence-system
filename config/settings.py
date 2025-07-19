from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ""
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    postgres_url: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_db: str = ""
    jwt_secret: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
