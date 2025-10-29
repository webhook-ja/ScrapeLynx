#!/bin/bash

echo "========================================"
echo "  TEMU SCRAPER API - Iniciando..."
echo "========================================"
echo ""

# Activar entorno virtual
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "ERROR: Entorno virtual no encontrado"
    echo "Ejecuta ./install.sh primero"
    exit 1
fi

# Verificar .env
if [ ! -f ".env" ]; then
    echo "ERROR: Archivo .env no encontrado"
    echo "Ejecuta ./install.sh primero"
    exit 1
fi

# Iniciar API
echo "Iniciando API en http://localhost:8000"
echo "Documentación en http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener"
echo ""

python3 api.py
