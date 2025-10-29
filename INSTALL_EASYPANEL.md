# 🚀 SCRAPELYNX - INSTALACIÓN AUTOMÁTICA EN EASYPANEL

## ⚡ ONE-CLICK INSTALL

Este proyecto está **100% listo** para deployar en Easypanel con instalación automática.

---

## 📋 REQUISITOS PREVIOS

Solo necesitas 2 cosas:

1. ✅ **API Key de OpenAI** - https://platform.openai.com/api-keys
2. ✅ **ID de Afiliado de Temu** - https://seller.temu.com

---

## 🎯 INSTALACIÓN (3 Pasos - 5 minutos)

### PASO 1: Importar en Easypanel

1. Login a tu panel de Easypanel
2. Click en **"+ New"** o **"+ Create Service"**
3. Selecciona **"App"**
4. Selecciona **"From GitHub"**
5. Conecta GitHub si es primera vez
6. Selecciona el repositorio: **`webhook-ja/ScrapeLynx`**
7. Branch: **`main`**

### PASO 2: Configurar Compose File

En la configuración del proyecto:
- **Build Method**: Selecciona **"Docker Compose"**
- **Compose File**: `docker-compose.easypanel.yml`

### PASO 3: Configurar 2 Variables de Entorno

En **"Environment Variables"**, agrega SOLO estas 2:

```env
TEMU_AFFILIATE_ID=tu_id_aqui
OPENAI_API_KEY=sk-tu-key-aqui
```

**¡ESO ES TODO!** 🎉

### PASO 4: Deploy

1. Click en **"Deploy"**
2. Espera 10-15 minutos (primera vez)
3. Ve a **"Logs"** para ver el progreso

---

## ✅ VERIFICAR QUE FUNCIONA

Una vez deployado:

### Health Check
```
https://tu-app.easypanel.host/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "timestamp": "..."
}
```

### API Docs
```
https://tu-app.easypanel.host/docs
```

### Frontend
```
https://tu-app.easypanel.host
```

---

## 🎨 LO QUE SE INSTALA AUTOMÁTICAMENTE

El docker-compose incluye:

- ✅ **PostgreSQL 15** - Base de datos configurada automáticamente
- ✅ **Redis 7** - Caché configurado automáticamente
- ✅ **ScrapeLynx API** - FastAPI con todas las dependencias
- ✅ **Playwright + Chromium** - Para scraping anti-bot
- ✅ **Health checks** - Monitoreo automático
- ✅ **Auto-restart** - Si falla, se reinicia solo
- ✅ **Volúmenes persistentes** - Datos no se pierden

---

## 🔧 CONFIGURACIÓN AVANZADA (OPCIONAL)

Si quieres personalizar más, puedes agregar estas variables:

```env
# Modelo LLM (por defecto: gpt-4o-mini)
LLM_PROVIDER=openai/gpt-4o-mini

# Puerto (por defecto: 8000)
PORT=8000

# CORS (por defecto: permite todo)
CORS_ORIGINS=*

# Límites de scraping
MAX_CONCURRENT_REQUESTS=3
REQUEST_DELAY_SECONDS=2

# PostgreSQL personalizado (opcional)
POSTGRES_DB=scrapelynx
POSTGRES_USER=scrapelynx
POSTGRES_PASSWORD=tu_password_seguro
```

---

## 🎯 INSTALACIÓN ALTERNATIVA: DESDE GIT DIRECTO

Si Easypanel soporta Git URL directo:

```
Repository URL: https://github.com/webhook-ja/ScrapeLynx.git
Compose File: docker-compose.easypanel.yml
Environment:
  TEMU_AFFILIATE_ID=xxx
  OPENAI_API_KEY=sk-xxx
```

**Deploy** → ¡Listo!

---

## 🐛 TROUBLESHOOTING

### Build falla por timeout

**Solución:** Aumenta el timeout de build a 20 minutos (Playwright tarda en descargar Chromium)

### No puede conectar a PostgreSQL

**Solución:** Espera 30 segundos más, el entrypoint espera automáticamente a que PostgreSQL esté listo

### Error "Invalid API Key"

**Solución:** Verifica que `OPENAI_API_KEY` esté correctamente configurada y tenga créditos

### Frontend no carga

**Solución:** Verifica que el puerto 8000 esté expuesto en Easypanel

---

## 📊 LOGS Y MONITOREO

El sistema auto-configura:

- ✅ Health checks cada 30 segundos
- ✅ Logs en tiempo real en Easypanel
- ✅ Reinicio automático si falla
- ✅ Métricas de CPU/RAM

Para ver los logs:
```bash
# En Easypanel UI
Tu app → Logs → Ver en tiempo real
```

---

## 🔄 ACTUALIZAR A NUEVA VERSIÓN

Cuando haya updates en GitHub:

1. En Easypanel: Tu app → **"Redeploy"**
2. Espera el nuevo build
3. ¡Listo!

O si configuraste auto-deploy:
```bash
git pull
# Automáticamente se redeploy
```

---

## 💡 VARIABLES AUTO-GENERADAS

Easypanel auto-genera estas variables:

- `POSTGRES_URL` - URL completa de PostgreSQL
- `REDIS_URL` - URL completa de Redis

El entrypoint las detecta y configura automáticamente.

---

## 🎉 ¡ESO ES TODO!

Con esta configuración:
- ✅ No necesitas crear servicios manualmente
- ✅ No necesitas configurar base de datos
- ✅ No necesitas ejecutar migraciones
- ✅ No necesitas instalar dependencias
- ✅ Todo se hace **automáticamente**

**Solo configura 2 variables y deploy** 🚀

---

## 📞 SOPORTE

Si algo falla:
1. Revisa los logs en Easypanel
2. Verifica que las 2 variables estén configuradas
3. Espera a que termine el build completo (10-15 min primera vez)

---

## 🔐 REPOSITORIO PRIVADO

Si tu repo es privado:
1. Easypanel te pedirá permisos de GitHub
2. Autoriza el acceso
3. Listo, funciona igual

---

**Made with ❤️ for Easy Deployment** 🐆

---

## 🎯 PRÓXIMOS PASOS

Una vez instalado:
1. Prueba hacer búsquedas
2. Verifica que los links de afiliado se generen
3. Revisa los logs por 24h
4. ¡Empieza a promocionar tus productos!

**¡ScrapeLynx listo para cazar!** 🐆💰
