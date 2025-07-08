# 🚀 Guide de Démarrage - Générateur de Mèmes Absurdes

## ⚠️ Problème moviepy résolu

Si vous avez l'erreur `ModuleNotFoundError: No module named 'moviepy.editor'`, suivez ces étapes :

## 🔧 Solution Rapide (Version Simple)

### 1. Nettoyer l'environnement
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot/backend
rm -rf venv
```

### 2. Lancer la version simple
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot
./start_simple.sh
```

### 3. Si le script ne fonctionne pas, lancement manuel :
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot/backend

# Créer un nouvel environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances simplifiées
pip install -r requirements_simple.txt

# Lancer la version simple (SANS moviepy)
uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
```

### 4. Frontend (dans un autre terminal)
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot/frontend
python3 -m http.server 3000
```

## 🌐 Accès à l'application
- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation** : http://localhost:8000/docs

## 🎯 Fonctionnalités de la version simple
- ✅ Génération d'images absurdes et saturées
- ✅ Synthèse vocale française
- ✅ Interface web colorée
- ✅ Téléchargement image + audio séparément
- ❌ Pas de vidéos (nécessite moviepy)

## 🎬 Pour activer les vidéos (optionnel)

Si vous voulez absolument les vidéos, installez moviepy :
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot/backend
source venv/bin/activate
pip install moviepy
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🐛 Dépannage

### Erreur "command not found"
```bash
chmod +x ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrianRot/start_simple.sh
```

### Erreur de port occupé
```bash
# Tuer les processus sur le port 8000
sudo lsof -ti:8000 | xargs kill -9
```

### Python non trouvé
```bash
# Vérifier Python
python3 --version
# Ou essayer
python --version
```

## ✅ Test rapide

Une fois lancé, testez avec :
```bash
curl http://localhost:8000/
```

Vous devriez voir : `{"message": "Générateur de Mèmes Absurdes - API fonctionnelle!"}`
