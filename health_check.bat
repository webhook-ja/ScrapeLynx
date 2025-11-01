@echo off
REM ScrapeLynx - Health Check Script for Windows
REM Este script verifica que todos los componentes estén listos para el despliegue

echo 🔍 ScrapeLynx - Health Check Script for Windows
echo ================================================

REM Verificar si Docker está instalado
echo 1. Verificando Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker no está instalado o no está en el PATH
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('docker --version') do set docker_version=%%i
    echo ✅ Docker instalado: %docker_version%
)

REM Verificar si docker-compose está instalado
echo.
echo 2. Verificando Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker Compose no está instalado o no está en el PATH
    echo    Esto no es crítico si usas docker compose (sin guión)
) else (
    for /f "tokens=*" %%i in ('docker-compose --version') do set compose_version=%%i
    echo ✅ Docker Compose instalado: %compose_version%
)

REM Verificar si docker compose (sin guion) está disponible
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Docker compose (sin guión) no disponible
) else (
    for /f "tokens=*" %%i in ('docker compose version') do set compose_new_version=%%i
    echo ✅ Docker compose (sin guión) disponible: %compose_new_version%
)

REM Verificar archivos importantes
echo.
echo 3. Verificando archivos importantes...

set "missing_files="
set "required_files=Dockerfile docker-compose.yml docker-compose.easypanel.yml docker-compose.optimizado.yml docker-compose.simplificado.yml api.py scraper.py database.py requirements.txt requirements-production.txt"

REM Verificar cada archivo
for %%f in (%required_files%) do (
    if not exist "%%f" (
        set "missing_files=!missing_files! %%f"
    )
)

if "%missing_files%"=="" (
    echo ✅ Todos los archivos importantes están presentes
) else (
    echo ❌ Faltan archivos importantes:!missing_files!
    pause
    exit /b 1
)

REM Verificar si .env existe
echo.
echo 4. Verificando archivo de configuración...

if exist ".env" (
    echo ✅ Archivo .env encontrado
    
    REM Comprobar si las variables principales están configuradas
    findstr /C:"TEMU_AFFILIATE_ID=your_affiliate_id" ".env" >nul 2>&1
    if %errorlevel% == 0 (
        echo ⚠️  ADVERTENCIA: TEMU_AFFILIATE_ID no está configurado en .env
    ) else (
        findstr /C:"TEMU_AFFILIATE_ID=" ".env" >nul 2>&1
        if !errorlevel! == 0 (
            echo ✅ TEMU_AFFILIATE_ID está configurado en .env
        )
    )
    
    findstr /C:"OPENAI_API_KEY=sk-your-api-key-here" ".env" >nul 2>&1
    if %errorlevel% == 0 (
        echo ⚠️  ADVERTENCIA: OPENAI_API_KEY no está configurado en .env
    ) else (
        findstr /C:"OPENAI_API_KEY=" ".env" >nul 2>&1
        if !errorlevel! == 0 (
            echo ✅ OPENAI_API_KEY está configurado en .env
        )
    )
) else (
    echo ℹ️  Archivo .env no encontrado (esto es normal en entornos de despliegue)
)

REM Verificar archivos de documentación
echo.
echo 5. Verificando archivos de documentación...

set "docs_found="
set "docs_missing="
set "docs_to_check=README.md DOCKER.md EASYPANEL_DEPLOY.md LICENSE"

for %%d in (%docs_to_check%) do (
    if exist "%%d" (
        set "docs_found=!docs_found! %%d"
    ) else (
        set "docs_missing=!docs_missing! %%d"
    )
)

if "%docs_missing%"=="" (
    echo ✅ Todos los archivos de documentación están presentes
) else (
    echo ℹ️  Documentación faltante (opcional para despliegue):%docs_missing%
)

REM Resumen
echo.
echo 📊 Resumen del estado:
echo ✅ Docker: Instalado
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 echo ✅ Docker Compose: Instalado
echo ✅ Archivos principales: Completos

echo.
echo 🎯 Recomendaciones para despliegue en Easypanel:
echo 1. Para despliegue rápido: Usa docker-compose.simplificado.yml
echo 2. Para despliegue completo: Usa docker-compose.optimizado.yml
echo 3. Asegúrate de configurar las variables de entorno:
echo    - TEMU_AFFILIATE_ID
echo    - OPENAI_API_KEY
echo 4. El sistema incluye health checks que se verificarán automáticamente
echo 5. El despliegue puede tardar 5-15 minutos en completarse

echo.
echo 🎉 ¡Tu entorno está listo para despliegue en Easypanel!

pause