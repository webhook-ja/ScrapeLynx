@echo off
echo ========================================
echo   TEMU SCRAPER - Abriendo Frontend
echo ========================================
echo.

REM Verificar que frontend existe
if not exist frontend\index.html (
    echo ERROR: Frontend no encontrado
    pause
    exit /b 1
)

REM Abrir en navegador
echo Abriendo frontend en navegador...
start frontend\index.html

echo.
echo Frontend abierto!
echo IMPORTANTE: Asegurate de que la API este corriendo (start_api.bat)
echo.
pause
