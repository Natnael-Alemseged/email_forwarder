from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Email Forwarder"
    DB_URI: str = "sqlite:///./email_forwarder.db"
    GMAIL_USER: str
    GMAIL_PASSWORD: str
    IMAP_SERVER: str = "imap.gmail.com"
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
