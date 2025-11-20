from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # DB
    DATABASE_URL: str

    # AUTH
    AUTH0_DOMAIN: str
    AUTH0_AUDIENCE: str | None = None
    AUTH0_ALGORITHMS: str = "RS256"

    # DEBUG MODE
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
