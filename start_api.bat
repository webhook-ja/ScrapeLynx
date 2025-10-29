@echo off
echo ========================================
echo   TEMU SCRAPER API - Iniciando...
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

REM Iniciar API
echo Iniciando API en http://localhost:8000
echo Documentacion en http://localhost:8000/docs
echo.
echo Presiona Ctrl+C para detener
echo.

python api.py

pause
