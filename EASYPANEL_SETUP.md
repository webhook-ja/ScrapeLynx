# INSTALACIÓN EASYPANEL

## 1. Crear PostgreSQL
```
+ New → Database → PostgreSQL
Name: scrapelynx-db
Database: scrapelynx
User: scrapelynx
Password: [copia el password generado]
```

## 2. Crear App
```
+ New → App → From GitHub
Repo: webhook-ja/ScrapeLynx
Branch: main
Build: Dockerfile
Port: 8000
```

## 3. Variables de Entorno
```env
DATABASE_URL=postgresql://scrapelynx:[PASSWORD]@scrapelynx-db:5432/scrapelynx
DATABASE_TYPE=postgresql
TEMU_AFFILIATE_ID=tu_id
OPENAI_API_KEY=sk-tu-key
PORT=8000
ENVIRONMENT=production
CORS_ORIGINS=*
```

## 4. Deploy

Listo.
