from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from gtts import gTTS
from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip
import random
import os
import io
import uuid

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

def create_video(image_path: str, audio_path: str) -> str:
    clip = ImageClip(image_path).set_duration(5)
    audio = AudioFileClip(audio_path)
    video = clip.set_audio(audio)
    video_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4()}.mp4")
    video.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", verbose=False, logger=None)
    return video_path

@app.post("/generate-meme")
async def generate_meme(request: MemeRequest):
    image_path = generate_absurd_image(request.text)
    audio_path = generate_voice(request.text)
    video_path = create_video(image_path, audio_path)
    return {"video_url": f"/video/{os.path.basename(video_path)}"}

@app.get("/video/{video_filename}")
async def get_video(video_filename: str):
    video_path = os.path.join(OUTPUT_DIR, video_filename)
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    return Response(status_code=404)
