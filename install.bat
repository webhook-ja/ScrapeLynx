@echo off
echo ========================================
echo   TEMU SCRAPER - Instalacion Automatica
echo ========================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Crear entorno virtual
echo [2/6] Creando entorno virtual...
if exist venv (
    echo Entorno virtual ya existe, saltando...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: No se pudo crear el entorno virtual
        pause
        exit /b 1
    )
    echo Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo.

REM Instalar dependencias
echo [4/6] Instalando dependencias Python...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Error instalando dependencias
    pause
    exit /b 1
)
echo.

REM Instalar navegadores Playwright
echo [5/6] Instalando navegadores Playwright...
playwright install chromium
if errorlevel 1 (
    echo ERROR: Error instalando navegadores
    pause
    exit /b 1
)
echo.

REM Configurar .env
echo [6/6] Configurando variables de entorno...
if exist .env (
    echo Archivo .env ya existe, saltando...
) else (
    copy .env.example .env
    echo Archivo .env creado
    echo.
    echo IMPORTANTE: Edita el archivo .env y agrega:
    echo   - TEMU_AFFILIATE_ID (tu ID de afiliado)
    echo   - OPENAI_API_KEY (tu API key de OpenAI)
)
echo.

REM Inicializar base de datos
echo [BONUS] Inicializando base de datos...
python database.py
echo.

echo ========================================
echo   INSTALACION COMPLETADA!
echo ========================================
echo.
echo Proximos pasos:
echo 1. Edita .env con tus credenciales
echo 2. Ejecuta: start_api.bat (para iniciar la API)
echo 3. Ejecuta: start_frontend.bat (para abrir el frontend)
echo 4. O ejecuta: test_scraper.bat (para probar el scraper)
echo.
pause
