#!/bin/bash

echo "=========================================="
echo "  SETUP BASE DE DATOS EN RAILWAY"
echo "=========================================="
echo ""

# Verificar si railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI no está instalado"
    echo ""
    echo "Instalando Railway CLI..."
    npm i -g @railway/cli
    if [ $? -ne 0 ]; then
        echo "❌ Error al instalar Railway CLI"
        exit 1
    fi
fi

echo "✅ Railway CLI instalado"
echo ""

# Verificar login
echo "Verificando sesión de Railway..."
if ! railway whoami &> /dev/null; then
    echo "⚠️  No has iniciado sesión en Railway"
    echo "Ejecuta: railway login"
    exit 1
fi

echo "✅ Sesión activa en Railway"
echo ""

# Enlazar al proyecto
echo "Enlazando al proyecto Railway..."
railway link

echo ""
echo "=========================================="
echo "  PASOS PARA CONFIGURAR LA BASE DE DATOS"
echo "=========================================="
echo ""
echo "1. Agregar MySQL al proyecto:"
echo "   - Ve a: https://railway.app/dashboard"
echo "   - Abre tu proyecto: iaimages"
echo "   - Haz clic en '+ New'"
echo "   - Selecciona 'Database' -> 'Add MySQL'"
echo ""
echo "2. Espera a que MySQL se cree (30-60 segundos)"
echo ""
echo "3. Conecta MySQL a tu servicio Django:"
echo "   - Haz clic en tu servicio Django"
echo "   - Ve a 'Variables'"
echo "   - Agrega estas variables con referencias:"
echo ""
echo "   DJANGO_DATABASE_SERVER: \${{MySQL.MYSQLHOST}}"
echo "   DJANGO_DATABASE_NAME: \${{MySQL.MYSQLDATABASE}}"
echo "   DJANGO_DATABASE_USER: \${{MySQL.MYSQLUSER}}"
echo "   DJANGO_DATABASE_PASSWORD: \${{MySQL.MYSQLPASSWORD}}"
echo ""
echo "4. Una vez configurado, ejecuta:"
echo ""
echo "   railway run python manage.py migrate"
echo ""
echo "   O desde el dashboard de Railway:"
echo "   - Ve a tu servicio -> Deploy Logs"
echo "   - Click en 'Deploy' para re-desplegar"
echo ""
echo "=========================================="
echo ""

read -p "¿Ya agregaste MySQL a tu proyecto Railway? (s/n): " mysql_added

if [ "$mysql_added" = "s" ] || [ "$mysql_added" = "S" ]; then
    echo ""
    echo "Ejecutando migraciones..."
    railway run python manage.py migrate
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Migraciones ejecutadas exitosamente"
        echo ""
        echo "Ahora ejecuta el script SQL para crear las tablas personalizadas:"
        echo ""
        echo "railway run bash -c 'mysql -h \$MYSQLHOST -u \$MYSQLUSER -p\$MYSQLPASSWORD -P \$MYSQLPORT \$MYSQLDATABASE < MySql.sql'"
    else
        echo "❌ Error al ejecutar migraciones"
        echo "Verifica que las variables de entorno estén configuradas correctamente"
    fi
else
    echo ""
    echo "⚠️  Primero agrega MySQL a tu proyecto Railway siguiendo los pasos de arriba"
fi

echo ""
echo "=========================================="
