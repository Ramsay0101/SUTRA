"""
Sutra Core Configuration Module
Enforces type-safe application settings via Pydantic v2 BaseSettings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # -------------------------------------------------------------------------
    # 1. Application Metadata & Runtime
    # -------------------------------------------------------------------------
    PROJECT_NAME: str = "Sutra"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"  # "development", "testing", "production"
    DEBUG: bool = True

    # -------------------------------------------------------------------------
    # 2. PostgreSQL 16 Transactional Database (Async Engine)
    # -------------------------------------------------------------------------
    # Note: postgresql+asyncpg:// is required for SQLAlchemy 2.0 async engine
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/sutra"

    # -------------------------------------------------------------------------
    # 3. Redis 7 Cache & Rate Limiter
    # -------------------------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"
    CLOUD_LLM_RPM_LIMIT: int = 35  # Architectural rate cap (35 Requests Per Minute)

    # -------------------------------------------------------------------------
    # 4. Security, Cryptography & Authentication
    # -------------------------------------------------------------------------
    SECRET_KEY: str = "sutra-insecure-dev-secret-key-replace-in-production-1234567890"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 Hours for development
    ALGORITHM: str = "HS256"

    # -------------------------------------------------------------------------
    # 5. Epistemic Stores (Neo4j Graph & Qdrant Vector)
    # -------------------------------------------------------------------------
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "sutrapassword"
    QDRANT_URL: str = "http://localhost:6333"

    # -------------------------------------------------------------------------
    # Pydantic v2 Settings Configuration
    # -------------------------------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


# Global singleton instance for use across the application
settings = Settings()
