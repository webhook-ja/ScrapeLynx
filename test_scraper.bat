@echo off
echo ========================================
echo   TEMU SCRAPER - Prueba de Scraper
echo ========================================
echo.

REM Activar entorno virtual
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Entorno virtual no encontrado
    echo Ejecuta install.bat primero
    pause
    exit /b 1
)

REM Verificar .env
if not exist .env (
    echo ERROR: Archivo .env no encontrado
    echo Ejecuta install.bat primero
    pause
    exit /b 1
)

REM Ejecutar scraper de prueba
echo Ejecutando scraper de prueba...
echo Buscando: wireless earbuds
echo.

python scraper.py

echo.
echo Revisa el archivo: temu_search_results.json
echo.
pause
