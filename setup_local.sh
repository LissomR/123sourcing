#!/bin/bash

echo "🚀 123sourcing Local Setup Script"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL is not installed. Please install MySQL Server."
    echo "   Ubuntu/Debian: sudo apt install mysql-server"
    exit 1
fi

echo "✅ MySQL found"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies for CPU
echo ""
echo "📥 Installing dependencies (CPU version)..."
pip install -r requirements.cpu.txt

# Create .env file if it doesn't exist
if [ ! -f "api_channel/.env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example api_channel/.env
    echo "⚠️  Please edit api_channel/.env with your configuration!"
    echo "   Required: MySQL credentials, Pinecone API key"
else
    echo "✅ .env file already exists"
fi

# Download trained models
if [ ! -d "trained_models" ]; then
    echo ""
    echo "📥 Downloading trained models (this may take a while)..."
    if [ ! -f "trained_models.zip" ]; then
        wget https://d2hbdgqvbu3n3g.cloudfront.net/123sourcing/trained_models.zip
    fi
    
    echo "📦 Extracting models..."
    unzip -q trained_models.zip
    
    # Extract tar files
    if [ -d "trained_models/cpu-model/model" ]; then
        cd trained_models/cpu-model/model
    elif [ -d "trained_models/gpu-model/model" ]; then
        cd trained_models/gpu-model/model
    fi
    
    if [ -f "docprompt_params.tar" ]; then
        tar -xf docprompt_params.tar
    fi
    
    cd ../../..
    rm trained_models.zip
    echo "✅ Models extracted"
else
    echo "✅ Trained models already exist"
fi

# Create MySQL database
echo ""
echo "🗄️  Setting up MySQL database..."
echo "Please enter your MySQL root password when prompted:"
read -sp "MySQL root password: " MYSQL_ROOT_PASSWORD
echo ""

mysql -u root -p"$MYSQL_ROOT_PASSWORD" <<EOF
CREATE DATABASE IF NOT EXISTS 123sourcing_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '123sourcing_user'@'localhost' IDENTIFIED BY 'sourcing123!';
GRANT ALL PRIVILEGES ON 123sourcing_db.* TO '123sourcing_user'@'localhost';
FLUSH PRIVILEGES;
EOF

if [ $? -eq 0 ]; then
    echo "✅ Database created successfully"
    echo ""
    echo "📊 Database credentials:"
    echo "   Database: 123sourcing_db"
    echo "   User: 123sourcing_user"
    echo "   Password: sourcing123!"
    echo ""
    echo "⚠️  Update these in your api_channel/.env file!"
else
    echo "⚠️  Database creation failed. Please create it manually."
fi

# Import database schema
if [ -f "MySql.sql" ]; then
    echo ""
    read -p "Do you want to import the database schema? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        mysql -u 123sourcing_user -psourcing123! 123sourcing_db < MySql.sql
        echo "✅ Database schema imported"
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Edit api_channel/.env with your credentials"
echo "   2. Activate virtual environment: source venv/bin/activate"
echo "   3. Run migrations: python manage.py migrate"
echo "   4. Create superuser: python manage.py createsuperuser"
echo "   5. Run server: python manage.py runserver"
echo ""
echo "🎉 Happy coding!"
