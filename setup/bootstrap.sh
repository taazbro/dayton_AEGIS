#!/bin/bash

# Zyberpol AEGIS Bootstrap Script
# Sets up the complete development environment

set -e

echo "=========================================="
echo "🔥 Zyberpol AEGIS - Bootstrap Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || {
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
}

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp setup/env_template.env .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env and add your API keys"
else
    echo "✓ .env file already exists"
fi

# Create reports directory
echo ""
echo "Creating reports directory..."
mkdir -p reports
echo "✓ Reports directory created"

# Create logs directory
echo ""
echo "Creating logs directory..."
mkdir -p logs
echo "✓ Logs directory created"

# Run individual setup scripts
echo ""
echo "Running component setup scripts..."

bash setup/install_sentry.sh
bash setup/install_browseruse.sh
bash setup/install_claude.sh

echo ""
echo "=========================================="
echo "✓ Bootstrap complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run AEGIS: python main.py"
echo ""
