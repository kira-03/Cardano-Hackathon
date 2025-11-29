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
    blockfrost_api_key: str
    blockfrost_network: str = "preprod"
    
    # Database
    database_url: str = "sqlite:///./cardano_navigator.db"
    
    # Masumi Integration (MIP-003 Compliant)
    masumi_registry_url: str = "https://cardano-preprod.blockfrost.io/api/v0"
    masumi_payment_url: str = "http://localhost:8081/api/v1"
    
    # OpenAI (optional - for AI-powered analysis)
    openai_api_key: Optional[str] = None
    use_ai_analysis: bool = True  # Enable/disable AI features
    
    # Environment
    environment: str = "development"

settings = Settings()
