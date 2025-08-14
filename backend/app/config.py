"""Application configuration settings with cloud deployment support."""

import os
from pathlib import Path
from typing import List, Optional, Dict, Any

from pydantic import Field, validator
from pydantic_settings import BaseSettings


class CloudSettings(BaseSettings):
    """Cloud deployment configuration."""
    
    # Cloud Provider
    CLOUD_PROVIDER: str = Field(
        default="local",
        description="Cloud provider: aws, gcp, azure, or local"
    )
    
    # AWS Configuration
    AWS_REGION: str = Field(
        default="us-east-1",
        description="AWS region"
    )
    AWS_ACCESS_KEY_ID: Optional[str] = Field(
        default=None,
        description="AWS access key ID"
    )
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(
        default=None,
        description="AWS secret access key"
    )
    AWS_S3_BUCKET: Optional[str] = Field(
        default=None,
        description="AWS S3 bucket name"
    )
    AWS_S3_PREFIX: str = Field(
        default="i2c-chatbot",
        description="S3 prefix for storing data"
    )
    
    # GCP Configuration
    GCP_PROJECT_ID: Optional[str] = Field(
        default=None,
        description="GCP project ID"
    )
    GCP_REGION: str = Field(
        default="us-central1",
        description="GCP region"
    )
    GCP_STORAGE_BUCKET: Optional[str] = Field(
        default=None,
        description="GCP Cloud Storage bucket"
    )
    
    # Azure Configuration
    AZURE_STORAGE_ACCOUNT: Optional[str] = Field(
        default=None,
        description="Azure storage account name"
    )
    AZURE_STORAGE_KEY: Optional[str] = Field(
        default=None,
        description="Azure storage account key"
    )
    AZURE_CONTAINER_NAME: Optional[str] = Field(
        default=None,
        description="Azure blob container name"
    )
    
    # Cloud Database
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Cloud database URL (PostgreSQL/MySQL)"
    )
    
    # Redis Configuration (for caching)
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL"
    )
    
    # CDN Configuration
    CDN_BASE_URL: Optional[str] = Field(
        default=None,
        description="CDN base URL for static assets"
    )


class Settings(BaseSettings):
    """Application settings with validation using environment variables."""
    
    # Server Configuration
    HOST: str = Field(default="127.0.0.1", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=False, description="Debug mode")
    RELOAD: bool = Field(default=False, description="Auto-reload on code changes")
    
    # Environment
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, staging, production"
    )
    
    # API Configuration
    APP_NAME: str = Field(default="I2C AI Chatbot", description="Application name")
    API_V1_PREFIX: str = Field(default="/api/v1", description="API version prefix")
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for encryption"
    )
    API_KEY: Optional[str] = Field(
        default=None,
        description="API key for authentication"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256",
        description="JWT signing algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time"
    )
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        description="Allowed CORS origins"
    )
    
    # Allowed Hosts for deployment
    ALLOWED_HOSTS: List[str] = Field(
        default=["localhost", "127.0.0.1", "0.0.0.0"],
        description="Allowed host headers for deployment"
    )
    
    # Base URLs
    API_BASE_URL: str = Field(
        default="http://localhost:8000/api/v1",
        description="Base API URL"
    )
    FRONTEND_URL: str = Field(
        default="http://localhost:3000",
        description="Frontend URL"
    )
    BASE_URL: str = Field(
        default="https://i2cinc.com",
        description="Base URL for scraping"
    )
    
    # External API URLs
    TOGETHER_API_URL: str = Field(
        default="https://api.together.xyz/v1/chat/completions",
        description="Together AI API endpoint"
    )
    OPENROUTER_API_URL: str = Field(
        default="https://openrouter.ai/api/v1/chat/completions",
        description="OpenRouter API endpoint"
    )
    HUGGINGFACE_API_URL: str = Field(
        default="https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta",
        description="HuggingFace API endpoint"
    )
    
    # Model Configuration
    MODEL_NAME: str = Field(
        default="microsoft/DialoGPT-large",
        description="HuggingFace model name"
    )
    MODEL_MAX_LENGTH: int = Field(
        default=1024,
        description="Maximum model input length"
    )
    TEMPERATURE: float = Field(
        default=0.7,
        description="Model temperature"
    )
    TOP_P: float = Field(
        default=0.9,
        description="Model top-p parameter"
    )
    
    # Vector Store Configuration
    CHROMA_DB_PATH: str = Field(
        default="./chroma_db",
        description="ChromaDB storage path"
    )
    CHROMA_COLLECTION_NAME: str = Field(
        default="i2c_documents",
        description="ChromaDB collection name"
    )
    EMBEDDING_MODEL: str = Field(
        default="BAAI/bge-small-en-v1.5",
        description="Sentence embedding model"
    )
    CHUNK_SIZE: int = Field(
        default=512,
        description="Text chunk size"
    )
    CHUNK_OVERLAP: int = Field(
        default=50,
        description="Text chunk overlap"
    )
    
    # Scraping Configuration
    SCRAPER_BASE_URL: str = Field(
        default="https://www.i2cinc.com",
        description="Base URL for scraping"
    )
    SCRAPE_DELAY: float = Field(
        default=1.0,
        description="Delay between requests"
    )
    MAX_SCRAPE_PAGES: int = Field(
        default=100,
        description="Maximum pages to scrape"
    )
    
    # API Keys
    HF_API_TOKEN: str = Field(
        default="",
        description="HuggingFace API token"
    )
    TOGETHER_API_KEY: str = Field(
        default="",
        description="Together AI API key"
    )
    OPENROUTER_API_KEY: str = Field(
        default="",
        description="OpenRouter API key"
    )
    
    # Application Settings
    USE_CLOUD_API: bool = Field(
        default=True,
        description="Use cloud API instead of local models"
    )
    
    # Logging Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Logging level"
    )
    LOG_FILE: Optional[str] = Field(
        default="logs/app.log",
        description="Log file path"
    )
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string"
    )
    
    # Performance Settings
    WORKERS: int = Field(
        default=1,
        description="Number of worker processes"
    )
    MAX_REQUESTS_PER_WORKER: int = Field(
        default=1000,
        description="Maximum requests per worker before restart"
    )
    TIMEOUT: int = Field(
        default=30,
        description="Request timeout in seconds"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Rate limit per minute per IP"
    )
    
    # Cache Settings
    CACHE_TTL: int = Field(
        default=3600,
        description="Cache TTL in seconds"
    )
    ENABLE_CACHE: bool = Field(
        default=True,
        description="Enable response caching"
    )
    
    # Monitoring
    ENABLE_METRICS: bool = Field(
        default=False,
        description="Enable Prometheus metrics"
    )
    METRICS_PORT: int = Field(
        default=9090,
        description="Prometheus metrics port"
    )
    
    # Cloud Configuration
    cloud: CloudSettings = Field(default_factory=CloudSettings)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v):
        """Validate environment setting."""
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v
    
    @validator("LOG_LEVEL")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in valid_levels:
            raise ValueError(f"Log level must be one of {valid_levels}")
        return v.upper()
    
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"
    
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.ENVIRONMENT == "development"
    
    def get_cloud_storage_config(self) -> Dict[str, Any]:
        """Get cloud storage configuration based on provider."""
        if self.cloud.CLOUD_PROVIDER == "aws":
            return {
                "provider": "aws",
                "region": self.cloud.AWS_REGION,
                "bucket": self.cloud.AWS_S3_BUCKET,
                "prefix": self.cloud.AWS_S3_PREFIX,
            }
        elif self.cloud.CLOUD_PROVIDER == "gcp":
            return {
                "provider": "gcp",
                "project_id": self.cloud.GCP_PROJECT_ID,
                "bucket": self.cloud.GCP_STORAGE_BUCKET,
            }
        elif self.cloud.CLOUD_PROVIDER == "azure":
            return {
                "provider": "azure",
                "account": self.cloud.AZURE_STORAGE_ACCOUNT,
                "container": self.cloud.AZURE_CONTAINER_NAME,
            }
        return {"provider": "local"}
    
    def create_directories(self) -> None:
        """Create necessary directories."""
        directories = [
            self.CHROMA_DB_PATH,
            "logs",
            "data",
            "models",
            "temp",
            "backups"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Create settings instance
settings = Settings()
settings.create_directories()
