#!/usr/bin/env python3
"""
Script de lancement rapide pour le serveur FastAPI
"""

import uvicorn
import os

if __name__ == "__main__":
    # Créer le dossier output s'il n'existe pas
    os.makedirs("output", exist_ok=True)
    
    print("🚀 Lancement du serveur FastAPI...")
    print("📍 Backend accessible sur: http://localhost:8000")
    print("📖 Documentation API: http://localhost:8000/docs")
    print("🛑 Arrêter avec Ctrl+C")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
