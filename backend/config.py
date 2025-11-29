"""
Configuration for Cross-Chain Navigator Agent
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Cardano
    blockfrost_api_key: str = "mainnetkxDq3x6Tn5SaDE7VVn1OgNdovwqrCZ70"
    blockfrost_network: str = "mainnet"
    
    # Database
    database_url: str = "sqlite:///./cardano_navigator.db"
    
    # Masumi Integration (MIP-003 Compliant)
    masumi_registry_url: str = "https://cardano-mainnet.blockfrost.io/api/v0"
    masumi_payment_url: str = "http://localhost:8081/api/v1"
    
    # AI Configuration (OpenAI)
    openai_api_key: Optional[str] = None
    use_ai_analysis: bool = True  # Enable/disable AI features
    
    # Email Configuration (SMTP)
    smtp_host: Optional[str] = None  # e.g., "smtp.gmail.com" or "smtp-mail.outlook.com"
    smtp_port: int = 587  # Default for TLS (Gmail/Outlook)
    smtp_user: Optional[str] = None  # Your email address
    smtp_password: Optional[str] = None  # App password for Gmail/Outlook
    sender_email: Optional[str] = None  # From email address
    sender_name: str = "EcosystemBridge Assistant"  # From name
    reply_to_email: Optional[str] = None  # Reply-to address (optional)
    
    # Environment
    environment: str = "development"

settings = Settings()
