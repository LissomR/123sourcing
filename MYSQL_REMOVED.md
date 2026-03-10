# ✅ MySQL Eliminado del Sistema

## Fecha: Marzo 6, 2026

Se ha eliminado **completamente MySQL** del sistema para reducir costos durante la fase de pruebas.

---

## 📋 Cambios Realizados

### 1. **Base de Datos Cambiada a SQLite**
- **Antes**: MySQL externo (Railway/servidor)
- **Ahora**: SQLite (archivo local `db.sqlite3`)
- **Costo**: $0 (SQLite no requiere servidor)

### 2. **App de Usuarios Deshabilitada**
- La app `users` fue removida de `INSTALLED_APPS`
- Los endpoints de login/registro ya NO están disponibles:
  - ❌ `/login` - eliminado
  - ❌ `/signup` - eliminado
  
### 3. **Autenticación Simplificada**
- Sistema de autenticación usando **solo API Key**
- Configurado en: [custom_lib/authentication.py](custom_lib/authentication.py)
- Todos los requests requieren header: `X-Api-Key: your-api-key`

### 4. **Archivos Actualizados**

#### [api_channel/settings.py](api_channel/settings.py)
```python
# ANTES:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DJANGO_DATABASE_NAME,
        'USER': DJANGO_DATABASE_USER,
        'PASSWORD': DJANGO_DATABASE_PASSWORD,
        ...
    }
}

# AHORA:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### [requirements.txt](requirements.txt) y [requirements.cpu.txt](requirements.cpu.txt)
- ❌ Eliminado: `mysqlclient==2.2.0`

#### [Dockerfile.railway](Dockerfile.railway)
- ❌ Eliminado: `libmariadb-dev`, `pkg-config`, `default-mysql-client`

#### [entrypoint.sh](entrypoint.sh)
- ❌ Eliminado: Todo el código de espera/setup de MySQL
- ✅ Mensaje: "MySQL REMOVED - Using SQLite instead"

---

## 🚀 APIs Disponibles

### ✅ APIs que SÍ funcionan:

1. **GetDetails** - Extracción de datos de documentos
   - Endpoint: `/GetDetails`
   - Método: POST
   - Auth: X-Api-Key header

2. **AddStamp** - Agregar sellos a la base vectorial
   - Endpoint: `/AddStamp`
   - Método: POST
   - Auth: X-Api-Key header

3. **StampVerification** - Verificación de sellos
   - Endpoint: `/StampVerification`
   - Método: POST
   - Auth: X-Api-Key header

### ❌ APIs que ya NO funcionan:

- Login (usuarios)
- Signup (registro)
- Cualquier endpoint relacionado con usuarios

---

## 💰 Reducción de Costos

### Antes (con MySQL):
- MySQL Service: ~$5-10/mes
- Storage: ~$0.50/mes
- **Total adicional**: ~$5.50-10.50/mes

### Ahora (con SQLite):
- SQLite: $0 (incluido en el servicio)
- Storage: $0.04/mes (muy mínimo)
- **Total adicional**: ~$0.04/mes

### **Ahorro mensual: ~$5-10 USD**

---

## 🔧 Variables de Entorno en Railway

### ❌ Variables que YA NO necesitas:
Puedes **eliminarlas** de tu proyecto en Railway:
- `DJANGO_DATABASE_NAME`
- `DJANGO_DATABASE_USER`
- `DJANGO_DATABASE_PASSWORD`
- `DJANGO_DATABASE_SERVER`
- `DJANGO_DATABASE_PORT`
- `MYSQLHOST`
- `MYSQLUSER`
- `MYSQLPASSWORD`
- `MYSQLDATABASE`
- `MYSQLPORT`

### ✅ Variables que SÍ necesitas mantener:
- `DJANGO_SECRET_KEY` ✅
- `API_KEY` ✅
- `PINECONE_API_KEY` ✅ (para stamp detection)
- `PINECONE_INDEX_NAME` ✅ (para stamp detection)
- `MODELS_PATH` ✅
- `HOST_SERVER_URL` (opcional)
- `MAINTENANCE_MODE` (opcional - ver MAINTENANCE_MODE.md)

---

## 📦 Despliegue en Railway

### Pasos para aplicar los cambios:

1. **Hacer push de los cambios al repositorio**:
```bash
git add .
git commit -m "Remove MySQL - Use SQLite instead"
git push
```

2. **Railway detectará los cambios automáticamente** y redesplegará

3. **Eliminar el servicio MySQL** (opcional pero recomendado):
   - Ve a tu proyecto en Railway
   - Si tienes un servicio MySQL separado
   - Haz clic en él y selecciona "Remove Service"

4. **Limpiar variables de entorno** (recomendado):
   - Ve a Variables en Railway
   - Elimina todas las variables MySQL listadas arriba

---

## ⚠️  Notas Importantes

### SQLite en Railway
- SQLite guarda los datos en un archivo local (`db.sqlite3`)
- **Los datos se perderán si el contenedor se reinicia**
- Esto es PERFECTO para testing/desarrollo
- NO recomendado para producción con datos importantes

### Si Necesitas Persistencia de Datos:
- Railway ofrece **Volúmenes** para persistir archivos
- Cuesta extra pero menos que MySQL
- O puedes regresar a MySQL en producción

### Para Producción Real:
- Considera regresar a MySQL/PostgreSQL
- O usa servicios como PlanetScale (tiene plan gratuito)
- O mantén SQLite con un volumen de Railway

---

## 🧪 Cómo Probar Localmente

```bash
# Activar entorno virtual
source venv/bin/activate

# Crear base de datos SQLite (automático)
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

La base de datos SQLite se creará automáticamente en `db.sqlite3`

---

## 🔄 Si Necesitas Revertir a MySQL

1. Deshacer los cambios en git
2. Reinstalar `mysqlclient` en requirements
3. Reconfigurar `DATABASES` en settings.py
4. Agregar servicio MySQL en Railway
5. Configurar variables de entorno

Pero para testing, SQLite es **mucho más económico**.

---

## 📊 Resumen

| Aspecto | MySQL | SQLite |
|---------|--------|--------|
| **Costo mensual** | ~$5-10 | $0 |
| **Setup** | Complejo | Automático |
| **Velocidad** | Red | Local (más rápido) |
| **Persistencia** | Sí | No (en Railway sin volumen) |
| **Ideal para** | Producción | Testing/Desarrollo |

---

## ✅ Conclusión

Sistema ahora funciona **sin MySQL**, usando SQLite que es:
- ✅ Gratis
- ✅ Más rápido para testing
- ✅ Cero configuración
- ✅ Perfecto para desarrollo

**Costos reducidos significativamente durante fase de pruebas** 🎉
