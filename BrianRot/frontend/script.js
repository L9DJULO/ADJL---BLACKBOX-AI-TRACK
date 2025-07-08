const API_BASE_URL = 'http://localhost:8000';

let currentVideoUrl = null;

async function generateMeme() {
    const text = document.getElementById('memeText').value.trim();
    
    if (!text) {
        alert('Veuillez entrer du texte pour générer un mème !');
        return;
    }
    
    // Show loading, hide result
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
    document.getElementById('generateBtn').disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-meme`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        if (!response.ok) {
            throw new Error('Erreur lors de la génération du mème');
        }
        
        const data = await response.json();
        
        // Show result, hide loading
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('result').classList.remove('hidden');
        
        // Check if we have video or separate image/audio
        if (data.video_url) {
            currentVideoUrl = `${API_BASE_URL}${data.video_url}`;
            const video = document.getElementById('memeVideo');
            video.src = currentVideoUrl;
            video.load();
        } else if (data.image_url && data.audio_url) {
            // Display image and audio separately
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `
                <h3>Votre mème absurde :</h3>
                <img src="${API_BASE_URL}${data.image_url}" alt="Mème généré" style="max-width: 640px; border-radius: 15px; margin-bottom: 15px;">
                <br>
                <audio controls style="margin-bottom: 20px;">
                    <source src="${API_BASE_URL}${data.audio_url}" type="audio/mpeg">
                    Votre navigateur ne supporte pas la lecture audio.
                </audio>
                <div class="actions">
                    <button onclick="downloadImage('${API_BASE_URL}${data.image_url}')">Télécharger Image</button>
                    <button onclick="downloadAudio('${API_BASE_URL}${data.audio_url}')">Télécharger Audio</button>
                    <button onclick="generateAnother()">Générer un autre</button>
                </div>
            `;
        }
        
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la génération du mème. Vérifiez que le serveur backend est démarré.');
        document.getElementById('loading').classList.add('hidden');
    } finally {
        document.getElementById('generateBtn').disabled = false;
    }
}

function setSuggestion(text) {
    document.getElementById('memeText').value = text;
}

function generateAnother() {
    document.getElementById('result').classList.add('hidden');
    document.getElementById('memeText').value = '';
    document.getElementById('memeText').focus();
}

function downloadVideo() {
    if (currentVideoUrl) {
        const a = document.createElement('a');
        a.href = currentVideoUrl;
        a.download = `meme-absurde-${Date.now()}.mp4`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

function downloadImage(imageUrl) {
    const a = document.createElement('a');
    a.href = imageUrl;
    a.download = `meme-image-${Date.now()}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

function downloadAudio(audioUrl) {
    const a = document.createElement('a');
    a.href = audioUrl;
    a.download = `meme-audio-${Date.now()}.mp3`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Add some random absurd text suggestions
const absurdSuggestions = [
    "Quand tu réalises que les nuages sont des moutons en vacances",
    "POV: Tu es un cactus qui fait du yoga",
    "Moi quand je découvre que mon chat parle italien",
    "Les spaghettis qui dansent la salsa à 3h du matin",
    "Quand ton réveil devient un DJ de techno",
    "POV: Tu es une pizza qui rêve d'être astronaute",
    "Moi expliquant à ma plante pourquoi elle doit payer le loyer",
    "Quand tu réalises que les chaussettes ont une vie secrète",
    "POV: Tu es un pingouin qui vend des glaces au pôle Nord",
    "Moi quand je vois que mon frigo organise une rave party"
];

// Add random suggestion button
function addRandomSuggestion() {
    const randomText = absurdSuggestions[Math.floor(Math.random() * absurdSuggestions.length)];
    document.getElementById('memeText').value = randomText;
}

// Add keyboard shortcut for generation
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        generateMeme();
    }
});

// Add random suggestion button to the page
document.addEventListener('DOMContentLoaded', function() {
    const suggestionsDiv = document.querySelector('.suggestion-buttons');
    const randomBtn = document.createElement('button');
    randomBtn.textContent = '🎲 Suggestion aléatoire';
    randomBtn.onclick = addRandomSuggestion;
    suggestionsDiv.appendChild(randomBtn);
});
