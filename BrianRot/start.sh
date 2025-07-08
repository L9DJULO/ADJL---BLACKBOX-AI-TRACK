#!/bin/bash

echo "🧠 Générateur de Mèmes Absurdes - BrineRot 🧠"
echo "=============================================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Aller dans le dossier backend
cd backend

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel Python..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

# Créer le dossier output
mkdir -p output

echo ""
echo "🚀 Lancement du serveur backend..."
echo "📍 Backend: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "🌐 Pour le frontend, ouvrez un autre terminal et lancez:"
echo "   cd frontend"
echo "   python3 -m http.server 3000"
echo "   Puis ouvrez: http://localhost:3000"
echo ""
echo "🛑 Arrêter avec Ctrl+C"
echo ""

# Lancer le serveur
python run.py
