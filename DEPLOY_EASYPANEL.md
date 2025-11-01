# 🚀 Deploy ScrapeLynx on Easypanel - Complete Guide

This guide will walk you through deploying ScrapeLynx on Easypanel with a single click.

## 📋 Prerequisites

Before starting, you need:

1. ✅ **Easypanel account** - [https://easypanel.io](https://easypanel.io)
2. ✅ **GitHub account** - [https://github.com](https://github.com)
3. ✅ **OpenAI API Key** - [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
4. ✅ **Temu Affiliate ID** - From your Temu seller account

## 🎯 One-Click Installation Steps

### Step 1: Create PostgreSQL Database

1. In Easypanel dashboard, click **"+ New"** → **"Database"** → **"PostgreSQL"**
2. Configure the database:
   ```
   Name: scrapelynx-db
   Database: scrapelynx
   User: scrapelynx
   Password: [use auto-generated password]
   ```
3. Click **"Create"** and wait for it to be ready

### Step 2: Create Application

1. Click **"+ New"** → **"App"** → **"From GitHub"**
2. Connect your GitHub account if prompted
3. Select your ScrapeLynx repository (e.g., `your-username/scrapelynx`)
4. Select branch: **`main`**
5. Build Method: **"Docker Compose"**
6. Compose File: **`docker-compose.easypanel.yml`**

### Step 3: Configure Environment Variables

Click on the **"Environment"** tab and add only these **2 required variables**:

```env
TEMU_AFFILIATE_ID=your_real_affiliate_id_here
OPENAI_API_KEY=sk-your-real-openai-key-here
```

**Optional variables** (with defaults you can change):
```env
LLM_PROVIDER=openai/gpt-4o-mini          # LLM provider and model
ENVIRONMENT=production                   # Environment mode
PORT=8000                               # Port number
CORS_ORIGINS=*                          # Allowed origins
MAX_CONCURRENT_REQUESTS=3               # Max concurrent requests
REQUEST_DELAY_SECONDS=2                 # Delay between requests
```

### Step 4: Deploy

1. Click **"Deploy"** button
2. Wait for 10-15 minutes for the first build
3. Check the "Logs" tab to monitor progress

## 🎉 Post-Deployment

### Access Your Application

- **API**: `https://your-app.easypanel.host/`
- **API Documentation**: `https://your-app.easypanel.host/docs`
- **Health Check**: `https://your-app.easypanel.host/health`

### Verify Installation

1. Check the **"Logs"** tab for successful startup messages:
   ```
   🦁 Starting ScrapeLynx API...
   ✅ PostgreSQL is ready!
   ✅ Database initialized successfully
   ✅ All critical variables configured
   🚀 Starting ScrapeLynx API...
   ```

2. Test the health endpoint: `https://your-app.easypanel.host/health`

## 🔧 Troubleshooting

### Common Issues

1. **"Database not ready" error**
   - Wait longer as PostgreSQL initialization can take time
   - Check that your database service is running

2. **"Invalid API key" error**
   - Verify your OpenAI API key format (starts with `sk-`)
   - Check that the key has sufficient credits
   - Ensure no extra spaces in the variable

3. **"Affiliate ID not configured"**
   - Verify the `TEMU_AFFILIATE_ID` variable is correctly set
   - Ensure there are no spaces in the ID

4. **"Container keeps restarting"**
   - Check the logs for specific error messages
   - Verify all required environment variables are set

### Performance Tips

- **For high-volume usage**: Increase `MAX_CONCURRENT_REQUESTS` but monitor costs
- **For cost optimization**: Use `openai/gpt-4o-mini` instead of `gpt-4o`
- **For speed**: Ensure sufficient container resources allocated

## 🔗 Integration with n8n

To use with n8n workflows:

1. Import `n8n_workflows/temu_scraper_workflow.json` into your n8n instance
2. Set the API URL to: `https://your-app.easypanel.host/webhook/n8n/search`

## 📊 API Endpoints

- `GET /` - Service information
- `GET /health` - Health check
- `POST /api/search` - Search products with filters
- `POST /api/product` - Get single product details
- `POST /api/affiliate` - Generate affiliate link
- `GET /api/results` - List saved results
- `GET /api/results/{filename}` - Get specific result
- `POST /webhook/n8n/search` - n8n integration endpoint

## 🛡️ Security

- Your API keys and affiliate ID are stored securely in environment variables
- Health endpoints are public (no sensitive data exposed)
- For production use, consider adding authentication middleware

## 📈 Scaling

If you need to scale your application:

1. In Easypanel, go to your app settings
2. Increase container resources (CPU/RAM)
3. Adjust `MAX_CONCURRENT_REQUESTS` according to resources
4. Monitor performance in the logs

## 🔄 Updates

To update your application:

1. Push changes to your GitHub repository
2. In Easypanel, go to your app
3. Click "Actions" → "Redeploy"
4. The new version will be built and deployed automatically

## 🎯 Success!

You now have a fully functional ScrapeLynx application running on Easypanel! The system will automatically handle:

- Database initialization
- Health checks
- Auto-restart on failures
- Proper startup order (database first, then application)
- Service health monitoring

Ready to start scraping profitable products on Temu! 🚀