const API_BASE_URL = 'http://localhost:8000';
let currentStyle = 'absurd';
let currentImageUrl = '';
let currentAudioUrl = '';
let currentText = '';

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    loadStyles();
});

function setupEventListeners() {
    // Boutons de style
    document.querySelectorAll('.style-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.style-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentStyle = this.dataset.style;
        });
    });

    // Bouton de génération
    document.getElementById('generateBtn').addEventListener('click', generateBrainRot);
    
    // Bouton chaos total
    document.getElementById('randomBtn').addEventListener('click', generateRandomBrainRot);
    
    // Enter dans le textarea
    document.getElementById('promptInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.ctrlKey) {
            generateBrainRot();
        }
    });
}

async function loadStyles() {
    try {
        const response = await fetch(`${API_BASE_URL}/styles`);
        if (response.ok) {
            const data = await response.json();
            console.log('Styles disponibles:', data.styles);
        }
    } catch (error) {
        console.log('Impossible de charger les styles:', error);
    }
}

async function generateBrainRot() {
    const prompt = document.getElementById('promptInput').value.trim();
    
    // Afficher le loading
    showLoading();
    disableButtons();
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-brainrot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                style: currentStyle
            })
        });
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        displayResult(data);
        
    } catch (error) {
        console.error('Erreur:', error);
        showError('Erreur lors de la génération du BrainRot. Vérifiez que le serveur backend est démarré.');
    } finally {
        hideLoading();
        enableButtons();
    }
}

async function generateRandomBrainRot() {
    showLoading();
    disableButtons();
    
    try {
        const response = await fetch(`${API_BASE_URL}/random-brainrot`);
        
        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        displayResult(data);
        
        // Mettre à jour le style sélectionné
        currentStyle = data.style;
        document.querySelectorAll('.style-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.style === currentStyle);
        });
        
    } catch (error) {
        console.error('Erreur:', error);
        showError('Erreur lors de la génération aléatoire. Vérifiez que le serveur backend est démarré.');
    } finally {
        hideLoading();
        enableButtons();
    }
}

function displayResult(data) {
    // Cacher le loading et afficher le résultat
    hideLoading();
    document.getElementById('result').classList.remove('hidden');
    
    // Mettre à jour les informations IA
    document.getElementById('aiInfo').textContent = data.ai_info || `Style: ${data.style}`;
    
    // Mettre à jour l'image
    if (data.image_url) {
        currentImageUrl = `${API_BASE_URL}${data.image_url}`;
        const imageElement = document.getElementById('memeImage');
        imageElement.src = currentImageUrl;
        imageElement.style.display = 'block';
    }
    
    // Mettre à jour l'audio
    if (data.audio_url) {
        currentAudioUrl = `${API_BASE_URL}${data.audio_url}`;
        const audioElement = document.getElementById('memeAudio');
        audioElement.src = currentAudioUrl;
        audioElement.style.display = 'block';
    } else {
        document.getElementById('memeAudio').style.display = 'none';
    }
    
    // Mettre à jour le texte
    currentText = data.text;
    document.getElementById('generatedText').textContent = currentText;
    
    // Scroll vers le résultat
    document.getElementById('result').scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    // Animation d'apparition
    setTimeout(() => {
        document.getElementById('result').style.animation = 'bounce 0.6s ease';
    }, 100);
}

function showLoading() {
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
}

function hideLoading() {
    document.getElementById('loading').classList.add('hidden');
}

function disableButtons() {
    document.getElementById('generateBtn').disabled = true;
    document.getElementById('randomBtn').disabled = true;
}

function enableButtons() {
    document.getElementById('generateBtn').disabled = false;
    document.getElementById('randomBtn').disabled = false;
}

function showError(message) {
    alert(message);
    hideLoading();
}

// Fonctions utilitaires
function setPrompt(text) {
    document.getElementById('promptInput').value = text;
    // Animation du textarea
    const textarea = document.getElementById('promptInput');
    textarea.style.animation = 'pulse 0.5s ease';
    setTimeout(() => {
        textarea.style.animation = '';
    }, 500);
}

function downloadImage() {
    if (currentImageUrl) {
        const a = document.createElement('a');
        a.href = currentImageUrl;
        a.download = `brainrot-${currentStyle}-${Date.now()}.png`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Feedback visuel
        showNotification('📥 Image téléchargée!');
    }
}

function downloadAudio() {
    if (currentAudioUrl) {
        const a = document.createElement('a');
        a.href = currentAudioUrl;
        a.download = `brainrot-audio-${Date.now()}.mp3`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Feedback visuel
        showNotification('🔊 Audio téléchargé!');
    }
}

function shareContent() {
    if (currentText) {
        if (navigator.share) {
            navigator.share({
                title: '🧠 BrainRot Generator',
                text: currentText,
                url: window.location.href
            }).catch(console.error);
        } else {
            // Fallback: copier dans le presse-papiers
            navigator.clipboard.writeText(currentText).then(() => {
                showNotification('📤 Texte copié dans le presse-papiers!');
            }).catch(() => {
                // Fallback ultime
                const textArea = document.createElement('textarea');
                textArea.value = currentText;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showNotification('📤 Texte copié!');
            });
        }
    }
}

function generateAnother() {
    // Vider le prompt pour plus de variété
    document.getElementById('promptInput').value = '';
    
    // Changer de style aléatoirement
    const styles = ['absurd', 'brainrot', 'tiktok', 'reddit'];
    const randomStyle = styles[Math.floor(Math.random() * styles.length)];
    
    document.querySelectorAll('.style-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.style === randomStyle);
    });
    currentStyle = randomStyle;
    
    // Générer
    generateBrainRot();
}

function showNotification(message) {
    // Créer une notification temporaire
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(45deg, #ff006e, #8338ec);
        color: white;
        padding: 15px 25px;
        border-radius: 25px;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.3);
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Ajouter les animations CSS pour les notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Easter eggs et interactions spéciales
let clickCount = 0;
document.querySelector('.header h1').addEventListener('click', function() {
    clickCount++;
    if (clickCount >= 5) {
        this.style.animation = 'spin 2s ease';
        showNotification('🎉 Mode chaos activé!');
        clickCount = 0;
        
        // Activer des effets spéciaux temporaires
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = '';
            this.style.animation = '';
        }, 2000);
    }
});

// Raccourcis clavier
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'Enter':
                e.preventDefault();
                generateBrainRot();
                break;
            case 'r':
                e.preventDefault();
                generateRandomBrainRot();
                break;
            case 'd':
                e.preventDefault();
                if (currentImageUrl) downloadImage();
                break;
        }
    }
});

// Gestion des erreurs globales
window.addEventListener('error', function(e) {
    console.error('Erreur JavaScript:', e.error);
});

// Feedback de connexion au backend
async function checkBackendStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            console.log('✅ Backend connecté');
        }
    } catch (error) {
        console.warn('⚠️ Backend non accessible:', error.message);
    }
}

// Vérifier la connexion au démarrage
checkBackendStatus();
