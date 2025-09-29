# backend/app/config.py
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Classe di configurazione per l'applicazione usando Pydantic v2."""

    mongodb_uri: str = Field(..., alias="MONGODB_URI")
    mongodb_db_name: str = Field(..., alias="MONGODB_DB_NAME")
    mongodb_bet_collection: str = Field(..., alias="MONGODB_BET_COLLECTION")
    mongodb_old_bet_collection: str = Field(..., alias="MONGODB_OLD_BET_COLLECTION")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
