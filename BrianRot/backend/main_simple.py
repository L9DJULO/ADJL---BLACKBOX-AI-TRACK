from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from gtts import gTTS
import random
import os
import io
import uuid
import base64

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store generated files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class MemeRequest(BaseModel):
    text: str

def generate_absurd_image(text: str) -> str:
    # Create a saturated absurd image with Pillow
    width, height = 640, 480
    image = Image.new("RGB", (width, height), color=(random.randint(100,255), random.randint(100,255), random.randint(100,255)))
    draw = ImageDraw.Draw(image)

    # Draw random shapes for absurdity
    for _ in range(30):
        shape_type = random.choice(["ellipse", "rectangle"])
        x0 = random.randint(0, width)
        y0 = random.randint(0, height)
        x1 = x0 + random.randint(20, 100)
        y1 = y0 + random.randint(20, 100)
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        if shape_type == "ellipse":
            draw.ellipse([x0, y0, x1, y1], fill=color, outline=None)
        else:
            draw.rectangle([x0, y0, x1, y1], fill=color, outline=None)

    # Add saturated overlay
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(3.0)  # increase saturation

    # Add text in a bold font
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    text_position = (20, height - 80)
    draw.text(text_position, text, font=font, fill=(255,255,255))

    # Save image
    image_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.png")
    image.save(image_path)
    return image_path

def generate_voice(text: str) -> str:
    tts = gTTS(text=text, lang='fr')
    audio_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp3")
    tts.save(audio_path)
    return audio_path

@app.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    image_path = generate_absurd_image(request.text)
    audio_path = generate_voice(request.text)
    
    return {
        "image_url": f"/image/{os.path.basename(image_path)}",
        "audio_url": f"/audio/{os.path.basename(audio_path)}",
        "message": "Mème généré avec succès! Image et audio séparés (vidéo nécessite moviepy)"
    }

@app.get("/image/{image_filename}")
async def get_image(image_filename: str):
    image_path = os.path.join(OUTPUT_DIR, image_filename)
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    return Response(status_code=404)

@app.get("/audio/{audio_filename}")
async def get_audio(audio_filename: str):
    audio_path = os.path.join(OUTPUT_DIR, audio_filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    return Response(status_code=404)

@app.get("/")
async def root():
    return {"message": "Générateur de Mèmes Absurdes - API fonctionnelle!"}
