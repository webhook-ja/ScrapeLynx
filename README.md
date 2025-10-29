# 🛍️ TEMU Scraper - Sistema Completo

Sistema avanzado de scraping de productos de Temu con:
- 🤖 **Scraping anti-bot** con Crawl4AI + IA
- 🔗 **Generación automática** de links de afiliado
- 🎨 **Interfaz web** con filtros interactivos
- 🔄 **API REST** para integración con n8n
- 💾 **Base de datos** SQLite/PostgreSQL

---

## 🔥 Características Completas

✅ **Scraping anti-bot**: Evade protecciones de Temu usando Crawl4AI con stealth mode
✅ **Extracción con IA**: Usa LLMs para extraer datos estructurados sin selectores CSS
✅ **Links de afiliado**: Genera automáticamente tus links de referido
✅ **Filtros avanzados**: Rating, reviews, ventas, precio, categoría
✅ **API REST**: FastAPI con endpoints para búsqueda y gestión
✅ **Frontend web**: Interfaz gráfica con Tailwind CSS
✅ **Integración n8n**: Workflows listos para importar
✅ **Base de datos**: SQLite (desarrollo) o PostgreSQL (producción)
✅ **Scripts de instalación**: Setup automático para Windows/Linux/Mac

---

## 📁 Estructura del Proyecto

```
temu_scraper/
├── scraper.py              # Motor de scraping (Crawl4AI + LLM)
├── api.py                  # API REST (FastAPI)
├── database.py             # Sistema de base de datos
├── requirements.txt        # Dependencias Python
├── .env.example           # Template de configuración
│
├── frontend/              # Interfaz web
│   ├── index.html        # Frontend HTML
│   └── app.js            # JavaScript
│
├── n8n_workflows/        # Workflows de n8n
│   ├── temu_scraper_workflow.json
│   └── README_N8N.md
│
├── results/              # Resultados guardados (JSON)
│
└── Scripts de instalación:
    ├── install.bat       # Windows
    ├── install.sh        # Linux/Mac
    ├── start_api.bat     # Iniciar API (Windows)
    ├── start_api.sh      # Iniciar API (Linux/Mac)
    ├── test_scraper.bat  # Probar scraper (Windows)
    └── test_scraper.sh   # Probar scraper (Linux/Mac)
```

---

## 🚀 Instalación Rápida

### Windows

```bash
# 1. Clonar/descargar el proyecto
cd temu_scraper

# 2. Ejecutar instalador automático
install.bat

# 3. Editar .env con tus credenciales
notepad .env

# 4. Iniciar la API
start_api.bat

# 5. Abrir frontend
start_frontend.bat
```

### Linux/Mac

```bash
# 1. Clonar/descargar el proyecto
cd temu_scraper

# 2. Dar permisos a los scripts
chmod +x *.sh

# 3. Ejecutar instalador automático
./install.sh

# 4. Editar .env con tus credenciales
nano .env

# 5. Iniciar la API
./start_api.sh

# 6. Abrir frontend/index.html en navegador
```

---

## 📦 Instalación Manual

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Instalar navegadores de Playwright

```bash
playwright install chromium
```

### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita `.env` y agrega:
- Tu **ID de afiliado de Temu**
- Tu **API Key de OpenAI** (o usa Ollama local)

### 4. Inicializar base de datos

```bash
python database.py
```

---

## 🚀 Uso

### Búsqueda básica

```python
import asyncio
from scraper import scrape_temu_search

async def main():
    results = await scrape_temu_search(
        search_query="wireless earbuds",
        max_products=20
    )
    print(results)

asyncio.run(main())
```

### Búsqueda con filtros avanzados

```python
results = await scrape_temu_search(
    search_query="smartphone",
    max_products=30,
    min_rating=4.5,        # Mínimo 4.5 estrellas
    min_reviews=500,       # Mínimo 500 reviews
    min_sales=1000,        # Mínimo 1000 ventas
    price_min=50.0,        # Precio mínimo $50
    price_max=300.0        # Precio máximo $300
)
```

### Scrape de producto individual

```python
from scraper import scrape_single_product

result = await scrape_single_product(
    product_url="https://www.temu.com/example-product.html"
)
```

---

## 🧪 Pruebas

Ejecuta el script de prueba:

```bash
python scraper.py
```

Esto buscará "wireless earbuds" con filtros y guardará los resultados en `temu_search_results.json`.

---

## 📊 Estructura de Datos

### Producto

```json
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
  "affiliate_link": "https://www.temu.com/...?_x_ads_channel=affiliate&_x_ads_sub_channel=YOUR_ID",
  "category": "Electronics"
}
```

---

## 🔧 Configuración Avanzada

### Cambiar modelo LLM

En `scraper.py`, modifica:

```python
# Usar GPT-4o (más preciso, más caro)
LLM_PROVIDER = "openai/gpt-4o"

# Usar GPT-4o-mini (más barato, rápido)
LLM_PROVIDER = "openai/gpt-4o-mini"

# Usar Ollama local (GRATIS, pero necesitas correr Ollama)
LLM_PROVIDER = "ollama/llama2"
```

### Ajustar anti-bot protection

En `CrawlerRunConfig`:

```python
config = CrawlerRunConfig(
    magic=True,              # Activa anti-bot automático
    simulate_user=True,      # Simula movimiento de mouse, etc.
    override_navigator=True, # Falsifica propiedades del navegador
    delay_before_return_html=5.0,  # Esperar más tiempo
)
```

---

## 🔗 Integración con n8n

### Importar Workflow

1. Abre n8n
2. Importa `n8n_workflows/temu_scraper_workflow.json`
3. Configura credenciales (Google Sheets, Telegram)
4. Actualiza la URL de la API
5. Lee la documentación completa en `n8n_workflows/README_N8N.md`

### Endpoints de la API

```
POST /api/search          - Búsqueda de productos
POST /api/product         - Scrape producto individual
POST /api/affiliate       - Generar link de afiliado
GET  /api/results         - Listar resultados guardados
GET  /api/results/{file}  - Obtener resultado específico

POST /webhook/n8n/search  - Webhook especial para n8n
```

Documentación completa: `http://localhost:8000/docs`

---

## 💾 Base de Datos

### SQLite (Desarrollo)

Por defecto, usa SQLite local (`temu_products.db`):

```python
# .env
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///temu_products.db
```

### PostgreSQL (Producción)

Para producción, usa PostgreSQL:

```python
# .env
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://user:password@localhost:5432/temu_db
```

### Funciones Disponibles

```python
from database import db

# Guardar productos
await db.save_product(product_data)
await db.save_products_batch([product1, product2])

# Buscar productos
products = await db.search_products(
    query="earbuds",
    min_rating=4.5,
    limit=50
)

# Estadísticas
stats = await db.get_stats()
```

---

## 🎨 Frontend Web

### Usar la Interfaz

1. Inicia la API: `start_api.bat` o `./start_api.sh`
2. Abre `frontend/index.html` en tu navegador
3. Configura filtros de búsqueda
4. Click en "Buscar Productos"
5. Copia links de afiliado con un click

### Características del Frontend

- ✅ Búsqueda en tiempo real
- ✅ Filtros interactivos (rating, reviews, ventas, precio)
- ✅ Vista de productos en grid responsive
- ✅ Estadísticas automáticas
- ✅ Copiar link de afiliado
- ✅ Vista previa de imágenes
- ✅ Indicadores de descuentos

---

## 📊 API Endpoints (Detalle)

### Búsqueda de Productos

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "search_query": "wireless earbuds",
    "max_products": 20,
    "min_rating": 4.0,
    "min_reviews": 100,
    "min_sales": 0,
    "price_min": 0,
    "price_max": 999999
  }'
```

### Producto Individual

```bash
curl -X POST http://localhost:8000/api/product \
  -H "Content-Type: application/json" \
  -d '{
    "product_url": "https://www.temu.com/product-xyz.html"
  }'
```

### Generar Link de Afiliado

```bash
curl -X POST http://localhost:8000/api/affiliate \
  -H "Content-Type: application/json" \
  -d '{
    "product_url": "https://www.temu.com/product-xyz.html",
    "affiliate_id": "YOUR_ID"
  }'
```

---

## ⚠️ Notas Importantes

1. **Rate limiting**: No hagas scraping masivo. Usa delays entre requests (configurado en 2-3 segundos)
2. **Términos de servicio**: Respeta los TOS de Temu
3. **Proxies**: Para scraping intensivo, considera usar proxies rotativos
4. **Costos LLM**: Si usas OpenAI, ten en cuenta los costos por request (~$0.001-0.01 por búsqueda)
5. **Caché**: La base de datos cachea resultados para evitar scraping repetido
6. **Anti-bot**: Crawl4AI incluye stealth mode, pero Temu puede bloquearte si haces muchos requests

---

## 🐛 Troubleshooting

### Error: "Could not find module 'crawl4ai'"

**Solución**: Instala las dependencias
```bash
pip install -r requirements.txt
playwright install chromium
```

### Error: "OPENAI_API_KEY not found"

**Solución**: Configura tu `.env`
```bash
cp .env.example .env
# Edita .env y agrega tu API key
```

### Error: "Connection refused localhost:8000"

**Solución**: Asegúrate de que la API esté corriendo
```bash
python api.py
```

### Scraping muy lento

**Solución**: Reduce el delay en `scraper.py`
```python
config = CrawlerRunConfig(
    delay_before_return_html=2.0  # Cambiar de 3.0 a 2.0
)
```

### Temu bloqueó mi IP

**Solución**:
1. Espera 30 minutos
2. Usa VPN o proxies rotativos
3. Reduce la frecuencia de scraping

---

## 📝 TO-DO / Roadmap

- [x] Scraper con Crawl4AI + LLM
- [x] API REST con FastAPI
- [x] Frontend con filtros interactivos
- [x] Integración n8n
- [x] Sistema de base de datos
- [x] Scripts de instalación
- [ ] Sistema de caché (Redis)
- [ ] Soporte para proxies rotativos
- [ ] Modo batch (scrapear múltiples búsquedas)
- [ ] Dashboard de estadísticas avanzadas
- [ ] Sistema de alertas (precio/stock)
- [ ] Exportar a CSV/Excel
- [ ] Docker Compose para deployment

---

## 🤝 Contribuciones

Creado para automatizar búsqueda de productos en Temu con links de afiliado.

**Dev: Jorge** 🔥
