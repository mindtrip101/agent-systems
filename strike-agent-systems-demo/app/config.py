from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    jwt_secret: str = "dev-secret-change-me"
    jwt_issuer: str = "local-demo"
    jwt_audience: str = "tool-gateway"
    audit_log_path: str = "audit.log.jsonl"
    approval_db_path: str = "approvals.db.json"

settings = Settings()
