#!/bin/bash
# ScrapeLynx - Health Check Script
# Este script verifica que todos los componentes estén listos para el despliegue

echo "🔍 ScrapeLynx - Health Check Script"
echo "===================================="

# Verificar si Docker está instalado
echo "1. Verificando Docker..."
if ! [ -x "$(command -v docker)" ]; then
  echo "❌ Docker no está instalado o no está en el PATH"
  exit 1
else
  echo "✅ Docker instalado: $(docker --version)"
fi

# Verificar si docker-compose está instalado
echo -e "\n2. Verificando Docker Compose..."
if ! [ -x "$(command -v docker-compose)" ]; then
  echo "⚠️  Docker Compose no está instalado o no está en el PATH"
  echo "   Esto no es crítico si usas docker compose (sin guión)"
else
  echo "✅ Docker Compose instalado: $(docker-compose --version)"
fi

# Verificar si docker compose (sin guion) está disponible
if ! docker compose version >/dev/null 2>&1; then
  echo "⚠️  Docker compose (sin guión) no disponible"
else
  echo "✅ Docker compose (sin guión) disponible: $(docker compose version)"
fi

# Verificar archivos importantes
echo -e "\n3. Verificando archivos importantes..."

required_files=(
  "Dockerfile"
  "docker-compose.yml"
  "docker-compose.easypanel.yml"
  "docker-compose.optimizado.yml"
  "docker-compose.simplificado.yml"
  "api.py"
  "scraper.py"
  "database.py"
  "requirements.txt"
  "requirements-production.txt"
)

missing_files=()
for file in "${required_files[@]}"; do
  if [ ! -f "$file" ]; then
    missing_files+=("$file")
  fi
done

if [ ${#missing_files[@]} -eq 0 ]; then
  echo "✅ Todos los archivos importantes están presentes"
else
  echo "❌ Faltan archivos importantes:"
  printf '%s\n' "${missing_files[@]}"
  exit 1
fi

# Verificar que la imagen de Docker exista o se pueda construir
echo -e "\n4. Verificando la imagen de Docker..."

# Intentar obtener la imagen desde GHCR
if docker pull ghcr.io/webhook-ja/scrapelynx:latest >/dev/null 2>&1; then
  echo "✅ Imagen de Docker disponible en GHCR: ghcr.io/webhook-ja/scrapelynx:latest"
else
  echo "⚠️  Imagen no disponible en GHCR (puede que aún no se haya construido)"
  echo "   La imagen se construirá automáticamente durante el despliegue de Easypanel"
fi

# Verificar si .env existe
echo -e "\n5. Verificando archivo de configuración..."

if [ -f ".env" ]; then
  echo "✅ Archivo .env encontrado"
  
  # Comprobar si las variables principales están configuradas
  if grep -q "TEMU_AFFILIATE_ID=your_affiliate_id" .env || [ -z "$(grep 'TEMU_AFFILIATE_ID=' .env | cut -d'=' -f2)" ]; then
    echo "⚠️  ADVERTENCIA: TEMU_AFFILIATE_ID no está configurado en .env"
  else
    echo "✅ TEMU_AFFILIATE_ID está configurado en .env"
  fi
  
  if grep -q "OPENAI_API_KEY=sk-your-api-key-here" .env || [ -z "$(grep 'OPENAI_API_KEY=' .env | cut -d'=' -f2)" ]; then
    echo "⚠️  ADVERTENCIA: OPENAI_API_KEY no está configurado en .env"
  else
    echo "✅ OPENAI_API_KEY está configurado en .env"
  fi
else
  echo "ℹ️  Archivo .env no encontrado (esto es normal en entornos de despliegue)"
fi

# Verificar archivos de documentación
echo -e "\n6. Verificando archivos de documentación..."

docs_found=()
docs_missing=()
docs_to_check=(
  "README.md"
  "DOCKER.md"
  "EASYPANEL_DEPLOY.md"
  "LICENSE"
)

for doc in "${docs_to_check[@]}"; do
  if [ -f "$doc" ]; then
    docs_found+=("$doc")
  else
    docs_missing+=("$doc")
  fi
done

if [ ${#docs_missing[@]} -eq 0 ]; then
  echo "✅ Todos los archivos de documentación están presentes"
else
  echo "ℹ️  Documentación faltante (opcional para despliegue):"
  printf '  %s\n' "${docs_missing[@]}"
fi

# Resumen
echo -e "\n📊 Resumen del estado:"
echo "✅ Docker: Instalado"
if [ -x "$(command -v docker-compose)" ]; then
  echo "✅ Docker Compose: Instalado"
fi
echo "✅ Archivos principales: Completos"
echo "✅ Imagen Docker: $(if docker pull ghcr.io/webhook-ja/scrapelynx:latest >/dev/null 2>&1; then echo "Disponible"; else echo "No disponible (se construirá en despliegue)"; fi)"

echo -e "\n🎯 Recomendaciones para despliegue en Easypanel:"
echo "1. Para despliegue rápido: Usa docker-compose.simplificado.yml"
echo "2. Para despliegue completo: Usa docker-compose.optimizado.yml"
echo "3. Asegúrate de configurar las variables de entorno:"
echo "   - TEMU_AFFILIATE_ID"
echo "   - OPENAI_API_KEY"
echo "4. El sistema incluye health checks que se verificarán automáticamente"
echo "5. El despliegue puede tardar 5-15 minutos en completarse"

echo -e "\n🎉 ¡Tu entorno está listo para despliegue en Easypanel!"