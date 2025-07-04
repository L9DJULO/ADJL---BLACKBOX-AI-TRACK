from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .api import router as api_router

# Chargement des settings
settings = get_settings()

app = FastAPI(
    title="AI Backend API",
    description="Backend API pour interroger GrokCloud, Llama et BlackBox",
    version="1.0.0",
)

# CORS pour permettre les appels depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Point de test
@app.get("/")
def root():
    return {"message": "API backend opérationnelle."}

# Inclusion des routes dans /api
app.include_router(api_router, prefix="/api")
