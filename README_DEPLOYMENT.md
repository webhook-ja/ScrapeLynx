# 🚀 Guía de Deployment en Easypanel

Esta guía te llevará paso a paso para deployar **Temu Scraper** en Easypanel y transformarlo en un SaaS.

---

## 📋 Pre-requisitos

Antes de empezar, necesitas:

1. ✅ Cuenta en [Easypanel](https://easypanel.io)
2. ✅ Cuenta en [GitHub](https://github.com)
3. ✅ API Key de [OpenAI](https://platform.openai.com/api-keys)
4. ✅ ID de Afiliado de [Temu](https://seller.temu.com)

---

## 🎯 PASO 1: Subir el Código a GitHub

### 1.1 Inicializar Git (si no lo has hecho)

```bash
cd temu_scraper
git init
```

### 1.2 Crear repositorio en GitHub

1. Ve a [GitHub](https://github.com/new)
2. Nombre: `temu-scraper` (o el que prefieras)
3. Privado o Público (tu elección)
4. **NO** agregues README, .gitignore ni licencia (ya los tenemos)
5. Click en **"Create repository"**

### 1.3 Subir el código

```bash
# Agregar todos los archivos
git add .

# Crear primer commit
git commit -m "Initial commit - Temu Scraper for Easypanel"

# Agregar remote (reemplaza TU_USUARIO con tu usuario de GitHub)
git branch -M main
git remote add origin https://github.com/TU_USUARIO/temu-scraper.git

# Push
git push -u origin main
```

✅ **Verificación**: Ve a tu repositorio en GitHub y asegúrate de que todos los archivos estén ahí.

---

## 🗄️ PASO 2: Crear Base de Datos PostgreSQL en Easypanel

### 2.1 Login a Easypanel

1. Ve a tu panel: `https://tu-servidor.easypanel.io`
2. Ingresa tus credenciales

### 2.2 Crear servicio PostgreSQL

1. Click en **"+ Create Service"** o **"New Service"**
2. Selecciona **"Database"** > **"PostgreSQL"**
3. Configuración:
   - **Name**: `temu-postgres`
   - **Database Name**: `temu_db`
   - **Username**: `temu_user`
   - **Password**: Genera una contraseña segura (guárdala)
   - **Version**: PostgreSQL 15 o 16
4. Click en **"Create"** o **"Deploy"**
5. Espera a que el status sea **"Running"** (puede tomar 1-2 minutos)

### 2.3 Obtener la URL de conexión

1. Click en el servicio `temu-postgres`
2. Ve a la sección **"Connection"** o **"Environment"**
3. Copia la **"Connection String"**, se verá así:
   ```
   postgresql://temu_user:tu_password@temu-postgres:5432/temu_db
   ```
4. **GUARDA ESTA URL**, la necesitarás en el Paso 4

✅ **Verificación**: El servicio debe estar en estado "Running" con un ícono verde.

---

## 🔴 PASO 3: Crear Redis (Opcional - Recomendado)

Redis se usará para caché en futuras versiones.

### 3.1 Crear servicio Redis

1. Click en **"+ Create Service"**
2. Selecciona **"Database"** > **"Redis"**
3. Configuración:
   - **Name**: `temu-redis`
   - **Version**: Redis 7
4. Click en **"Create"**
5. Espera a que esté **"Running"**

### 3.2 Obtener URL de Redis

La URL será:
```
redis://temu-redis:6379/0
```

✅ **Verificación**: Redis corriendo con ícono verde.

---

## 🚀 PASO 4: Crear Aplicación (API)

### 4.1 Crear servicio de App

1. Click en **"+ Create Service"**
2. Selecciona **"App"** > **"From GitHub"**
3. Si es la primera vez, conecta tu cuenta de GitHub:
   - Click en **"Connect GitHub"**
   - Autoriza Easypanel
4. Selecciona tu repositorio: `tu-usuario/temu-scraper`
5. Configuración:
   - **Name**: `temu-api`
   - **Branch**: `main`
   - **Build Method**: Selecciona **"Dockerfile"**
   - **Dockerfile Path**: `./Dockerfile` (o déjalo en blanco si Dockerfile está en la raíz)

### 4.2 Configurar Variables de Entorno

En la sección **"Environment Variables"**, agrega estas variables:

```env
# Entorno
ENVIRONMENT=production
DEBUG=false

# Database (pega la URL del Paso 2.3)
DATABASE_TYPE=postgresql
DATABASE_URL=postgresql://temu_user:tu_password@temu-postgres:5432/temu_db

# Redis (si lo creaste en Paso 3)
REDIS_ENABLED=true
REDIS_URL=redis://temu-redis:6379/0

# Temu Affiliate (IMPORTANTE: consigue tu ID en https://seller.temu.com)
TEMU_AFFILIATE_ID=tu_id_de_afiliado_aqui

# OpenAI (IMPORTANTE: consigue tu key en https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-tu-api-key-aqui
LLM_PROVIDER=openai/gpt-4o-mini

# Scraping Config
MAX_CONCURRENT_REQUESTS=3
REQUEST_DELAY_SECONDS=2

# API
PORT=8000
CORS_ORIGINS=*

# Storage
RESULTS_DIR=/app/results
LOGS_DIR=/app/logs
```

### 4.3 Configurar Puerto

1. En la sección **"Ports"** o **"Expose"**
2. Agrega el puerto **8000** (HTTP)

### 4.4 Configurar Dominio

1. Ve a la sección **"Domains"**
2. Opciones:
   - **Subdominio Easypanel** (gratis): `tu-app.easypanel.host`
   - **Dominio custom**: Si tienes uno propio
3. Click en **"Add Domain"**
4. Easypanel configurará HTTPS automáticamente con Let's Encrypt

### 4.5 Deploy

1. Click en **"Deploy"** o **"Create and Deploy"**
2. Ve a **"Logs"** para ver el progreso
3. El primer build tomará **10-15 minutos** (Playwright descarga Chromium)
4. Espera hasta ver:
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

✅ **Verificación**:
- Status: **"Running"** con ícono verde
- Logs muestran "Application startup complete"

---

## ✅ PASO 5: Verificar el Deployment

### 5.1 Health Check

Abre en tu navegador:
```
https://tu-app.easypanel.host/health
```

Deberías ver:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00"
}
```

### 5.2 Documentación de API

```
https://tu-app.easypanel.host/docs
```

Verás la interfaz interactiva de Swagger con todos los endpoints.

### 5.3 Frontend

```
https://tu-app.easypanel.host
```

Deberías ver la interfaz de búsqueda de productos.

### 5.4 Prueba de Scraping

1. En el frontend, ingresa: `wireless earbuds`
2. Ajusta filtros
3. Click en **"Buscar Productos"**
4. Espera 10-20 segundos
5. Deberías ver productos de Temu con links de afiliado

---

## 🔧 PASO 6: Configuración Adicional

### 6.1 Auto-Deploy en cada Push

1. En tu app `temu-api`, ve a **"Settings"** > **"Build"**
2. Activa **"Auto Deploy on Push"**
3. Ahora cada vez que hagas `git push`, se rebuildeará automáticamente

### 6.2 Configurar Límites de Recursos

1. Ve a **"Resources"**
2. Ajusta según tu plan:
   - **CPU**: 1-2 vCPU
   - **Memory**: 1-2 GB (mínimo 1GB por Playwright)
   - **Storage**: 5-10 GB

### 6.3 Configurar Reinicio Automático

1. Ve a **"Advanced"** > **"Restart Policy"**
2. Selecciona **"Always"** o **"Unless Stopped"**

### 6.4 Configurar Backups (Base de Datos)

1. Ve a tu servicio `temu-postgres`
2. En **"Backups"**, configura:
   - Frecuencia: Diaria
   - Retención: 7 días
   - Hora: 3:00 AM (o cuando tengas menos tráfico)

---

## 📊 PASO 7: Monitoreo y Logs

### 7.1 Ver Logs en Tiempo Real

1. Ve a tu app `temu-api`
2. Click en **"Logs"**
3. Verás logs en tiempo real
4. Filtra por:
   - **Level**: INFO, WARNING, ERROR
   - **Time**: Últimas 1h, 24h, 7d

### 7.2 Métricas

1. Ve a **"Metrics"**
2. Verás:
   - CPU usage
   - Memory usage
   - Network I/O
   - Response time

### 7.3 Alertas (Opcional)

1. Ve a **"Alerts"**
2. Configura alertas para:
   - CPU > 80%
   - Memory > 90%
   - App down

---

## 🔐 PASO 8: Seguridad

### 8.1 Cambiar SECRET_KEY

Genera una key segura:
```bash
openssl rand -hex 32
```

Agrégala como variable de entorno:
```
SECRET_KEY=tu-key-generada-aqui
```

### 8.2 Restringir CORS

Cambia `CORS_ORIGINS=*` por tu dominio:
```
CORS_ORIGINS=https://tu-app.easypanel.host,https://tu-dominio-custom.com
```

### 8.3 Variables Sensibles

Asegúrate de que estas NO estén en Git:
- ✅ `OPENAI_API_KEY` → Solo en Easypanel
- ✅ `DATABASE_URL` → Solo en Easypanel
- ✅ `SECRET_KEY` → Solo en Easypanel

---

## 🐛 Troubleshooting

### Problema: Build falla

**Error**: `playwright install failed`

**Solución**:
- Verifica que el Dockerfile tenga las dependencias del sistema
- Aumenta timeout de build en Easypanel

### Problema: App crashea al iniciar

**Error**: `Connection refused (PostgreSQL)`

**Solución**:
- Verifica `DATABASE_URL` en variables de entorno
- Asegúrate de que PostgreSQL esté corriendo
- Verifica que el nombre del servicio sea correcto: `temu-postgres`

### Problema: Scraping falla

**Error**: `Could not find browser`

**Solución**:
- Verifica que el Dockerfile ejecute `playwright install chromium`
- Aumenta memoria a 1GB mínimo

### Problema: OpenAI API error

**Error**: `Invalid API key`

**Solución**:
- Verifica `OPENAI_API_KEY` en variables de entorno
- Asegúrate de tener créditos en tu cuenta de OpenAI

---

## 📈 Próximos Pasos (Roadmap SaaS)

Ahora que tienes la base funcionando en Easypanel, los siguientes pasos son:

### ✅ PASO 1 (COMPLETADO)
- [x] Dockerizar aplicación
- [x] Configurar PostgreSQL
- [x] Deploy en Easypanel

### 🔜 PASO 2: Sistema de Usuarios
- [ ] Autenticación con JWT
- [ ] Registro de usuarios
- [ ] Login/Logout
- [ ] Recuperación de contraseña

### 🔜 PASO 3: Sistema de Pagos
- [ ] Integración con Stripe
- [ ] Planes de suscripción (Basic, Pro, Enterprise)
- [ ] Webhooks de Stripe

### 🔜 PASO 4: Panel de Usuario
- [ ] Dashboard con estadísticas
- [ ] Historial de búsquedas
- [ ] Límites de uso por plan
- [ ] Gestión de suscripción

### 🔜 PASO 5: Sistema de Referidos
- [ ] Códigos de referido únicos
- [ ] Tracking de referidos
- [ ] Recompensas (créditos, descuentos)

### 🔜 PASO 6: Panel de Administrador
- [ ] Dashboard de admin
- [ ] Gestión de usuarios
- [ ] Estadísticas globales
- [ ] Sistema de soporte

---

## 📞 Soporte

Si tienes problemas durante el deployment:

1. Revisa los **Logs** en Easypanel
2. Verifica las **Variables de Entorno**
3. Consulta la [Documentación de Easypanel](https://easypanel.io/docs)
4. Revisa el archivo `easypanel.yml` en este repositorio

---

## 🎉 ¡Felicidades!

Has deployado exitosamente Temu Scraper en Easypanel. Ahora tienes:

✅ API REST funcionando en producción
✅ Base de datos PostgreSQL
✅ Frontend accesible públicamente
✅ HTTPS automático
✅ Auto-deploy en cada push

**¡Listo para el siguiente paso del SaaS!** 🚀

---

**Creado por:** Jorge 🔥
**Versión:** 1.0.0
**Fecha:** Enero 2025
