"""
CONFIGURACIÓN PARA PRODUCCIÓN
Configuración centralizada para el deployment en Easypanel
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ================== ENTORNO ==================

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# ================== DATABASE ==================

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///temu_products.db")

# Convertir URL para async
if DATABASE_TYPE == "postgresql":
    if DATABASE_URL.startswith("postgresql://"):
        ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    elif DATABASE_URL.startswith("postgresql+asyncpg://"):
        ASYNC_DATABASE_URL = DATABASE_URL
    else:
        ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DATABASE_URL}"
else:
    ASYNC_DATABASE_URL = "sqlite+aiosqlite:///temu_products.db"

# Pool settings
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))

# ================== REDIS ==================

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
REDIS_ENABLED = os.getenv("REDIS_ENABLED", "false").lower() == "true"

# ================== TEMU / SCRAPING ==================

TEMU_AFFILIATE_ID = os.getenv("TEMU_AFFILIATE_ID", "YOUR_AFFILIATE_ID")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai/gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Scraping limits
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "3"))
REQUEST_DELAY_SECONDS = float(os.getenv("REQUEST_DELAY_SECONDS", "2"))

# ================== API ==================

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", "8000"))

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# ================== LOGGING ==================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ================== SEGURIDAD (para futuro) ==================

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))

# ================== RATE LIMITING (para futuro) ==================

RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW_MINUTES = int(os.getenv("RATE_LIMIT_WINDOW_MINUTES", "15"))

# ================== STORAGE ==================

RESULTS_DIR = os.getenv("RESULTS_DIR", "results")
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

# Crear directorios si no existen
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ================== VALIDACIONES ==================

def validate_config():
    """Valida que la configuración esté completa para producción"""
    errors = []

    if IS_PRODUCTION:
        if TEMU_AFFILIATE_ID == "YOUR_AFFILIATE_ID":
            errors.append("❌ TEMU_AFFILIATE_ID no está configurado")

        if not OPENAI_API_KEY and LLM_PROVIDER.startswith("openai"):
            errors.append("❌ OPENAI_API_KEY no está configurado pero se usa OpenAI")

        if DATABASE_TYPE == "sqlite":
            errors.append("⚠️  SQLite en producción no es recomendado. Usa PostgreSQL")

        if SECRET_KEY == "change-this-secret-key-in-production":
            errors.append("❌ SECRET_KEY debe ser cambiado en producción")

    return errors

# ================== PRINT CONFIG (útil para debugging) ==================

def print_config():
    """Imprime configuración (sin datos sensibles)"""
    print("\n" + "="*60)
    print("🔧 CONFIGURACIÓN DEL SISTEMA")
    print("="*60)
    print(f"Environment: {ENVIRONMENT}")
    print(f"Debug: {DEBUG}")
    print(f"Database: {DATABASE_TYPE}")
    print(f"Redis: {'Enabled' if REDIS_ENABLED else 'Disabled'}")
    print(f"LLM Provider: {LLM_PROVIDER}")
    print(f"API Port: {API_PORT}")
    print(f"CORS Origins: {CORS_ORIGINS}")
    print("="*60 + "\n")

    # Validar configuración
    errors = validate_config()
    if errors:
        print("⚠️  ADVERTENCIAS DE CONFIGURACIÓN:")
        for error in errors:
            print(f"  {error}")
        print()

if __name__ == "__main__":
    print_config()
