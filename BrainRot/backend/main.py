from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from gtts import gTTS
import requests
import random
import os
import uuid
import json

app = FastAPI(title="BrainRot Generator", description="Générateur de mèmes absurdes avec IA BlackBox")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration BlackBox API
BLACKBOX_API_KEY = "sk-9zouY4NbLdKuti9hJgNL0w"
BLACKBOX_API_URL = "https://api.blackboxai.com/v1/chat/completions"

# Directory to store generated files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class MemeRequest(BaseModel):
    prompt: str = ""
    style: str = "absurd"  # absurd, brainrot, tiktok, reddit

class AIGeneratedContent(BaseModel):
    text: str
    style_instructions: str

@app.get("/")
async def root():
    return {"message": "🧠 BrainRot Generator avec BlackBox AI - API fonctionnelle! 🧠"}

def generate_brainrot_content(prompt: str, style: str) -> AIGeneratedContent:
    """Génère du contenu brainrot avec l'API BlackBox"""
    
    style_prompts = {
        "absurd": "Génère un texte complètement absurde et surréaliste de maximum 50 mots, style mème internet français. Utilise des références décalées et des situations impossibles.",
        "brainrot": "Crée un texte brainrot Gen Z français avec du slang internet, des références TikTok/YouTube, maximum 50 mots. Style très énergique et chaotique.",
        "tiktok": "Écris un texte viral TikTok français avec des trends actuels, du drama fictif, maximum 50 mots. Style dramatique et exagéré.",
        "reddit": "Génère un texte style Reddit français, avec des références de culture internet, memes, maximum 50 mots. Ton sarcastique et intelligent."
    }
    
    system_prompt = style_prompts.get(style, style_prompts["absurd"])
    
    if prompt:
        full_prompt = f"{system_prompt} Thème: {prompt}"
    else:
        full_prompt = f"{system_prompt} Invente un thème complètement aléatoire."
    
    headers = {
        "Authorization": f"Bearer {BLACKBOX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "blackboxai",
        "messages": [
            {"role": "system", "content": "Tu es un générateur de contenu brainrot français. Réponds UNIQUEMENT avec le texte demandé, sans explication."},
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 100,
        "temperature": 0.9
    }
    
    try:
        response = requests.post(BLACKBOX_API_URL, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            generated_text = result["choices"][0]["message"]["content"].strip()
            return AIGeneratedContent(
                text=generated_text,
                style_instructions=f"Style: {style}, généré par BlackBox AI"
            )
    except Exception as e:
        print(f"Erreur API BlackBox: {e}")
    
    # Fallback si l'API ne fonctionne pas
    fallback_texts = {
        "absurd": [
            "Quand tu réalises que les nuages sont des moutons en vacances qui ont oublié de redescendre",
            "POV: Tu es un pingouin qui fait du skateboard dans l'espace intersidéral",
            "Les chaussettes qui disparaissent sont en fait des agents secrets infiltrés",
            "Moi quand je vois que mon frigo parle mandarin avec les légumes"
        ],
        "brainrot": [
            "No cap cette situation est trop sus, j'ai ghost mes responsabilités fr fr",
            "Bro cette vibe est pas it, on dirait un NPC qui a bug dans la matrix",
            "Sheesh cette energy me donne des flashbacks de mes 13 ans sur TikTok",
            "Respectfully cette situation me trigger, c'est du pure chaos energy"
        ],
        "tiktok": [
            "STORYTIME: Comment j'ai découvert que mon chat était secrètement influenceur",
            "POV: Tu réalises que ta vie est un TikTok raté mais tu continues quand même",
            "Plot twist: Les adultes comprennent rien à notre génération et c'est iconic",
            "Main character energy: Quand tu danses sur du Phonk à 3h du matin"
        ],
        "reddit": [
            "AITA pour avoir expliqué à mon chat pourquoi ses memes sont cringe?",
            "TIL que les boomers pensent que nous sommes tous des NPCs",
            "Unpopular opinion: Les memes d'aujourd'hui sont trop meta pour être drôles",
            "ELI5: Pourquoi ma génération communique uniquement par références obscures?"
        ]
    }
    
    selected_texts = fallback_texts.get(style, fallback_texts["absurd"])
    return AIGeneratedContent(
        text=random.choice(selected_texts),
        style_instructions=f"Style: {style}, texte de fallback"
    )

def generate_enhanced_image(content: AIGeneratedContent) -> str:
    """Génère une image améliorée basée sur le contenu IA"""
    width, height = 800, 600
    
    # Couleurs selon le style
    style_colors = {
        "absurd": [(255, 100, 150), (100, 255, 200), (255, 200, 100)],
        "brainrot": [(255, 0, 255), (0, 255, 255), (255, 255, 0)],
        "tiktok": [(255, 20, 147), (0, 191, 255), (50, 205, 50)],
        "reddit": [(255, 69, 0), (0, 123, 255), (40, 167, 69)]
    }
    
    # Déterminer le style depuis les instructions
    current_style = "absurd"
    for style in style_colors.keys():
        if style in content.style_instructions.lower():
            current_style = style
            break
    
    colors = style_colors[current_style]
    
    # Créer l'image de base avec dégradé
    image = Image.new("RGB", (width, height), color=colors[0])
    draw = ImageDraw.Draw(image)
    
    # Ajouter un dégradé de fond
    for y in range(height):
        ratio = y / height
        r = int(colors[0][0] * (1 - ratio) + colors[1][0] * ratio)
        g = int(colors[0][1] * (1 - ratio) + colors[1][1] * ratio)
        b = int(colors[0][2] * (1 - ratio) + colors[1][2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # Ajouter des formes géométriques chaotiques
    for _ in range(random.randint(15, 30)):
        shape_type = random.choice(["ellipse", "rectangle", "polygon"])
        x0 = random.randint(-50, width)
        y0 = random.randint(-50, height)
        x1 = x0 + random.randint(30, 150)
        y1 = y0 + random.randint(30, 150)
        color = random.choice(colors + [(255, 255, 255), (0, 0, 0)])
        
        if shape_type == "ellipse":
            draw.ellipse([x0, y0, x1, y1], fill=color, outline=None)
        elif shape_type == "rectangle":
            draw.rectangle([x0, y0, x1, y1], fill=color, outline=None)
        else:  # polygon
            points = [(x0, y0), (x1, y0), (x1, y1), (x0 + random.randint(-30, 30), y1)]
            draw.polygon(points, fill=color, outline=None)
    
    # Appliquer des effets de saturation extrême
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(2.5)
    
    # Ajouter du contraste
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.8)
    
    # Ajouter le texte avec style adaptatif
    try:
        font_size = max(24, min(48, 800 // len(content.text) * 2))
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Texte avec contour pour la lisibilité
    text_lines = []
    words = content.text.split()
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if len(test_line) > 25:  # Limite de caractères par ligne
            if current_line:
                text_lines.append(current_line)
                current_line = word
            else:
                text_lines.append(word)
        else:
            current_line = test_line
    
    if current_line:
        text_lines.append(current_line)
    
    # Positionner le texte
    total_text_height = len(text_lines) * (font_size + 10)
    start_y = height - total_text_height - 20
    
    for i, line in enumerate(text_lines):
        y_pos = start_y + i * (font_size + 10)
        x_pos = 20
        
        # Contour noir
        for dx in [-2, -1, 0, 1, 2]:
            for dy in [-2, -1, 0, 1, 2]:
                if dx != 0 or dy != 0:
                    draw.text((x_pos + dx, y_pos + dy), line, font=font, fill=(0, 0, 0))
        
        # Texte principal en blanc
        draw.text((x_pos, y_pos), line, font=font, fill=(255, 255, 255))
    
    # Sauvegarder l'image
    image_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.png")
    image.save(image_path)
    return image_path

def generate_voice(text: str) -> str:
    """Génère la synthèse vocale"""
    try:
        tts = gTTS(text=text, lang='fr', slow=False)
        audio_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Erreur génération audio: {e}")
        return None

@app.post("/generate-brainrot")
async def generate_brainrot(request: MemeRequest):
    """Génère un mème brainrot avec IA BlackBox"""
    try:
        # Générer le contenu avec BlackBox AI
        ai_content = generate_brainrot_content(request.prompt, request.style)
        
        # Générer l'image améliorée
        image_path = generate_enhanced_image(ai_content)
        
        # Générer l'audio
        audio_path = generate_voice(ai_content.text)
        
        response = {
            "text": ai_content.text,
            "style": request.style,
            "ai_info": ai_content.style_instructions,
            "image_url": f"/image/{os.path.basename(image_path)}"
        }
        
        if audio_path:
            response["audio_url"] = f"/audio/{os.path.basename(audio_path)}"
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération: {str(e)}")

@app.get("/random-brainrot")
async def random_brainrot():
    """Génère un mème brainrot complètement aléatoire"""
    styles = ["absurd", "brainrot", "tiktok", "reddit"]
    random_style = random.choice(styles)
    
    request = MemeRequest(prompt="", style=random_style)
    return await generate_brainrot(request)

@app.get("/image/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    raise HTTPException(status_code=404, detail="Image non trouvée")

@app.get("/audio/{audio_filename}")
async def get_audio(audio_filename: str):
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio non trouvé")

@app.get("/styles")
async def get_styles():
    """Retourne les styles disponibles"""
    return {
        "styles": [
            {"id": "absurd", "name": "Absurde", "description": "Contenu surréaliste et décalé"},
            {"id": "brainrot", "name": "BrainRot", "description": "Slang Gen Z et chaos énergétique"},
            {"id": "tiktok", "name": "TikTok", "description": "Trends viraux et drama"},
            {"id": "reddit", "name": "Reddit", "description": "Culture internet et sarcasme"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
