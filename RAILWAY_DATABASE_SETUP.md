# 🚀 Guía para Configurar Base de Datos en Railway

## 📋 Pasos para Configurar MySQL en Railway

### 1️⃣ Agregar MySQL a tu Proyecto Railway

1. Ve al dashboard de Railway: https://railway.app/dashboard
2. Abre tu proyecto: **iaimages**
3. Haz clic en el botón **"+ New"**
4. Selecciona **"Database"**
5. Elige **"Add MySQL"**
6. Espera 30-60 segundos a que se cree

### 2️⃣ Configurar Variables de Entorno

1. Haz clic en tu **servicio Django** (el que tiene tu código)
2. Ve a la pestaña **"Variables"**
3. Agrega estas variables haciendo referencia a MySQL:

```
DJANGO_DATABASE_SERVER
${{MySQL.MYSQLHOST}}

DJANGO_DATABASE_NAME
${{MySQL.MYSQLDATABASE}}

DJANGO_DATABASE_USER
${{MySQL.MYSQLUSER}}

DJANGO_DATABASE_PASSWORD
${{MySQL.MYSQLPASSWORD}}
```

**Nota:** Railway reemplazará automáticamente estas referencias con los valores de tu base de datos MySQL.

### 3️⃣ Otras Variables de Entorno Necesarias

Agrega también estas variables en tu servicio Django:

```
DJANGO_SECRET_KEY
django-insecure-f@c6_4-oqw7#g!62&pqgdo0w657xt@epq*a^$8nt48oaop6nr6

JWT_AUTH_SECRET
fdxqjcqi63843bixvqlibhcwc632

AUTH_TOKEN_EXPIRE_TIME
1440

HOST_SERVER_URL
https://tu-app.up.railway.app

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

### 4️⃣ Crear las Tablas en Railway

**Opción A - Usando los scripts automáticos (Recomendado):**

```bash
# 1. Ejecuta el script de setup
./setup_railway_db.sh

# 2. Si ya agregaste MySQL, ejecuta:
./create_railway_tables.sh
```

**Opción B - Manual desde tu terminal:**

```bash
# 1. Asegúrate de tener Railway CLI instalado
npm i -g @railway/cli

# 2. Login en Railway
railway login

# 3. Enlaza tu proyecto
railway link

# 4. Ejecuta las migraciones de Django
railway run python manage.py migrate

# 5. Crea las tablas personalizadas
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT $MYSQLDATABASE < MySql.sql'

# 6. Verifica las tablas
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT -e "USE $MYSQLDATABASE; SHOW TABLES;"'
```

**Opción C - Desde el Dashboard de Railway:**

1. Ve a tu servicio Django en Railway
2. Haz clic en **"Connect"** o busca la opción de **"Shell"**
3. Ejecuta:
```bash
python manage.py migrate
mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT $MYSQLDATABASE < MySql.sql
```

### 5️⃣ Verificar la Base de Datos

Desde tu terminal local:

```bash
# Ver todas las tablas
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT -e "USE $MYSQLDATABASE; SHOW TABLES;"'

# Ver estructura de sb_users
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT -e "USE $MYSQLDATABASE; DESCRIBE sb_users;"'

# Ver estructura de sb_users_token
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT -e "USE $MYSQLDATABASE; DESCRIBE sb_users_token;"'
```

### 6️⃣ Re-desplegar tu Aplicación

1. Ve a tu servicio Django en Railway
2. Haz clic en **"Deploy"** o espera el auto-deploy
3. Verifica los logs para asegurarte que no hay errores de conexión a la base de datos

## 🔧 Solución de Problemas

### Error: "No module named 'MySQLdb'"
- Asegúrate que `mysqlclient` está en tu `requirements.txt` o `requirements.cpu.txt`
- Railway debería instalarlo automáticamente

### Error: "Can't connect to MySQL server"
- Verifica que las variables de entorno estén correctamente configuradas
- Asegúrate de estar usando las referencias `${{MySQL.MYSQLHOST}}` etc.
- Revisa que MySQL esté corriendo en Railway

### Error: "Access denied for user"
- Verifica que las credenciales de MySQL sean correctas
- Revisa las variables en Railway Dashboard

### Las tablas no se crean
- Verifica que el archivo `MySql.sql` esté en el repositorio
- Asegúrate que tiene los punto y coma (;) al final de cada sentencia CREATE TABLE
- Ejecuta manualmente el script SQL usando railway run

## 📝 Notas Importantes

1. **No uses contraseñas en texto plano en tu repositorio**
   - Railway maneja las credenciales de MySQL de forma segura
   - Usa siempre las referencias `${{MySQL.VARIABLE}}`

2. **Actualiza HOST_SERVER_URL**
   - Después de generar el dominio en Railway, actualiza esta variable con tu URL real

3. **Backups**
   - Railway hace backups automáticos de tu base de datos
   - Puedes configurar backups adicionales desde el dashboard

4. **Conexión desde DBeaver**
   - Puedes conectarte usando las credenciales de Railway
   - Encuentra los datos en: Railway Dashboard → MySQL → Connect

## 🎯 Checklist Final

- [ ] MySQL agregado al proyecto Railway
- [ ] Variables de entorno configuradas en el servicio Django
- [ ] Migraciones ejecutadas (`python manage.py migrate`)
- [ ] Tablas personalizadas creadas (MySql.sql)
- [ ] Servicio re-desplegado exitosamente
- [ ] Aplicación funcionando correctamente

## 🔗 Enlaces Útiles

- Railway Dashboard: https://railway.app/dashboard
- Documentación Railway: https://docs.railway.app/
- Railway CLI: https://docs.railway.app/develop/cli
