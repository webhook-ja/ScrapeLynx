#!/bin/bash

echo "========================================"
echo "  TEMU SCRAPER - Instalación Automática"
echo "========================================"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
echo "[1/6] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 no está instalado${NC}"
    echo "Instala Python 3: https://www.python.org/downloads/"
    exit 1
fi
python3 --version
echo ""

# Crear entorno virtual
echo "[2/6] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Entorno virtual ya existe, saltando...${NC}"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}ERROR: No se pudo crear el entorno virtual${NC}"
        exit 1
    fi
    echo -e "${GREEN}Entorno virtual creado${NC}"
fi
echo ""

# Activar entorno virtual
echo "[3/6] Activando entorno virtual..."
source venv/bin/activate
echo ""

# Instalar dependencias
echo "[4/6] Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Error instalando dependencias${NC}"
    exit 1
fi
echo ""

# Instalar navegadores Playwright
echo "[5/6] Instalando navegadores Playwright..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Error instalando navegadores${NC}"
    exit 1
fi
echo ""

# Configurar .env
echo "[6/6] Configurando variables de entorno..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}Archivo .env ya existe, saltando...${NC}"
else
    cp .env.example .env
    echo -e "${GREEN}Archivo .env creado${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANTE: Edita el archivo .env y agrega:${NC}"
    echo "  - TEMU_AFFILIATE_ID (tu ID de afiliado)"
    echo "  - OPENAI_API_KEY (tu API key de OpenAI)"
fi
echo ""

# Inicializar base de datos
echo "[BONUS] Inicializando base de datos..."
python3 database.py
echo ""

echo "========================================"
echo -e "  ${GREEN}INSTALACIÓN COMPLETADA!${NC}"
echo "========================================"
echo ""
echo "Próximos pasos:"
echo "1. Edita .env con tus credenciales:"
echo "   nano .env"
echo ""
echo "2. Inicia la API:"
echo "   ./start_api.sh"
echo ""
echo "3. Prueba el scraper:"
echo "   ./start_scraper.sh"
echo ""
echo "4. Abre el frontend:"
echo "   Abre frontend/index.html en tu navegador"
echo ""
