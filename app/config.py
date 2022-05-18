from pydantic import BaseSettings

# For easily validating env varaibles
class Settings(BaseSettings):
    db_pwd: str
    db_username: str
    secret_key: str
    db_hostname: str
    db_port: str
    db_name: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
      env_file = ".env"


settings = Settings()