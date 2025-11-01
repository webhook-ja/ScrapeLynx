# 🐳 ScrapeLynx - Docker Image

Official Docker image for ScrapeLynx - AI-Powered Affiliate Scraping Platform.

## 📦 Image Information

- **Registry**: GitHub Container Registry (GHCR)
- **Image**: `ghcr.io/webhook-ja/scrapelynx`
- **Tags**: `latest`, commit-sha

## 🚀 Quick Start

### Run with Docker
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

### Run with Docker Compose
```yaml
version: '3.8'
services:
  app:
    image: ghcr.io/webhook-ja/scrapelynx:latest
    container_name: scrapelynx
    ports:
      - "8000:8000"
    environment:
      - TEMU_AFFILIATE_ID=your_affiliate_id
      - OPENAI_API_KEY=sk-your-api-key
      - DATABASE_TYPE=postgresql
      - DATABASE_URL=postgresql://user:password@host:5432/dbname
    volumes:
      - ./results:/app/results
      - ./logs:/app/logs
```

## ⚙️ Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `TEMU_AFFILIATE_ID` | ✅ | Your Temu affiliate ID | - |
| `OPENAI_API_KEY` | ✅ | OpenAI API key | - |
| `DATABASE_TYPE` | ❌ | Database type (postgresql/sqlite) | `postgresql` |
| `DATABASE_URL` | ❌ | Database connection string | `postgresql://...` |
| `LLM_PROVIDER` | ❌ | LLM provider | `openai/gpt-4o-mini` |
| `MAX_CONCURRENT_REQUESTS` | ❌ | Max concurrent requests | `3` |
| `REQUEST_DELAY_SECONDS` | ❌ | Delay between requests | `2` |
| `ENVIRONMENT` | ❌ | Environment mode | `production` |
| `PORT` | ❌ | API port | `8000` |
| `REDIS_URL` | ❌ | Redis connection URL | `redis://localhost:6379/0` |
| `REDIS_ENABLED` | ❌ | Enable Redis caching | `false` |

## 🚢 Building the Image Locally

```bash
# Build the image
docker build -t scrapelynx .

# Tag the image
docker tag scrapelynx ghcr.io/webhook-ja/scrapelynx:latest

# Run the built image
docker run -d -p 8000:8000 \
  -e TEMU_AFFILIATE_ID=your_affiliate_id \
  -e OPENAI_API_KEY=sk-your-api-key \
  scrapelynx
```

## 📊 Available Endpoints

- `GET /` - Service info
- `GET /health` - Health check
- `POST /api/search` - Search products
- `POST /api/product` - Get single product
- `POST /api/affiliate` - Generate affiliate link
- `GET /api/results` - List saved results
- `POST /webhook/n8n/search` - n8n webhook endpoint
- `GET /docs` - API Documentation

## 🛡️ Security

- All credentials passed via environment variables
- Built with production security practices
- Health check endpoint for monitoring

## 🔄 Auto-Build

The Docker image is automatically built and published to GHCR when:
- Changes are pushed to the `main` branch
- Manual workflow dispatch via GitHub Actions

This ensures you always have access to the latest stable version.

## 🌐 Accessing the Image

The image is publicly available at:
- `ghcr.io/webhook-ja/scrapelynx:latest`

You can pull it using:
```bash
docker pull ghcr.io/webhook-ja/scrapelynx:latest
```