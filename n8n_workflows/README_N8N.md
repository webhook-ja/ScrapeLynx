# 🔗 Integración con n8n

Este directorio contiene workflows listos para importar en n8n.

## 📁 Workflows Disponibles

### 1. `temu_scraper_workflow.json`

Workflow completo para scraping automatizado de Temu con:
- ✅ Búsqueda de productos con filtros personalizados
- ✅ Guardado automático en Google Sheets
- ✅ Notificaciones por Telegram
- ✅ Manejo de errores

---

## 🚀 Instalación

### 1. Importar el Workflow

1. Abre n8n: `https://tu-instancia-n8n.com`
2. Click en el botón **+** (crear workflow)
3. Click en **⋮** (menú) > **Import from File**
4. Selecciona `temu_scraper_workflow.json`

### 2. Configurar Credenciales

El workflow usa estas credenciales:

#### Google Sheets (Opcional)
- Click en el nodo **"Save to Google Sheets"**
- Agrega tu cuenta de Google
- Selecciona tu Google Sheet
- **Sheet ID**: Reemplaza `YOUR_GOOGLE_SHEET_ID_HERE`

#### Telegram (Opcional)
- Click en el nodo **"Send Telegram Success"**
- Agrega tu bot de Telegram
- **Bot Token**: Obtén de [@BotFather](https://t.me/BotFather)
- **Chat ID**: Tu ID de chat

### 3. Configurar API URL

En el nodo **"Call Temu Scraper API"**:

```
URL: http://localhost:8000/webhook/n8n/search
```

Si tu API está en otro servidor, cambia la URL:
```
URL: http://tu-servidor:8000/webhook/n8n/search
```

---

## 🎯 Uso

### Búsqueda Manual

1. Click en **"Execute Workflow"**
2. Edita los parámetros en **"Set Search Parameters"**:
   - `search_query`: "wireless earbuds"
   - `max_products`: 20
   - `min_rating`: 4.0
   - `min_reviews`: 100
   - `min_sales`: 0
   - `price_min`: 0
   - `price_max`: 999999

### Búsqueda Programada (Cron)

1. Elimina el nodo **"When clicking 'Test workflow'"**
2. Agrega un nodo **Schedule Trigger**:
   - **Mode**: Every Hour
   - **Hour**: */2 (cada 2 horas)

### Búsqueda con Webhook

1. Elimina el nodo **"When clicking 'Test workflow'"**
2. Agrega un nodo **Webhook**:
   - **Method**: POST
   - **Path**: `temu-search`
   - **Body**: JSON con parámetros

Ejemplo de llamada:
```bash
curl -X POST https://tu-n8n.com/webhook/temu-search \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "smartphone",
    "max_products": 30,
    "min_rating": 4.5
  }'
```

---

## 📊 Estructura de Datos

### Input (Set Search Parameters)

```json
{
  "search_query": "wireless earbuds",
  "max_products": 20,
  "min_rating": 4.0,
  "min_reviews": 100,
  "min_sales": 0,
  "price_min": 0,
  "price_max": 999999
}
```

### Output (Call Temu Scraper API)

```json
{
  "success": true,
  "total_products": 15,
  "search_query": "wireless earbuds",
  "timestamp": "2025-01-15T10:30:00",
  "products": [
    {
      "title": "Auriculares Bluetooth TWS",
      "price": 15.99,
      "original_price": 39.99,
      "discount_percentage": 60,
      "rating": 4.7,
      "reviews_count": 1523,
      "sales_count": 5420,
      "image_url": "https://...",
      "product_url": "https://www.temu.com/...",
      "affiliate_link": "https://www.temu.com/...?_x_ads_channel=affiliate&_x_ads_sub_channel=YOUR_ID"
    }
  ]
}
```

---

## 🔧 Personalización

### Agregar Base de Datos

Reemplaza **"Save to Google Sheets"** con:
- **PostgreSQL** (mejor para datos grandes)
- **MySQL**
- **MongoDB**
- **Airtable**

### Agregar Notificaciones

Además de Telegram, puedes agregar:
- **Slack**
- **Discord**
- **Email**
- **WhatsApp** (con Twilio)

### Agregar Procesamiento de Imágenes

Después de **"Split Products"**, agrega:
- **HTTP Request** para descargar imágenes
- **Cloudinary** para almacenar imágenes
- **Image Processing** para optimizar

---

## 🎨 Workflows Avanzados

### Workflow 1: Comparador de Precios

```
1. Trigger (Schedule): Cada 6 horas
2. Loop sobre lista de productos
3. Scrape precio actual
4. Compara con precio anterior (base de datos)
5. Si bajó > 10%, envía notificación
```

### Workflow 2: Top Productos del Día

```
1. Trigger (Schedule): Diario a las 9 AM
2. Scrape múltiples categorías
3. Filtra top 10 por (rating * reviews * sales)
4. Genera imagen con productos
5. Publica en redes sociales
```

### Workflow 3: Monitoreo de Competencia

```
1. Trigger (Webhook): Al actualizar lista de productos
2. Scrape productos similares
3. Compara precios, ratings, reviews
4. Genera reporte en PDF
5. Envía por email
```

---

## 🐛 Troubleshooting

### Error: "Could not connect to API"

**Problema**: La API no está corriendo o la URL es incorrecta.

**Solución**:
```bash
# Verifica que la API esté corriendo
python api.py

# Verifica la URL en el nodo HTTP Request
http://localhost:8000/webhook/n8n/search
```

### Error: "success: false"

**Problema**: El scraping falló (Temu bloqueó, timeout, etc).

**Solución**:
- Aumenta `delay_before_return_html` en `scraper.py`
- Usa proxies rotativos
- Reduce `max_products`

### Error: "Google Sheets authentication failed"

**Problema**: Credenciales inválidas o permisos insuficientes.

**Solución**:
- Re-autentica tu cuenta de Google
- Verifica que el Sheet ID sea correcto
- Da permisos de escritura al Sheet

---

## 💡 Tips

1. **Rate Limiting**: No scrapes más de 1 vez cada 2 horas para evitar bans
2. **Proxies**: Para scraping intensivo, usa proxies rotativos
3. **Caché**: Guarda resultados en base de datos para reducir requests
4. **Monitoreo**: Agrega un workflow de health check para la API

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs de n8n
2. Revisa los logs de la API (`python api.py`)
3. Verifica que Crawl4AI esté instalado correctamente

---

**Dev: Jorge** 🔥
