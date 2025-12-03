# 123sourcing - Document Processing & OCR API

API de extracción de datos y detección de sellos usando PaddleOCR, LayoutLM/Ernie Layout y Pinecone Vector Database.

---

## 📋 Descripción del Proyecto

Este proyecto Django proporciona APIs para:
- **Extracción de datos** de documentos PDF e imágenes (shipmentId, deliveryId)
- **Detección y verificación de sellos** usando embeddings vectoriales
- **Almacenamiento de sellos** en Pinecone Vector Database

**Tecnologías:** Django 4.2, PaddleOCR, Transformers (LayoutLM), Pinecone, MySQL

---

## 🚀 Configuración Local (CPU)

### Requisitos Previos
- Python 3.9+ (recomendado 3.10)
- MySQL 5.7+
- 8GB RAM mínimo (16GB recomendado)
- 20GB de espacio en disco

### Setup Automático

```bash
# 1. Clonar el repositorio
git clone https://github.com/LissomR/123sourcing.git
cd 123sourcing

# 2. Ejecutar script de setup
./setup_local.sh
```

El script automáticamente:
- ✅ Crea entorno virtual
- ✅ Instala dependencias CPU
- ✅ Descarga modelos entrenados
- ✅ Configura base de datos MySQL
- ✅ Crea archivo .env

### Setup Manual

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependencias
pip install -r requirements.cpu.txt

# 3. Configurar variables de entorno
cp .env.example api_channel/.env
# Editar api_channel/.env con tus credenciales

# 4. Descargar modelos
./download_models.sh

# 5. Configurar MySQL
mysql -u root -p
```

```sql
CREATE DATABASE 123sourcing_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER '123sourcing_user'@'localhost' IDENTIFIED BY 'tu_password';
GRANT ALL PRIVILEGES ON 123sourcing_db.* TO '123sourcing_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```bash
# Importar schema
mysql -u 123sourcing_user -p 123sourcing_db < MySql.sql

# 6. Ejecutar migraciones
python manage.py migrate

# 7. Crear superusuario (opcional)
python manage.py createsuperuser

# 8. Iniciar servidor
python manage.py runserver
```

### Variables de Entorno Requeridas

Editar `api_channel/.env`:

```env
# Django
DJANGO_SECRET_KEY='tu-secret-key-aqui'
DJANGO_DATABASE_SERVER=localhost
DJANGO_DATABASE_NAME=123sourcing_db
DJANGO_DATABASE_USER=123sourcing_user
DJANGO_DATABASE_PASSWORD=tu_password
AUTH_TOKEN_EXPIRE_TIME=1440
JWT_AUTH_SECRET=tu-jwt-secret

# Server
HOST_SERVER_URL=http://localhost:8000

# Pinecone (obtener desde https://www.pinecone.io/)
PINECONE_API_KEY=tu-pinecone-api-key
PINECONE_INDEX_NAME=image-stamp-index

# Paths
MODELS_PATH=trained_models
TOKENIZERS_PARALLELISM=false
```

---

## ☁️ Deploy en Railway

### Paso 1: Configurar Pinecone

1. Crear cuenta en [Pinecone](https://www.pinecone.io/)
2. Crear un nuevo índice:
   - Nombre: `image-stamp-index`
   - Dimensiones: 768
   - Metric: cosine
3. Copiar tu API key

### Paso 2: Configurar MySQL en Railway

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login
railway login

# Crear proyecto
railway init
```

En Railway Dashboard:
1. Añadir servicio **MySQL**
2. Copiar las credenciales de conexión

### Paso 3: Deploy del Proyecto

```bash
# Conectar con Railway
railway link

# Configurar variables de entorno
railway variables set DJANGO_SECRET_KEY="tu-secret-key"
railway variables set PINECONE_API_KEY="tu-api-key"
railway variables set PINECONE_INDEX_NAME="image-stamp-index"
railway variables set DJANGO_DATABASE_SERVER="${{MySQL.MYSQL_HOST}}"
railway variables set DJANGO_DATABASE_NAME="${{MySQL.MYSQL_DATABASE}}"
railway variables set DJANGO_DATABASE_USER="${{MySQL.MYSQL_USER}}"
railway variables set DJANGO_DATABASE_PASSWORD="${{MySQL.MYSQL_PASSWORD}}"
railway variables set JWT_AUTH_SECRET="tu-jwt-secret"
railway variables set AUTH_TOKEN_EXPIRE_TIME="1440"
railway variables set MODELS_PATH="trained_models"
railway variables set TOKENIZERS_PARALLELISM="false"

# Deploy
railway up
```

**Nota:** Railway usará `Dockerfile.railway` que está optimizado para CPU.

### Paso 4: Importar Schema de BD

```bash
# Conectar a MySQL de Railway
railway connect MySQL

# En el cliente MySQL
SOURCE MySql.sql;
```

### Alternativa: Deploy desde GitHub

1. Conecta tu repositorio GitHub en Railway Dashboard
2. Configura las variables de entorno en Settings
3. Railway detectará automáticamente el `Dockerfile.railway`
4. Deploy automático en cada push

---

## 📚 API Documentation

### Autenticación

Todas las APIs requieren un Bearer token en el header:

```http
Authorization: Bearer YOUR_TOKEN_HERE
```

### API 1: Add Stamp

Agregar imagen de sello a Pinecone Vector Database.

**Endpoint:** `POST /AddStamp`

**Parámetros:**
- `files` (form-data): Archivo de imagen
- `url` (text): URL de imagen (alternativa a files)
- `companyId` (text, requerido): ID único de la compañía

**Ejemplo:**
```bash
curl -X POST https://tu-app.railway.app/AddStamp \
  -H "Authorization: Bearer TOKEN" \
  -F "companyId=e228f6c6-57f1-33ac-bbf5-2720de811e2c" \
  -F "url=https://example.com/stamp.png"
```

### API 2: Data Extraction

Extraer información de documentos (shipmentId, deliveryId).

**Endpoint:** `POST /GetDetails`

**Parámetros:**
- `files` (form-data): PDF o imagen
- `url` (text): URL del documento (alternativa)
- `bool_stamp_detection` (query): true/false para incluir detección de sellos

**Formatos soportados:**
- Imágenes: .jpeg, .jpg, .png, .gif, .bmp, .webp
- Documentos: .pdf

**Ejemplo:**
```bash
curl -X POST "https://tu-app.railway.app/GetDetails?bool_stamp_detection=true" \
  -H "Authorization: Bearer TOKEN" \
  -F "url=https://example.com/document.pdf"
```

### API 3: Stamp Verification

Verificar presencia de sello en documento.

**Endpoint:** `POST /StampVerification`

**Parámetros:**
- `files` (form-data): Archivo de imagen
- `url` (text): URL de imagen (alternativa)
- `companyId` (text, requerido): ID a verificar

**Ejemplo:**
```bash
curl -X POST https://tu-app.railway.app/StampVerification \
  -H "Authorization: Bearer TOKEN" \
  -F "companyId=e228f6c6-57f1-33ac-bbf5-2720de811e2c" \
  -F "files=@document.png"
```

### Swagger Documentation

Acceder a: `https://tu-app.railway.app/swagger`

---

## 🏗️ Arquitectura del Proyecto

```
123sourcing/
├── api_channel/          # Configuración Django
│   ├── settings.py       # Settings principal
│   ├── urls.py          # URLs del proyecto
│   └── .env             # Variables de entorno
├── custom_lib/          # Librerías personalizadas
│   ├── authentication.py # Sistema de autenticación
│   ├── helper.py        # Funciones auxiliares
│   └── logger.py        # Sistema de logging
├── data_extraction/     # App de extracción de datos
│   ├── paddleocr.py    # Integración PaddleOCR
│   ├── services.py     # Lógica de negocio
│   └── views.py        # APIs endpoints
├── stamp_detection/     # App de detección de sellos
│   ├── pinecone.py     # Integración Pinecone
│   └── services.py     # Lógica de sellos
├── users/              # App de usuarios
├── trained_models/     # Modelos ML (no en git)
├── requirements.txt    # Deps GPU (producción original)
├── requirements.cpu.txt # Deps CPU (local/Railway)
├── Dockerfile          # Docker GPU
├── Dockerfile.railway  # Docker CPU para Railway
├── setup_local.sh      # Script setup automático
└── download_models.sh  # Script descarga modelos
```

---

## 🧪 Testing

```bash
# Ejecutar tests
python manage.py test

# Tests específicos
python manage.py test data_extraction
python manage.py test stamp_detection
```

---

## 📊 Modelos Usados

### 1. LayoutLM (CPU - Local/Railway)
- Modelo: `impira/layoutlm-document-qa`
- Uso: Extracción de datos de documentos
- Optimizado para CPU
- [Documentación](https://huggingface.co/impira/layoutlm-document-qa)

### 2. Ernie Layout (GPU - Producción)
- Modelo: PaddleNLP Ernie Layout
- Uso: Extracción avanzada con GPU
- Requiere GPU 16GB+
- [Documentación](https://github.com/PaddlePaddle/PaddleNLP/tree/develop/model_zoo/ernie-layout)

### 3. PaddleOCR
- Detección y reconocimiento de texto
- Soporta CPU y GPU

---

## 🛠️ Troubleshooting

### Error: MySQL connection failed
```bash
# Verificar que MySQL está corriendo
sudo systemctl status mysql

# Verificar credenciales en .env
cat api_channel/.env | grep DJANGO_DATABASE
```

### Error: Trained models not found
```bash
# Descargar modelos manualmente
./download_models.sh

# O manualmente:
wget https://d2hbdgqvbu3n3g.cloudfront.net/123sourcing/trained_models.zip
unzip trained_models.zip
```

### Error: Pinecone index not found
1. Crear índice en [Pinecone Console](https://app.pinecone.io/)
2. Actualizar `PINECONE_INDEX_NAME` en `.env`

### Railway: Build timeout
- Los modelos son grandes (~2GB)
- Considera usar Railway Pro para más tiempo de build
- O pre-cachear modelos en Docker image

---

## 📝 Notas Importantes

- **CPU vs GPU:** Local y Railway usan CPU (más lento pero más barato)
- **Modelos:** Se descargan automáticamente en primer build (~2GB)
- **Base de datos:** Usar Railway MySQL o servicio externo
- **Pinecone:** Tier gratuito disponible para desarrollo

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear branch (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push al branch (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📄 Licencia

Este proyecto es privado y confidencial.

---

## 📞 Soporte

Para preguntas o soporte, contactar al equipo de desarrollo.
