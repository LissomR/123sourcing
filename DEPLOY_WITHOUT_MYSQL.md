# 🚀 Guía Rápida: Desplegar Sin MySQL en Railway

## ✅ Cambios Completados

- ✅ MySQL eliminado completamente
- ✅ SQLite configurado como base de datos
- ✅ App de usuarios deshabilitada
- ✅ Autenticación solo por API Key
- ✅ Requirements actualizados (sin mysqlclient)
- ✅ Dockerfile optimizado (sin dependencias MySQL)
- ✅ Entrypoint simplificado

---

## 📤 Pasos para Desplegar en Railway

### 1️⃣  Commit y Push
```bash
git add .
git commit -m "Remove MySQL, use SQLite for cost reduction"
git push origin main
```

### 2️⃣  Railway Redesplegará Automáticamente
- Railway detectará los cambios
- Construirá nueva imagen sin MySQL
- Desplegará automáticamente

### 3️⃣  Limpiar Variables de entorno (RECOMENDADO)
Ve a Railway Dashboard → Tu Proyecto → Variables y **elimina**:
- `DJANGO_DATABASE_NAME`
- `DJANGO_DATABASE_USER`
- `DJANGO_DATABASE_PASSWORD`
- `DJANGO_DATABASE_SERVER`
- `DJANGO_DATABASE_PORT`
- `MYSQLHOST`, `MYSQLUSER`, `MYSQLPASSWORD`, etc.

### 4️⃣  Eliminar Servicio MySQL (OPCIONAL)
Si tienes un servicio MySQL separado en Railway:
- Haz clic en el servicio MySQL
- Settings → Danger Zone → Delete Service
- **Ahorro: ~$5-10/mes**

---

## 🧪 Probar Localmente Primero

```bash
# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias actualizadas
pip install -r requirements.txt

# Crear base de datos SQLite (automático)
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

Prueba las APIs en: http://localhost:8000/swagger/

---

## 📋 Variables que SÍ Necesitas en Railway

Asegúrate de tener configuradas:
- ✅ `DJANGO_SECRET_KEY`
- ✅ `API_KEY` (para autenticación)
- ✅ `PINECONE_API_KEY` (para stamps)
- ✅ `PINECONE_INDEX_NAME` (para stamps)
- ✅ `MODELS_PATH` (default: 'trained_models')

**Opcional**:
- `MAINTENANCE_MODE` (true/false) - Ver MAINTENANCE_MODE.md
- `HOST_SERVER_URL`

---

## 🔍 Verificar Deployment

Después del despliegue:

1. Ve a la URL de tu app en Railway
2. Agrega `/swagger/` al final
3. Deberías ver la documentación de las APIs
4. Prueba un endpoint con tu API Key

---

## 💰 Costos Esperados

### Antes:
- Servicio Principal: $9/mes (según screenshot)
- MySQL Service: $5-10/mes
- **Total**: ~$14-19/mes

### Ahora:
- Servicio Principal: $9/mes
- Base de datos: $0 (SQLite incluido)
- **Total**: ~$9/mes

### 📊 **Ahorro: ~$5-10/mes (~40-50%)**

---

## ⚠️  Importante: Persistencia de Datos

SQLite en Railway **NO persiste datos** después de reinicios sin un volumen.

### Para esta fase de pruebas: ✅ Perfecto
- No necesitas guardar datos permanentemente
- Solo estás probando funcionalidad
- Costo: $0

### Para producción: ⚠️  Considera
- Agregar un Volumen Railway ($0.25/GB/mes)
- O volver a MySQL/PostgreSQL
- O usar servicio externo (PlanetScale free tier)

---

## 🆘 En Caso de Problemas

### Error: "no such table"
- Normal en primer despliegue
- SQLite se crea automáticamente
- No afecta funcionalidad (no usas usuarios)

### Error: "mysqlclient"
- Verifica que hiciste push de todos los cambios
- Revisa que requirements.txt no tenga mysqlclient

### Las APIs no responden
- Verifica que `API_KEY` esté configurada en Railway
- Prueba con header: `X-Api-Key: tu-api-key`

---

## 📚 Más Información

- [MYSQL_REMOVED.md](MYSQL_REMOVED.md) - Detalles técnicos completos
- [MAINTENANCE_MODE.md](MAINTENANCE_MODE.md) - Modo mantenimiento para reducir costos
- `./cleanup_mysql_files.sh` - Script para limpiar archivos obsoletos

---

## ✅ Checklist Final

Antes de desplegar:
- [ ] Commit y push realizados
- [ ] Variables MySQL eliminadas de Railway
- [ ] API_KEY configurada en Railway
- [ ] PINECONE credentials configuradas (si usas stamps)
- [ ] Servicio MySQL eliminado de Railway (opcional)

¡Listo para reducir costos! 🎉
