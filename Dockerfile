# Dockerfile para Temu Scraper API
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para Playwright y Crawl4AI
RUN apt-get update && apt-get install -y \
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
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegadores de Playwright
RUN playwright install chromium
RUN playwright install-deps chromium

# Copiar código de la aplicación
COPY . .

# Crear directorio para resultados
RUN mkdir -p /app/results

# Exponer puerto
EXPOSE 8000

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1
ENV DATABASE_TYPE=postgresql
ENV PORT=8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando para iniciar la aplicación
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
