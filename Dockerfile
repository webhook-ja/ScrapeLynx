# ============================================
# ScrapeLynx - Dockerfile para Easypanel
# One-Click Install Ready
# ============================================

FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    # PostgreSQL client para healthcheck
    postgresql-client \
    # Dependencias de Playwright
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    # Utilidades
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt requirements-production.txt ./

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements-production.txt

# Instalar navegadores de Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiar código de la aplicación
COPY . .

# Hacer ejecutable el entrypoint
RUN chmod +x entrypoint.sh

# Crear directorios necesarios
RUN mkdir -p /app/results /app/logs

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    ENVIRONMENT=production \
    DATABASE_TYPE=postgresql

# Exponer puerto
EXPOSE 8000

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Usar entrypoint para auto-inicialización
ENTRYPOINT ["./entrypoint.sh"]
