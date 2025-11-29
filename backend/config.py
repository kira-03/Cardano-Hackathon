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
    
    # AI Configuration (Gemini)
    gemini_api_key: Optional[str] = "AIzaSyCIjJu03NeZqJyS7IMFF68auottIjEExAc"
    use_ai_analysis: bool = True  # Enable/disable AI features
    
    # Environment
    environment: str = "development"

settings = Settings()
