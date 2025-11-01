# 🐆 ScrapeLynx - AI-Powered Affiliate Scraping SaaS Platform

**Complete system for scraping Temu products with affiliate link generation, API, and database management.**

## ✨ Features

- 🤖 **AI-Powered Scraping**: Uses Crawl4AI with LLMs for data extraction without CSS selectors
- 🔗 **Affiliate Link Generation**: Automatically creates Temu affiliate links
- 🎨 **Web Interface**: Interactive frontend with filtering capabilities
- 🔄 **REST API**: FastAPI endpoints for integration with n8n
- 💾 **Database Support**: PostgreSQL (production) / SQLite (development)
- 🐳 **Docker Ready**: Production-ready Docker configuration
- 🚀 **Easypanel Deployment**: One-click deployment ready

## 📁 Project Structure

```
scrapelynx/
├── scraper.py              # AI-powered scraping engine
├── api.py                  # FastAPI REST API
├── database.py             # Database management (PostgreSQL/SQLite)
├── config.py               # Centralized configuration
├── requirements.txt        # Python dependencies
├── requirements-production.txt # Production dependencies
├── temu_url_parser.py      # URL parsing and affiliate link generation
│
├── frontend/              # Web interface
│   ├── index.html         # Main dashboard
│   └── app.js             # Frontend logic
│
├── chrome_extension/      # Chrome extension for cookie/API inspection
│   ├── manifest.json      # Extension configuration
│   ├── popup.html         # Extension UI
│   ├── popup.js           # Extension logic
│   ├── content.js         # Content script for page inspection
│   ├── background.js      # Background functionality
│   └── icons/             # Extension icons
│
├── Dockerfile             # Production Docker configuration
├── docker-compose.yml     # Development compose file
├── docker-compose.easypanel.yml # Production compose for Easypanel
│
└── deployment/
    ├── .env.example       # Environment template
    ├── entrypoint.sh      # Container startup script
    └── nginx.conf         # Nginx configuration
```

## 🚀 Quick Start - Local Development

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/scrapelynx.git
cd scrapelynx
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure environment variables
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Required
TEMU_AFFILIATE_ID=your_affiliate_id
OPENAI_API_KEY=sk-your-api-key-here

# Database (defaults to SQLite for development)
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///temu_products.db
```

### 4. Start the application
```bash
python api.py
```

### 5. Access the interface
- API: `http://localhost:8000`
- Documentation: `http://localhost:8000/docs`
- Frontend: Open `frontend/index.html` in your browser

## 🚀 Production Deployment with Easypanel

### Prerequisites
- Easypanel account
- GitHub repository with this code
- Temu Affiliate ID
- OpenAI API Key (or Ollama for local LLM)

### 1. Create PostgreSQL Database in Easypanel
```
+ New → Database → PostgreSQL
Name: scrapelynx-db
Database: scrapelynx
User: scrapelynx
Password: [use auto-generated password]
```

### 2. Create Application in Easypanel
```
+ New → App → From GitHub
Repository: your-username/scrapelynx
Branch: main
Build Method: Docker Compose
Compose File: docker-compose.easypanel.yml
```

### 3. Add Environment Variables
Add only these required variables:
```env
TEMU_AFFILIATE_ID=your_real_affiliate_id
OPENAI_API_KEY=sk-your-real-api-key
```

### 4. Deploy
Click "Deploy" and wait 10-15 minutes for the first build.

## 🐳 Docker Image

ScrapeLynx is available as a Docker image on GitHub Container Registry.

### Using Pre-built Image

Pull and run the latest image directly:

```bash
docker run -d \
  --name scrapelynx \
  -p 8000:8000 \
  -e TEMU_AFFILIATE_ID=your_affiliate_id \
  -e OPENAI_API_KEY=sk-your-api-key \
  -e DATABASE_TYPE=postgresql \
  -e DATABASE_URL=postgresql://user:password@host:5432/dbname \
  ghcr.io/webhook-ja/scrapelynx:latest
```

### Available Image Tags

- `latest` - Latest stable build from main branch
- `${commit-sha}` - Specific commit builds

### Docker Compose Deployment

For complete setup with database and other services:

#### Option 1: Full setup with PostgreSQL and Redis
```bash
# Using optimized compose file
docker-compose -f docker-compose.optimizado.yml up -d

# View logs
docker-compose -f docker-compose.optimizado.yml logs -f app
```

#### Option 2: Simplified setup with SQLite
```bash
# Using simplified compose file
docker-compose -f docker-compose.simplificado.yml up -d

# View logs
docker-compose -f docker-compose.simplificado.yml logs -f app
```

### Building Locally

```bash
# Build the image from source
docker build -t scrapelynx .

# Run with your environment
docker run -d -p 8000:8000 \
  -e TEMU_AFFILIATE_ID=your_affiliate_id \
  -e OPENAI_API_KEY=sk-your-api-key \
  scrapelynx
```

For more Docker information, check the [DOCKER.md](DOCKER.md) file.

## 🚀 Easypanel Deployment (Updated)

We now provide multiple optimized options for Easypanel deployment:

### Recommended: Simultaneous API + PostgreSQL Deployment
1. Create a PostgreSQL database in Easypanel
2. Create an app using `docker-compose.optimizado.yml`
3. Configure only `TEMU_AFFILIATE_ID` and `OPENAI_API_KEY`
4. Complete system (API + PostgreSQL + Redis) deploys automatically

### Fastest: Single Service with Prebuilt Image
1. Create an app using `docker-compose.simplificado.yml`
2. Configure required environment variables
3. Uses prebuilt image for faster deployment

For detailed deployment instructions, check [EASYPANEL_DEPLOY.md](EASYPANEL_DEPLOY.md)

## 🔧 Available APIs

- `GET /` - API info
- `GET /health` - Health check
- `POST /api/search` - Search Temu products
- `POST /api/product` - Scrape individual product
- `POST /api/affiliate` - Generate affiliate link
- `GET /api/results` - List saved results
- `GET /api/results/{filename}` - Get specific result
- `DELETE /api/results/{filename}` - Delete result
- `POST /webhook/n8n/search` - n8n webhook endpoint

## 🌐 Additional Tools

### Chrome Extension: Cookie & API Inspector
A Chrome extension to detect cookies, affiliate IDs, API endpoints, and tracking parameters on websites.

**Features:**
- 🔍 **Cookie Detection**: View all cookies from the current website
- 🏷️ **Affiliate ID Detection**: Identify affiliate tracking parameters, IDs, and URLs  
- 🌐 **API Endpoint Detection**: Discover API endpoints used by the website
- 📊 **Real-time Monitoring**: Continuously scans for new data as you browse

**Installation:**
1. Open Chrome and navigate to `chrome://extensions`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select the `chrome_extension` folder

### URL Parser & Affiliate Link Generator
The `temu_url_parser.py` script can:
- Extract product IDs from Temu URLs
- Clean URLs of existing affiliate parameters
- Generate new affiliate links with your ID
- Identify affiliate parameters in URLs

Example usage:
```
python temu_url_parser.py
```

The script will analyze the provided URL, extract the product ID (for your example: 601100131913227), clean the URL of existing affiliate parameters, and show how to generate a new affiliate link with your own ID.

## 🤖 Using with n8n

1. Import workflow from `n8n_workflows/temu_scraper_workflow.json`
2. Configure API endpoint: `http://your-domain.com/webhook/n8n/search`
3. Set up Google Sheets/Telegram credentials in n8n

## 📊 API Usage Example

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

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TEMU_AFFILIATE_ID` | Your Temu affiliate ID (required) | - |
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `DATABASE_TYPE` | Database type (postgresql/sqlite) | `postgresql` |
| `DATABASE_URL` | Database connection string | `postgresql://...` |
| `LLM_PROVIDER` | LLM provider | `openai/gpt-4o-mini` |
| `MAX_CONCURRENT_REQUESTS` | Max concurrent requests | `3` |
| `REQUEST_DELAY_SECONDS` | Delay between requests | `2` |
| `ENVIRONMENT` | Environment mode | `production` |
| `PORT` | API port | `8000` |

## 🛡️ Security

- All sensitive data is loaded from environment variables
- Input validation on all API endpoints
- Rate limiting (implementable)
- SQL injection prevention with ORM

## 🔒 Production Security Notes

- Change default passwords in production
- Use HTTPS in production
- Implement authentication for sensitive endpoints
- Monitor API usage and costs

## 📈 Scaling

For high-volume usage:
- Add Redis for caching
- Implement proxy rotation
- Add load balancer for multiple instances
- Monitor and optimize scraping delays

## 🤝 Contributing

Feel free to submit issues and pull requests for improvements.

## 📄 License

[MIT License](LICENSE)