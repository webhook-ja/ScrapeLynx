# 🐆 ScrapeLynx - ONE-CLICK INSTALL

## ⚡ Instalación Automática en 3 Pasos

### 1. Importar en Easypanel
```
Easypanel → New → App → From GitHub
Repositorio: webhook-ja/ScrapeLynx
Branch: main
Build: Docker Compose
Compose File: docker-compose.easypanel.yml
```

### 2. Configurar 2 Variables
```env
TEMU_AFFILIATE_ID=tu_id_aqui
OPENAI_API_KEY=sk-tu-key-aqui
```

### 3. Deploy
```
Click Deploy → Espera 10-15 min → ¡Listo! 🎉
```

---

## ✅ Verifica que funciona

```
https://tu-app.easypanel.host/health
https://tu-app.easypanel.host/docs
https://tu-app.easypanel.host
```

---

## 🎯 Qué se instala automáticamente

- ✅ PostgreSQL 15 (configurado automáticamente)
- ✅ Redis 7 (caché automático)
- ✅ ScrapeLynx API (FastAPI + Playwright)
- ✅ Frontend (interfaz web)
- ✅ Health checks y auto-restart
- ✅ Migración de base de datos automática

**TODO funciona sin configuración manual** 🚀

---

## 📖 Documentación Completa

Lee: **`INSTALL_EASYPANEL.md`** para más detalles

---

**Made for Easy Deployment** 🐆
