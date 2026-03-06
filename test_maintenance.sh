#!/bin/bash
# Script para probar el modo de mantenimiento localmente

echo "=========================================="
echo "  Prueba de Modo de Mantenimiento"
echo "=========================================="
echo ""

# Verificar si el servidor está corriendo
if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo "⚠️  El servidor no está corriendo en http://localhost:8000"
    echo "   Inicia el servidor primero con: python manage.py runserver"
    exit 1
fi

echo "1️⃣  Probando sin modo mantenimiento..."
response=$(curl -s -w "\n%{http_code}" http://localhost:8000)
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | sed '$d')

if [ "$http_code" != "503" ]; then
    echo "✅ Sistema funcionando normalmente (HTTP $http_code)"
else
    echo "⚠️  Sistema ya está en modo mantenimiento"
fi

echo ""
echo "2️⃣  Activando modo mantenimiento..."
export MAINTENANCE_MODE=true

echo ""
echo "3️⃣  Para activar el modo en tu servidor local, ejecuta:"
echo "    export MAINTENANCE_MODE=true"
echo "    python manage.py runserver"
echo ""
echo "4️⃣  Para activar en Railway:"
echo "    railway variables --set MAINTENANCE_MODE=true"
echo ""
echo "5️⃣  Para desactivar en Railway:"
echo "    railway variables --set MAINTENANCE_MODE=false"
echo ""
echo "=========================================="
echo "✅ Configuración completada!"
echo "=========================================="
