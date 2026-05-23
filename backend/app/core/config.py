"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "DocMind AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/docmind"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # AI Provider
    OPENAI_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    AI_PROVIDER: str = "openai"  # or "gemini"
    
    # GitHub
    GITHUB_TOKEN: str = ""
    GITHUB_API_URL: str = "https://api.github.com"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    API_KEY_HEADER: str = "X-API-Key"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    
    # ChromaDB
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    CHROMA_COLLECTION_NAME: str = "docmind_embeddings"
    
    # Embeddings
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Documentation
    MAX_FILE_SIZE_MB: int = 10
    MAX_REPOSITORY_SIZE_MB: int = 500
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # LLM Settings
    LLM_MODEL: str = "gpt-4-turbo-preview"
    LLM_TEMPERATURE: float = 0.7
    LLM_MAX_TOKENS: int = 4000
    LLM_STREAMING: bool = True
    
    # Background Jobs
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Monitoring
    SENTRY_DSN: str = ""
    SENTRY_ENVIRONMENT: str = "development"
    
    # Feature Flags
    ENABLE_PR_ANALYSIS: bool = True
    ENABLE_WEBHOOKS: bool = True
    ENABLE_ARCHITECTURE_DIAGRAMS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
