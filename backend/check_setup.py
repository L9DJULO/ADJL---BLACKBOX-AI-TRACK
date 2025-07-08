#!/usr/bin/env python3
"""
Script pour vérifier que tout est correctement configuré
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Vérifie si un fichier existe"""
    exists = os.path.exists(filepath)
    status = "✅" if exists else ("❌" if required else "⚠️")
    print(f"{status} {filepath} - {'Exists' if exists else 'Missing'}")
    return exists

def check_imports():
    """Vérifie que les imports fonctionnent"""
    print("\n🔍 Checking imports...")
    
    try:
        from models.request_models import VoiceCommandResponse, ServiceStatus, CommandType
        print("✅ Model imports OK")
    except ImportError as e:
        print(f"❌ Model import error: {e}")
        return False
    
    try:
        from services.ai_orchestrator import AIOrchestrator
        print("✅ AIOrchestrator import OK")
    except ImportError as e:
        print(f"❌ AIOrchestrator import error: {e}")
        return False
    
    try:
        from routes.fetch_routes import router
        print("✅ Fetch routes import OK")
    except ImportError as e:
        print(f"❌ Fetch routes import error: {e}")
        return False
    
    return True

def check_env():
    """Vérifie le fichier .env"""
    print("\n🔍 Checking environment...")
    
    if not check_file_exists(".env"):
        print("💡 Create .env from .env.example")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_keys = ["BLACKBOX_API_KEY", "GROQ_API_KEY"]
    missing = []
    
    for key in required_keys:
        if not os.getenv(key):
            missing.append(key)
    
    if missing:
        print(f"❌ Missing required env vars: {', '.join(missing)}")
        return False
    else:
        print("✅ Required environment variables set")
        return True

def main():
    print("🚀 AI Voice Code Assistant - Setup Check\n")
    
    # Check required files
    print("📁 Checking required files...")
    files_ok = all([
        check_file_exists("app.py"),
        check_file_exists("models/request_models.py"),
        check_file_exists("services/ai_orchestrator.py"),
        check_file_exists("services/blackbox_service.py"),
        check_file_exists("services/groq_service.py"),
        check_file_exists("services/llama_service.py"),
        check_file_exists("services/coral_service.py"),
        check_file_exists("services/fetch_service.py"),
        check_file_exists("services/git_service.py"),
        check_file_exists("routes/fetch_routes.py"),
    ])
    
    # Check imports
    imports_ok = check_imports()
    
    # Check environment
    env_ok = check_env()
    
    # Summary
    print("\n" + "="*50)
    if files_ok and imports_ok and env_ok:
        print("✅ Everything looks good! You can run: python app.py")
    else:
        print("❌ Some issues need to be fixed before running the app")
        print("\nNext steps:")
        if not files_ok:
            print("- Check missing files")
        if not imports_ok:
            print("- Fix import errors")
        if not env_ok:
            print("- Configure .env file")

if __name__ == "__main__":
    main()