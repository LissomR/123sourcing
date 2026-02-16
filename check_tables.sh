#!/bin/bash

echo "Verificando tablas en la base de datos 123sourcing_db..."
echo ""

mysql -u 123sourcing_user -p'sourcing123!' -h localhost 123sourcing_db << EOF
SHOW TABLES;
EOF

echo ""
echo "Verificando estructura de la tabla sb_users..."
mysql -u 123sourcing_user -p'sourcing123!' -h localhost 123sourcing_db << EOF
DESCRIBE sb_users;
EOF

echo ""
echo "Verificando estructura de la tabla sb_users_token..."
mysql -u 123sourcing_user -p'sourcing123!' -h localhost 123sourcing_db << EOF
DESCRIBE sb_users_token;
EOF
