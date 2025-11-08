from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # AWS Configuration
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region: str = "us-east-1"
    aws_bedrock_model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # NBA Stats API Configuration
    nba_stats_base_url: str = "https://stats.nba.com/stats"
    
    # Database Configuration (if needed later)
    database_url: Optional[str] = None
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False
    
    # External API keys (if using premium sports data)
    rapidapi_key: Optional[str] = None
    sportsdata_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()