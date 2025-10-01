# backend/app/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):  # type: ignore[misc]
    """Classe di configurazione per l'applicazione usando Pydantic v2."""

    mongo_uri: str = Field(..., alias="MONGODB_URI")
    mongo_db_name: str = Field(..., alias="MONGODB_DB_NAME")
    mongo_bet_collection: str = Field(..., alias="MONGODB_BET_COLLECTION")
    mongo_old_bet_collection: str = Field(..., alias="MONGODB_OLD_BET_COLLECTION")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
