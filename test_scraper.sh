#!/bin/bash

echo "========================================"
echo "  TEMU SCRAPER - Prueba de Scraper"
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

# Ejecutar scraper de prueba
echo "Ejecutando scraper de prueba..."
echo "Buscando: wireless earbuds"
echo ""

python3 scraper.py

echo ""
echo "Revisa el archivo: temu_search_results.json"
echo ""
