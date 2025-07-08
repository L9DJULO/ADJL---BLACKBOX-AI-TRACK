#!/bin/bash

echo "🧠 Générateur de Mèmes Absurdes - Version Simple 🧠"
echo "===================================================="

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

# Installer les dépendances simplifiées (sans moviepy)
echo "📥 Installation des dépendances simplifiées..."
pip install -r requirements_simple.txt

# Créer le dossier output
mkdir -p output

echo ""
echo "🚀 Lancement du serveur backend (version simple)..."
echo "📍 Backend: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "🌐 Pour le frontend, ouvrez un autre terminal et lancez:"
echo "   cd frontend"
echo "   python3 -m http.server 3000"
echo "   Puis ouvrez: http://localhost:3000"
echo ""
echo "ℹ️  Version simple: génère image + audio séparément"
echo "   Pour les vidéos, installez moviepy et utilisez main.py"
echo ""
echo "🛑 Arrêter avec Ctrl+C"
echo ""

# Lancer le serveur avec la version simple
uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
