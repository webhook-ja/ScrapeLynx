#!/bin/bash
set -e

echo "🐆 ScrapeLynx - Starting..."

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}🚀 ScrapeLynx Auto-Initialization${NC}"
echo -e "${BLUE}================================================${NC}"

# Función para esperar a PostgreSQL
wait_for_postgres() {
    echo -e "${YELLOW}⏳ Esperando a que PostgreSQL esté listo...${NC}"

    # Extraer componentes de DATABASE_URL
    if [[ $DATABASE_URL =~ postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+) ]]; then
        DB_USER="${BASH_REMATCH[1]}"
        DB_PASS="${BASH_REMATCH[2]}"
        DB_HOST="${BASH_REMATCH[3]}"
        DB_PORT="${BASH_REMATCH[4]}"
        DB_NAME="${BASH_REMATCH[5]}"

        export PGPASSWORD="$DB_PASS"

        until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1; do
            echo -e "${YELLOW}⏳ PostgreSQL no está listo, esperando...${NC}"
            sleep 2
        done

        echo -e "${GREEN}✅ PostgreSQL está listo!${NC}"
    else
        echo -e "${YELLOW}⚠️  No se pudo parsear DATABASE_URL, continuando...${NC}"
    fi
}

# Función para inicializar la base de datos
init_database() {
    echo -e "${BLUE}📊 Inicializando base de datos...${NC}"

    # Ejecutar script de inicialización
    python init_db.py

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Base de datos inicializada correctamente${NC}"
    else
        echo -e "${YELLOW}⚠️  Error al inicializar la base de datos, continuando...${NC}"
    fi
}

# Función para verificar variables de entorno
check_env_vars() {
    echo -e "${BLUE}🔍 Verificando configuración...${NC}"

    local missing_vars=0

    # Variables críticas
    if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "sk-your-api-key-here" ]; then
        echo -e "${YELLOW}⚠️  OPENAI_API_KEY no configurada${NC}"
        missing_vars=1
    fi

    if [ -z "$TEMU_AFFILIATE_ID" ] || [ "$TEMU_AFFILIATE_ID" = "YOUR_AFFILIATE_ID" ]; then
        echo -e "${YELLOW}⚠️  TEMU_AFFILIATE_ID no configurada${NC}"
        missing_vars=1
    fi

    if [ $missing_vars -eq 1 ]; then
        echo -e "${YELLOW}⚠️  Algunas variables no están configuradas, pero continuando...${NC}"
        echo -e "${YELLOW}    Configúralas en el panel de Easypanel${NC}"
    else
        echo -e "${GREEN}✅ Todas las variables críticas configuradas${NC}"
    fi
}

# Función para mostrar información
show_info() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${GREEN}📋 Información del Sistema${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo -e "Environment: ${ENVIRONMENT:-development}"
    echo -e "Database Type: ${DATABASE_TYPE:-sqlite}"
    echo -e "LLM Provider: ${LLM_PROVIDER:-openai/gpt-4o-mini}"
    echo -e "Port: ${PORT:-8000}"
    echo -e "${BLUE}================================================${NC}"
}

# ===== INICIO DEL SCRIPT =====

# Verificar variables de entorno
check_env_vars

# Mostrar información
show_info

# Si es PostgreSQL, esperar y inicializar
if [ "$DATABASE_TYPE" = "postgresql" ]; then
    wait_for_postgres
    init_database
else
    echo -e "${YELLOW}ℹ️  Usando SQLite, saltando espera de PostgreSQL${NC}"
fi

echo -e "${BLUE}================================================${NC}"
echo -e "${GREEN}🚀 Iniciando ScrapeLynx API...${NC}"
echo -e "${BLUE}================================================${NC}"
echo -e "API docs: http://localhost:${PORT:-8000}/docs"
echo -e "Health check: http://localhost:${PORT:-8000}/health"
echo -e "${BLUE}================================================${NC}"

# Iniciar la aplicación
exec uvicorn api:app --host 0.0.0.0 --port "${PORT:-8000}" --log-level info
