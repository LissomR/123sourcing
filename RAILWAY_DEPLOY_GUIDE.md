# 🚀 Guía Completa de Despliegue en Railway

## ✅ Pasos Completados

1. ✅ Railway CLI instalado
2. ✅ Login en Railway (clrlissom@gmail.com)
3. ✅ Proyecto creado: **iaimages**
4. ✅ Código subido a Railway
5. ✅ Build iniciado

## 📋 Siguientes Pasos OBLIGATORIOS

### 1. Accede al Dashboard de Railway

Abre en tu navegador:
```
https://railway.com/project/cf2e44c8-71ee-4b40-bfd0-513dbe50ea16
```

### 2. Agregar Base de Datos MySQL

1. En el proyecto, haz clic en **"+ New"**
2. Selecciona **"Database"**
3. Elige **"Add MySQL"**
4. Espera a que se cree (30 segundos aprox)

### 3. Configurar Variables de Entorno

1. Haz clic en tu servicio principal (el que tiene tu código Django)
2. Ve a la pestaña **"Variables"**
3. Agrega las siguientes variables **una por una**:

#### Variables Básicas (copia y pega):

```
DJANGO_SECRET_KEY
django-insecure-f@c6_4-oqw7#g!62&pqgdo0w657xt@epq*a^$8nt48oaop6nr6

JWT_AUTH_SECRET
fdxqjcqi63843bixvqlibhcwc632

AUTH_TOKEN_EXPIRE_TIME
1440

PINECONE_API_KEY
5f08a0a8-f685-41e4-9d66-f0464852bb26

PINECONE_INDEX_NAME
iaimages

MODELS_PATH
trained_models

TOKENIZERS_PARALLELISM
false

JUPYTER_PLATFORM_DIRS
1
```

#### Variables de Base de Datos (usa las referencias de Railway):

**IMPORTANTE:** Railway creará variables automáticas cuando agregues MySQL. Usa las referencias así:

```
DJANGO_DATABASE_SERVER
${{MYSQL_HOST}}

DJANGO_DATABASE_NAME
${{MYSQL_DATABASE}}

DJANGO_DATABASE_USER
${{MYSQL_USER}}

DJANGO_DATABASE_PASSWORD
${{MYSQL_PASSWORD}}
```

### 4. Exponer el Servicio Públicamente

1. En tu servicio Django, ve a **"Settings"**
2. Encuentra la sección **"Networking"**
3. Haz clic en **"Generate Domain"**
4. Railway te dará una URL como: `https://tu-app.up.railway.app`

### 5. Ejecutar Migraciones de Base de Datos

Una vez que el servicio esté desplegado:

**Opción A - Desde Railway Dashboard:**
1. Ve a tu servicio Django
2. Click en **"Deploy Logs"**
3. Cuando termine el build, ve a **"Connect"** o **"Terminal"**
4. Ejecuta:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

**Opción B - Desde tu terminal local:**
```bash
railway run python manage.py migrate
railway run python manage.py collectstatic --noinput
```

### 6. Crear Superusuario (Opcional)

Para acceder al admin de Django:

```bash
railway run python manage.py createsuperuser
```

O desde el terminal de Railway:
```bash
python manage.py createsuperuser
```

## 🔍 Verificar el Despliegue

### Ver logs en tiempo real:
```bash
railway logs
```

### Ver estado del servicio:
```bash
railway status
```

### Abrir la aplicación:
```bash
railway open
```

O ve a: `https://tu-dominio-generado.up.railway.app/swagger/`

## ⚠️ Notas Importantes

1. **Build Time**: El primer build puede tardar 10-15 minutos porque descarga los modelos ML (~3GB)
2. **Memoria**: Railway free tier tiene 512MB de RAM. Si necesitas más, considera el plan Pro ($5/mes)
3. **Timeout**: El timeout está configurado en 300 segundos para las peticiones
4. **Workers**: Configurado con 2 workers para Gunicorn

## 🐛 Solución de Problemas

### Si el build falla:
```bash
railway logs
```
Revisa los errores y ajusta según necesario.

### Si la app no responde:
1. Verifica que todas las variables estén configuradas
2. Verifica que MySQL esté running
3. Checa los logs: `railway logs`

### Si faltan modelos:
Los modelos se descargan automáticamente desde CloudFront en el Dockerfile.railway

## 📊 Monitoreo

- **Logs**: `railway logs -f`
- **Status**: `railway status`
- **Metrics**: Ve al Dashboard de Railway -> tu servicio -> "Metrics"

## 🎯 URLs Importantes

- **Proyecto**: https://railway.com/project/cf2e44c8-71ee-4b40-bfd0-513dbe50ea16
- **API Swagger**: https://tu-dominio.up.railway.app/swagger/
- **Admin Django**: https://tu-dominio.up.railway.app/admin/

## ✅ Checklist Final

- [ ] MySQL agregado al proyecto
- [ ] Todas las variables de entorno configuradas
- [ ] Dominio público generado
- [ ] Migraciones ejecutadas (`manage.py migrate`)
- [ ] Archivos estáticos recolectados (`collectstatic`)
- [ ] Aplicación responde en /swagger/
- [ ] Endpoints funcionando correctamente

---

**Desarrollado para CPU-only deployment**
**Fecha**: Diciembre 2025
