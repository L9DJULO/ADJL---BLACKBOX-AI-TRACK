#!/bin/bash

# AI Voice Code Assistant - Setup Script
echo "🚀 Setting up AI Voice Code Assistant..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

# Upgrade pip and setuptools
echo "⬆️ Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install core requirements first
echo "📚 Installing core dependencies..."
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.4.2
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install requests==2.31.0
pip install aiohttp==3.9.1
pip install websockets==12.0
pip install GitPython==3.1.40

# Install API clients
echo "🔌 Installing API clients..."
pip install groq==0.4.1
pip install openai==1.3.5

# Install testing dependencies
echo "🧪 Installing testing dependencies..."
pip install pytest==7.4.3
pip install pytest-asyncio==0.21.1
pip install pytest-cov==4.1.0

# Optional: Install ML dependencies (comment out if not needed)
echo "🤖 Installing ML dependencies (optional)..."
echo "Skip this if you don't need local Llama model support"
# pip install torch==2.1.0 --index-url https://download.pytorch.org/whl/cpu
# pip install transformers==4.35.2

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and add your API keys"
echo "2. Run the server with: python app.py"
echo ""
echo "If you encounter any issues, try:"
echo "- pip install --no-cache-dir -r requirements.txt"
echo "- pip install --force-reinstall -r requirements.txt"