from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "MindBuilder Human OS"
    VERSION: str = "1.0.0"
    
    # .env 파일과 일치하는 기본값 설정
    POSTGRES_USER: str = Field(default="mindbuilder_user")
    POSTGRES_PASSWORD: str = Field(default="mindbuilder_password")
    POSTGRES_SERVER: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str = Field(default="mindbuilder")

    # 인증 설정
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    @property
    def sync_database_url(self) -> str:
        # Alembic (동기식)
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def async_database_url(self) -> str:
        # FastAPI 앱 (비동기식)
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()