#!/bin/bash

# Script para crear las tablas personalizadas en Railway MySQL

echo "=========================================="
echo "  CREAR TABLAS EN RAILWAY MYSQL"
echo "=========================================="
echo ""

# Verificar que estamos conectados a Railway
if ! railway whoami &> /dev/null; then
    echo "❌ No has iniciado sesión en Railway"
    echo "Ejecuta: railway login"
    exit 1
fi

echo "Obteniendo variables de MySQL..."
echo ""

# Ejecutar el script SQL en Railway
echo "Creando tablas personalizadas (sb_users y sb_users_token)..."
railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT $MYSQLDATABASE < MySql.sql'

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Tablas creadas exitosamente"
    echo ""
    echo "Verificando tablas..."
    railway run bash -c 'mysql -h $MYSQLHOST -u $MYSQLUSER -p$MYSQLPASSWORD -P $MYSQLPORT -e "USE $MYSQLDATABASE; SHOW TABLES;"'
else
    echo ""
    echo "❌ Error al crear las tablas"
    echo ""
    echo "Verifica que:"
    echo "1. MySQL esté agregado a tu proyecto Railway"
    echo "2. Las variables de entorno estén configuradas"
    echo "3. El archivo MySql.sql esté en el directorio actual"
fi

echo ""
echo "=========================================="
