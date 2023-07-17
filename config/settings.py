from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_prefix="",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        secrets_dir="",
    )

    # database
    EDGEDB_HOST: str
    EDGEDB_USER: str
    EDGEDB_PASSWORD: str
    EDGEDB_DB: str
    EDGEDB_PORT: int
    EDGEDB_TLS_CA: str
    EDGEDB_DB_TEST: str = "dialaxy_test_db"

    # class Config(ConfigDict):
    #     case_sensitive = True
    #     env_file = ".env"


settings = Settings()
