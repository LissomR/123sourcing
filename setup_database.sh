#!/bin/bash

# Script para configurar la base de datos del proyecto 123sourcing

echo "=========================================="
echo "Setup de Base de Datos - 123sourcing"
echo "=========================================="
echo ""

# Solicitar información de conexión
read -p "Ingresa el nombre de la base de datos (default: sourcing_db): " DB_NAME
DB_NAME=${DB_NAME:-sourcing_db}

read -p "Ingresa el usuario de MySQL (default: root): " DB_USER
DB_USER=${DB_USER:-root}

read -sp "Ingresa la contraseña de MySQL: " DB_PASSWORD
echo ""

read -p "Ingresa el host de MySQL (default: localhost): " DB_HOST
DB_HOST=${DB_HOST:-localhost}

echo ""
echo "Configuración:"
echo "  Base de datos: $DB_NAME"
echo "  Usuario: $DB_USER"
echo "  Host: $DB_HOST"
echo ""

# Verificar conexión a MySQL
echo "Verificando conexión a MySQL..."
if ! mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1;" > /dev/null 2>&1; then
    echo "❌ Error: No se pudo conectar a MySQL. Verifica tus credenciales."
    exit 1
fi
echo "✅ Conexión exitosa"
echo ""

# Crear la base de datos
echo "Creando base de datos '$DB_NAME'..."
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Base de datos creada exitosamente"
else
    echo "❌ Error al crear la base de datos"
    exit 1
fi
echo ""

# Ejecutar el script SQL
echo "Ejecutando script SQL para crear tablas..."
if [ -f "MySql.sql" ]; then
    mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < MySql.sql
    if [ $? -eq 0 ]; then
        echo "✅ Tablas creadas exitosamente"
    else
        echo "❌ Error al crear las tablas"
        exit 1
    fi
else
    echo "⚠️  Archivo MySql.sql no encontrado. Las tablas se crearán con las migraciones de Django."
fi
echo ""

# Crear o actualizar archivo .env
echo "Configurando archivo .env..."
if [ ! -f ".env" ]; then
    echo "Creando nuevo archivo .env..."
    cat > .env << EOF
# Django Configuration
DJANGO_SECRET_KEY='your-secret-key-here-change-this'
DEBUG=True

# Database Configuration
DJANGO_DATABASE_NAME=$DB_NAME
DJANGO_DATABASE_USER=$DB_USER
DJANGO_DATABASE_PASSWORD=$DB_PASSWORD
DJANGO_DATABASE_SERVER=$DB_HOST

# Host Configuration
HOST_SERVER_URL=http://localhost:8000

# Auth Configuration
AUTH_TOKEN_EXPIRE_TIME=86400
JWT_AUTH_SECRET='your-jwt-secret-here-change-this'

# Models Path
MODELS_PATH=trained_models

# Pinecone Configuration (opcional)
PINECONE_API_KEY=
PINECONE_INDEX_NAME=

# Log Configuration
LOG_DELETION_DAY=15
EOF
    echo "✅ Archivo .env creado"
else
    echo "⚠️  El archivo .env ya existe. Actualiza manualmente las siguientes variables:"
    echo "    DJANGO_DATABASE_NAME=$DB_NAME"
    echo "    DJANGO_DATABASE_USER=$DB_USER"
    echo "    DJANGO_DATABASE_PASSWORD=$DB_PASSWORD"
    echo "    DJANGO_DATABASE_SERVER=$DB_HOST"
fi
echo ""

echo "=========================================="
echo "✅ Setup completado exitosamente"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Revisa y actualiza el archivo .env con tus configuraciones"
echo "2. Activa tu entorno virtual: source venv/bin/activate"
echo "3. Instala las dependencias: pip install -r requirements.txt"
echo "4. Ejecuta las migraciones: python manage.py migrate"
echo "5. Crea un superusuario: python manage.py createsuperuser"
echo "6. Inicia el servidor: python manage.py runserver"
echo ""
