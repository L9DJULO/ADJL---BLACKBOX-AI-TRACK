# from fastapi import FastAPI, File, UploadFile, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from services.ai_orchestrator import AIOrchestrator
# from services.speech_service import SpeechService
# from services.git_service import GitService
# import os
# from dotenv import load_dotenv
# import time

# load_dotenv()

# app = FastAPI(title="AI Voice Code Assistant", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Services
# ai_orchestrator = AIOrchestrator()
# speech_service = SpeechService()
# git_service = GitService()

# @app.post("/api/voice-command")
# async def process_voice_command(
#     audio: UploadFile = File(...),
#     code_context: str = Form(...),
#     file_path: str = Form(...),
#     project_path: str = Form(...)
# ):
#     try:
#         # 1. Transcription vocale
#         audio_bytes = await audio.read()
#         transcription = await speech_service.transcribe_audio(audio_bytes)
        
#         # 2. Traitement avec tous les services AI
#         ai_results = await ai_orchestrator.process_voice_command(
#             command=transcription,
#             context=code_context,
#             file_path=file_path
#         )
        
#         # 3. Création branche Git
#         branch_name = f"ai-modification-{int(time.time())}"
#         git_result = await git_service.create_branch(project_path, branch_name)
        
#         return {
#             "success": True,
#             "transcription": transcription,
#             "ai_analysis": ai_results,
#             "branch_name": branch_name,
#             "git_status": git_result,
#             "services_used": ["blackbox", "groq", "llama", "coral"]
#         }
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/api/models/status")
# async def get_models_status():
#     """Vérifier le statut de tous les modèles"""
#     return {
#         "blackbox": "available",
#         "groq": "available", 
#         "llama": "loading" if not ai_orchestrator.llama.model else "ready",
#         "coral": "available"
#     }




# REFAIRE TOUT CA EN PRENANT LE TEXT DIRECT A LA PLACE DE L'UPLOAD DU FICHIER AUDIO