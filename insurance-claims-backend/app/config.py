from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "insurance_claims"

    class Config:
        env_file = ".env"


settings = Settings()
