# 🧠 BrainRot Generator - BlackBox AI Edition

## 🚀 Description

Générateur de mèmes absurdes et saturés ultime, propulsé par l'IA BlackBox pour créer du contenu BrainRot de qualité maximale. Cette version avancée utilise l'intelligence artificielle pour générer du contenu créatif et absurde dans différents styles.

## ✨ Fonctionnalités

### 🤖 IA BlackBox Intégrée
- **Génération de contenu intelligent** avec l'API BlackBox
- **4 styles distincts** : Absurde, BrainRot, TikTok, Reddit
- **Prompts personnalisés** ou génération aléatoire
- **Fallback automatique** si l'API n'est pas disponible

### 🎨 Génération Visuelle Avancée
- **Images saturées** avec effets visuels améliorés
- **Dégradés adaptatifs** selon le style choisi
- **Formes géométriques chaotiques** pour l'effet BrainRot
- **Texte avec contours** pour une lisibilité optimale

### 🔊 Audio & Interaction
- **Synthèse vocale française** avec gTTS
- **Interface ultra-saturée** avec animations CSS
- **Téléchargements** image et audio
- **Partage social** intégré
- **Raccourcis clavier** pour power users

## 🛠️ Installation

### Prérequis
- Python 3.8+
- Connexion internet pour l'API BlackBox

### Installation rapide

```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrainRot

# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Créer le dossier de sortie
mkdir -p output

# Lancer le backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (nouveau terminal)
```bash
cd ~/Documents/GitHub/ADJL---BLACKBOX-AI-TRACK/BrainRot/frontend
python3 -m http.server 3000
```

## 🌐 Accès

- **Frontend** : http://localhost:3000
- **Backend API** : http://localhost:8000
- **Documentation API** : http://localhost:8000/docs

## 🎯 Utilisation

### Interface Web
1. **Choisir un style** : Absurde, BrainRot, TikTok, ou Reddit
2. **Entrer un prompt** (optionnel) ou utiliser les suggestions
3. **Cliquer sur "GÉNÉRER DU BRAINROT"** ou "CHAOS TOTAL"
4. **Télécharger** ou **partager** le résultat

### Styles Disponibles

#### 🌀 Absurde
Contenu surréaliste et décalé avec des situations impossibles.

#### 🧠 BrainRot
Slang Gen Z, références TikTok/YouTube, énergie chaotique maximale.

#### 📱 TikTok
Trends viraux, drama fictif, style dramatique et exagéré.

#### 🤓 Reddit
Culture internet, memes, ton sarcastique et intelligent.

### Raccourcis Clavier
- **Ctrl+Enter** : Générer un mème
- **Ctrl+R** : Génération aléatoire
- **Ctrl+D** : Télécharger l'image

## 🔧 API Endpoints

### POST `/generate-brainrot`
Génère un mème avec prompt personnalisé
```json
{
  "prompt": "Chat influenceur secret",
  "style": "brainrot"
}
```

### GET `/random-brainrot`
Génère un mème complètement aléatoire

### GET `/styles`
Liste tous les styles disponibles

### GET `/image/{filename}`
Récupère une image générée

### GET `/audio/{filename}`
Récupère un fichier audio généré

## 🎨 Personnalisation

### Ajouter de nouveaux styles
Modifiez le dictionnaire `style_prompts` dans `backend/main.py` :

```python
style_prompts = {
    "nouveau_style": "Description du prompt pour l'IA...",
    # ...
}
```

### Modifier les couleurs
Ajustez `style_colors` dans la fonction `generate_enhanced_image()`.

## 🐛 Dépannage

### Backend ne démarre pas
```bash
# Vérifier Python
python3 --version

# Réinstaller les dépendances
pip install --upgrade -r requirements.txt
```

### API BlackBox non accessible
L'application utilise un système de fallback automatique avec des textes pré-définis.

### Erreur de CORS
Vérifiez que le frontend accède bien à `http://localhost:8000`.

### Audio ne fonctionne pas
Vérifiez l'installation de gTTS :
```bash
pip install --upgrade gtts
```

## 🔑 Configuration API

L'API BlackBox est configurée dans `backend/main.py` :
```python
BLACKBOX_API_KEY = "sk-FjYYA2K82ssQ4JBpE_0QYA"
```

## 📁 Structure du Projet

```
BrainRot/
├── backend/
│   ├── main.py              # API FastAPI principale
│   ├── requirements.txt     # Dépendances Python
│   └── output/             # Fichiers générés
├── frontend/
│   ├── index.html          # Interface utilisateur
│   ├── style.css           # Styles saturés
│   └── script.js           # Logique frontend
└── README.md               # Ce fichier
```

## 🚀 Fonctionnalités Avancées

### Easter Eggs
- Cliquez 5 fois sur le titre pour activer le mode chaos
- Effets visuels spéciaux aléatoires

### Notifications
- Feedback visuel pour toutes les actions
- Animations fluides et modernes

### Responsive Design
- Interface adaptée mobile et desktop
- Grille flexible pour tous les écrans

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créez une branche feature
3. Committez vos changements
4. Ouvrez une Pull Request

## 📄 Licence

Projet open source pour l'éducation et le divertissement.

## 🎉 Crédits

- **IA** : BlackBox AI pour la génération de contenu
- **Synthèse vocale** : Google Text-to-Speech (gTTS)
- **Framework** : FastAPI + Vanilla JS
- **Design** : Interface BrainRot saturée custom

---

**🧠 Maximum BrainRot Energy Achieved! 🚀**
