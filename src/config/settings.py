from enum import Enum
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    app_name: str = Field(default="RecipeApp")
    app_description: str = Field(default="AI driven Recipe Platform")
    app_environment: Environment = Field(default=Environment.DEVELOPMENT)
    port: int = Field(default=8000, alias="PORT")
    allowed_origins: list[str] = Field(default=[])

    # Database
    DATABASE_URL: str | None = None
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "recipe_db"
    
    # Connection Pool Settings
    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 10
    POSTGRES_POOL_TIMEOUT: int = 30
    POSTGRES_COMMAND_TIMEOUT: int = 60

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            # Handle Railway/Heroku style postgres URLs and replace scheme for asyncpg
            url = self.DATABASE_URL
            if url.startswith("postgres://"):
                url = url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif url.startswith("postgresql://"):
                url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return url

        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB
        ))

    # JWT Authentication
    jwt_secret_key: str = Field(default="change-me-in-production-please")
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_token_expire_minutes: int = Field(default=60 * 24)
    
    # Sentry
    sentry_dsn: str = Field(default="https://5d0ce5e23ec01ee6b34ccaacaf4de121@o4511162184237056.ingest.de.sentry.io/4511162190659664")

settings = Settings()
