#!/bin/bash

echo "🔧 Installation des dépendances pour le générateur de mèmes..."

# Aller dans le dossier backend
cd backend

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances une par une pour diagnostiquer les problèmes
echo "📦 Installation de FastAPI..."
pip install fastapi

echo "📦 Installation d'Uvicorn..."
pip install "uvicorn[standard]"

echo "📦 Installation de Pillow..."
pip install pillow

echo "📦 Installation de gTTS..."
pip install gtts

echo "📦 Installation de requests..."
pip install requests

echo "📦 Installation de python-multipart..."
pip install python-multipart

echo "📦 Installation de moviepy (peut prendre du temps)..."
pip install moviepy

echo "✅ Installation terminée!"
echo ""
echo "🚀 Vous pouvez maintenant lancer le serveur avec:"
echo "   uvicorn main:app --reload --host 0.0.0.0 --port 8000"
