#!/bin/bash
# Script para limpiar archivos obsoletos relacionados con MySQL

echo "=========================================="
echo "  Limpiando Archivos Obsoletos de MySQL"
echo "=========================================="
echo ""
echo "Los siguientes archivos ya NO son necesarios:"
echo ""

# Lista de archivos obsoletos
OBSOLETE_FILES=(
    "MySql.sql"
    "check_tables.sh"
    "create_railway_tables.sh"
    "setup_database.sh"
    "setup_railway_db.sh"
    "RAILWAY_DATABASE_SETUP.md"
)

for file in "${OBSOLETE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ❌ $file (relacionado con MySQL)"
    fi
done

echo ""
echo "=========================================="
echo "¿Deseas eliminar estos archivos? (s/n)"
read -r response

if [[ "$response" =~ ^[SsYy]$ ]]; then
    echo ""
    echo "Eliminando archivos..."
    for file in "${OBSOLETE_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm "$file"
            echo "  ✅ Eliminado: $file"
        fi
    done
    echo ""
    echo "✅ Limpieza completada!"
else
    echo ""
    echo "ℹ️  Archivos conservados. Puedes eliminarlos manualmente cuando quieras."
fi

echo ""
echo "=========================================="
echo "  Archivos que DEBES mantener:"
echo "=========================================="
echo "  ✅ entrypoint.sh (actualizado sin MySQL)"
echo "  ✅ Dockerfile.railway (actualizado sin MySQL)"
echo "  ✅ requirements.txt (sin mysqlclient)"
echo "  ✅ requirements.cpu.txt (sin mysqlclient)"
echo "  ✅ api_channel/settings.py (usando SQLite)"
echo ""
echo "Lee MYSQL_REMOVED.md para más información"
