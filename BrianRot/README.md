# 🧠 Générateur de Mèmes Absurdes - BrineRot

Une application qui génère automatiquement des mèmes absurdes et saturés, façon TikTok ou Reddit.

## 🧰 Tech Stack

- **Backend**: Python avec FastAPI
- **Frontend**: HTML/CSS/JavaScript
- **Librairies**: Pillow, gTTS, moviepy, requests, random

## 📁 Structure du projet

```
absurd-meme-generator/
├── backend/
│   ├── main.py           # Serveur FastAPI
│   ├── requirements.txt  # Dépendances Python
│   └── output/          # Dossier généré pour les fichiers de sortie
├── frontend/
│   ├── index.html       # Interface utilisateur
│   ├── style.css        # Styles CSS saturés
│   └── script.js        # Logique frontend
└── README.md
```

## 🚀 Installation et lancement

### 1. Backend (FastAPI)

```bash
# Aller dans le dossier backend
cd backend

# Créer un environnement virtuel Python
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le serveur FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur `http://localhost:8000`

### 2. Frontend

```bash
# Aller dans le dossier frontend
cd frontend

# Servir les fichiers statiques (plusieurs options):

# Option 1: Avec Python
python -m http.server 3000

# Option 2: Avec Node.js (si installé)
npx serve . -p 3000

# Option 3: Ouvrir directement index.html dans un navigateur
```

Le frontend sera accessible sur `http://localhost:3000`

## 🎮 Utilisation

1. Ouvrez le frontend dans votre navigateur
2. Entrez un texte absurde dans la zone de texte
3. Cliquez sur "Générer un Mème"
4. Regardez votre mème vidéo généré avec voix et images saturées !
5. Téléchargez ou générez un nouveau mème

## 🎨 Fonctionnalités

- **Génération d'images absurdes**: Formes colorées et saturées avec Pillow
- **Synthèse vocale**: Conversion du texte en voix française avec gTTS
- **Création de vidéos**: Combinaison image + audio avec moviepy
- **Interface saturée**: Design coloré façon TikTok/Reddit
- **Suggestions de textes**: Boutons avec des idées absurdes pré-définies
- **Téléchargement**: Sauvegarde des mèmes générés

## 🔧 API Endpoints

- `POST /generate-meme`: Génère un mème à partir d'un texte
- `GET /video/{filename}`: Récupère une vidéo générée

## 🎯 Exemple de textes absurdes

- "Quand tu réalises que les bananes sont des téléphones jaunes"
- "POV: Tu es un pingouin qui fait du skateboard dans l'espace"
- "Moi quand je vois que mon frigo parle mandarin"
- "Les chaussettes qui disparaissent sont en fait des agents secrets"

## 🛠️ Développement

Pour modifier l'application:

1. **Backend**: Modifiez `main.py` pour changer la logique de génération
2. **Frontend**: Modifiez les fichiers HTML/CSS/JS pour l'interface
3. **Styles**: Ajustez `style.css` pour des effets plus saturés
4. **Textes**: Ajoutez des suggestions dans `script.js`

## 📝 Notes

- Les fichiers générés sont stockés dans `backend/output/`
- L'application utilise des polices système par défaut
- La génération peut prendre quelques secondes selon la complexité
- Compatible avec tous les navigateurs modernes

Amusez-vous bien avec vos mèmes absurdes ! 🎉
