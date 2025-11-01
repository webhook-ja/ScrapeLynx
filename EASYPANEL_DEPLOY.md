# 🚀 ScrapeLynx - Despliegue en Easypanel

## 📋 Opciones de Despliegue

ScrapeLynx se puede desplegar en Easypanel de varias maneras. Aquí te explicamos las diferentes opciones:

## ✅ Opción 1: Despliegue Simultáneo de API + PostgreSQL (Recomendada)

### Pasos:
1. En Easypanel, crea una base de datos PostgreSQL:
   ```
   + New → Database → PostgreSQL
   Name: scrapelynx-db
   Database: scrapelynx
   User: scrapelynx
   Password: [auto-generado por Easypanel]
   ```

2. Crea una aplicación:
   ```
   + New → App → From GitHub
   Repository: webhook-ja/scrapelynx
   Branch: main
   Build Method: Docker Compose
   Compose File: docker-compose.optimizado.yml
   ```

3. Configura variables de entorno:
   ```env
   TEMU_AFFILIATE_ID=tu_id_de_afiliado
   OPENAI_API_KEY=sk-tu-api-key-de-openai
   ```

4. El sistema se desplegará completamente: API + PostgreSQL + Redis

## ⚡ Opción 2: Despliegue Único con Imagen Preconstruida (Más Rápido)

### Pasos:
1. Crea una aplicación:
   ```
   + New → App → From GitHub
   Repository: webhook-ja/scrapelynx
   Branch: main
   Build Method: Docker Compose
   Compose File: docker-compose.simplificado.yml
   ```

2. Configura variables de entorno:
   ```env
   TEMU_AFFILIATE_ID=tu_id_de_afiliado
   OPENAI_API_KEY=sk-tu-api-key-de-openai
   DATABASE_TYPE=sqlite  # o postgresql si tienes una base de datos externa
   ```

## 🔄 Variables de Entorno Disponibles

### Obligatorias:
- `TEMU_AFFILIATE_ID` - Tu ID de afiliado de Temu
- `OPENAI_API_KEY` - Tu clave API de OpenAI

### Opcionales:
- `DATABASE_TYPE` - Tipo de base de datos (sqlite o postgresql) [default: sqlite]
- `DATABASE_URL` - URL de conexión a la base de datos [default: sqlite:///scrapelynx.db]
- `LLM_PROVIDER` - Proveedor y modelo LLM [default: openai/gpt-4o-mini]
- `PORT` - Puerto de la aplicación [default: 8000]
- `CORS_ORIGINS` - Orígenes permitidos para CORS [default: *]
- `MAX_CONCURRENT_REQUESTS` - Requests concurrentes máximos [default: 3]
- `REQUEST_DELAY_SECONDS` - Retraso entre requests en segundos [default: 2]
- `ENVIRONMENT` - Modo de entorno (development o production) [default: production]
- `REDIS_ENABLED` - Habilitar Redis [default: false]
- `REDIS_URL` - URL de conexión a Redis [default: redis://redis:6379/0]

## 🔧 Solución de Problemas

### Common Issues:

1. **"Database connection failed"**: Verifica que las credenciales de PostgreSQL sean correctas
2. **"Health check failed"**: La aplicación puede tardar hasta 90 segundos en iniciar
3. **"Invalid API key"**: Verifica que tu clave API de OpenAI sea válida y tenga permisos
4. **"Affiliate ID not configured"**: Asegúrate de que `TEMU_AFFILIATE_ID` esté correctamente configurado

### Verificar el estado:
- Endpoint de salud: `http://tu-dominio.com/health`
- Documentación de la API: `http://tu-dominio.com/docs`

## 📊 Despliegue con Docker Compose Personalizado

Si necesitas configurar parámetros específicos, puedes usar este archivo base:

```yaml
version: '3.8'

services:
  app:
    image: ghcr.io/webhook-ja/scrapelynx:latest
    container_name: scrapelynx-api
    restart: always
    ports:
      - "8000:8000"
    environment:
      TEMU_AFFILIATE_ID: ${TEMU_AFFILIATE_ID}
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      DATABASE_TYPE: postgresql
      DATABASE_URL: postgresql://user:pass@host:5432/dbname
      LLM_PROVIDER: openai/gpt-4o-mini
      MAX_CONCURRENT_REQUESTS: 3
      REQUEST_DELAY_SECONDS: 2
    volumes:
      - ./results:/app/results
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 120s
```

## 🚀 Acceso a la aplicación

Después del despliegue exitoso:
- **API**: `https://tu-app.easypanel.host/`
- **Documentación**: `https://tu-app.easypanel.host/docs`
- **Salud**: `https://tu-app.easypanel.host/health`

## 🔄 Actualización

Para actualizar a la última versión:
1. Ve a la aplicación en Easypanel
2. Click en "Actions" → "Redeploy"
3. El sistema usará automáticamente la última versión de la imagen

¡Tu instancia de ScrapeLynx estará lista para usar en pocos minutos!