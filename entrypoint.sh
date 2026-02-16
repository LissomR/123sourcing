#!/bin/bash
set -e

echo "=========================================="
echo "  Starting 123sourcing Application"
echo "=========================================="

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
MAX_RETRIES=30
RETRY_COUNT=0
while ! python -c "
import MySQLdb
try:
    conn = MySQLdb.connect(
        host='$DJANGO_DATABASE_SERVER',
        user='$DJANGO_DATABASE_USER',
        passwd='$DJANGO_DATABASE_PASSWORD',
        port=int('${DJANGO_DATABASE_PORT:-3306}'),
        db='$DJANGO_DATABASE_NAME'
    )
    conn.close()
    print('MySQL is ready!')
except Exception as e:
    print(f'MySQL not ready: {e}')
    exit(1)
" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "ERROR: MySQL not available after $MAX_RETRIES retries"
        break
    fi
    echo "Retry $RETRY_COUNT/$MAX_RETRIES..."
    sleep 2
done

# Create database tables if they don't exist
echo "Creating database tables..."
python -c "
import MySQLdb
import os

host = os.environ.get('DJANGO_DATABASE_SERVER', 'localhost')
user = os.environ.get('DJANGO_DATABASE_USER', 'root')
passwd = os.environ.get('DJANGO_DATABASE_PASSWORD', '')
port = int(os.environ.get('DJANGO_DATABASE_PORT', '3306'))
db = os.environ.get('DJANGO_DATABASE_NAME', 'railway')

try:
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, port=port, db=db)
    cursor = conn.cursor()
    
    # Check if tables already exist
    cursor.execute('SHOW TABLES')
    tables = [t[0] for t in cursor.fetchall()]
    
    if 'sb_users' not in tables:
        print('Creating sb_users table...')
        cursor.execute('''
            CREATE TABLE sb_users (
                user_id bigint NOT NULL AUTO_INCREMENT,
                user_type enum('SUPER_BO','BO') NOT NULL,
                first_name varchar(50) NOT NULL,
                middle_name varchar(50) DEFAULT NULL,
                last_name varchar(50) NOT NULL,
                status enum('ACTIVE','INACTIVE','TERMINATE') DEFAULT NULL,
                password varchar(100) NOT NULL,
                mobile_code varchar(10) DEFAULT NULL,
                mobile_no varchar(15) DEFAULT NULL,
                email_id varchar(100) NOT NULL,
                address_one varchar(250) DEFAULT NULL,
                address_two varchar(250) DEFAULT NULL,
                city_code varchar(15) DEFAULT NULL,
                city varchar(50) DEFAULT NULL,
                state_code varchar(15) DEFAULT NULL,
                state varchar(50) DEFAULT NULL,
                country_code varchar(15) DEFAULT NULL,
                country varchar(50) DEFAULT NULL,
                zip varchar(20) DEFAULT NULL,
                created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id),
                UNIQUE KEY email_id (email_id),
                UNIQUE KEY mobile_no (mobile_no)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print('  sb_users created.')
    else:
        print('  sb_users already exists.')
    
    if 'sb_users_token' not in tables:
        print('Creating sb_users_token table...')
        cursor.execute('''
            CREATE TABLE sb_users_token (
                id int NOT NULL AUTO_INCREMENT,
                user_id int NOT NULL,
                token varchar(500) DEFAULT NULL,
                expire_at datetime DEFAULT CURRENT_TIMESTAMP,
                created_at datetime DEFAULT CURRENT_TIMESTAMP,
                updated_at datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (id),
                KEY user_id_idx (user_id)
            ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print('  sb_users_token created.')
    else:
        print('  sb_users_token already exists.')
    
    conn.commit()
    cursor.close()
    conn.close()
    print('Database setup complete!')
except Exception as e:
    print(f'Database setup error: {e}')
    print('Continuing anyway...')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input 2>/dev/null || true

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn api_channel.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --timeout 300 \
    --workers 2 \
    --access-logfile - \
    --error-logfile -
