from fastapi import FastAPI, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from services.ai_orchestrator import AIOrchestrator
from services.git_service import GitService
from models.request_models import (
    VoiceCommandResponse, 
    ServiceStatus, CommandType
)
from typing import Dict, List
import os
from dotenv import load_dotenv
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="AI Voice Code Assistant",
    version="1.0.0",
    description="Intelligent code assistant powered by BLACKBOX.AI, Groq, Llama, Coral, and Fetch.ai"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
ai_orchestrator = AIOrchestrator()
git_service = GitService()

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "status": "running",
        "service": "AI Voice Code Assistant",
        "version": "1.0.0"
    }

@app.post("/api/voice-command", response_model=VoiceCommandResponse)
async def process_voice_command(
    command: str = Form(..., description="Voice command text"),
    code_context: str = Form(..., description="Current code context"),
    file_path: str = Form(..., description="Path to the file being edited"),
    project_path: str = Form(..., description="Root project path")
):
    """
    Process a voice command with all AI services
    
    This endpoint:
    1. Analyzes the command intent
    2. Fetches external data if needed
    3. Generates code using BLACKBOX.AI
    4. Creates a Git branch for changes
    """
    try:
        start_time = time.time()
        
        logger.info(f"Processing voice command: {command}")
        
        # Process with AI orchestrator
        ai_results = await ai_orchestrator.process_voice_command(
            command=command,
            context=code_context,
            file_path=file_path
        )
        
        # Determine command type from intent analysis
        command_type = CommandType.GENERATE  # Default
        if ai_results.get("intent_analysis", {}).get("success"):
            intent_content = ai_results["intent_analysis"].get("content", "")
            # Parse the intent content (it might be a JSON string)
            try:
                import json
                if isinstance(intent_content, str):
                    intent_data = json.loads(intent_content)
                else:
                    intent_data = intent_content
                    
                action = intent_data.get("action", "generate")
                command_type_map = {
                    "analyze": CommandType.ANALYZE,
                    "generate": CommandType.GENERATE,
                    "refactor": CommandType.REFACTOR,
                    "test": CommandType.TEST,
                    "document": CommandType.DOCUMENT,
                    "fix": CommandType.FIX,
                    "optimize": CommandType.OPTIMIZE
                }
                command_type = command_type_map.get(action, CommandType.GENERATE)
            except:
                # If parsing fails, keep default
                pass
        
        # Create Git branch for the changes
        branch_name = f"ai-{command_type.value}-{int(time.time())}"
        generated_code = ai_results.get("code_generation", {}).get("code", "")
        
        # Only create branch if we have generated code
        git_result = {}
        if generated_code:
            git_result = git_service.create_branch_and_commit(
                repo_path=project_path,
                branch_name=branch_name,
                file_path=file_path,
                new_content=generated_code,
                commit_message=f"AI: {command[:50]}..."
            )
        else:
            git_result = {"success": False, "error": "No code generated"}
        
        execution_time = time.time() - start_time
        
        return VoiceCommandResponse(
            success=True,
            transcription=command,
            command_type=command_type,
            ai_analysis=ai_results,
            branch_name=branch_name if git_result.get("success") else None,
            git_status=git_result,
            services_used=["blackbox", "groq", "llama", "coral", "fetch"],
            execution_time=execution_time
        )
        
    except Exception as e:
        logger.error(f"Error processing voice command: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/models/status")
async def get_models_status() -> List[ServiceStatus]:
    """Check the status of all AI models and services"""
    try:
        statuses = []
        
        # Check each service
        services_status = await ai_orchestrator.get_service_status()
        
        for service_name, status in services_status.items():
            statuses.append(ServiceStatus(
                service_name=service_name,
                status=status,
                last_check=time.strftime("%Y-%m-%d %H:%M:%S")
            ))
        
        # Check Git service
        statuses.append(ServiceStatus(
            service_name="git",
            status="ready" if git_service.is_available() else "error",
            last_check=time.strftime("%Y-%m-%d %H:%M:%S")
        ))
        
        return statuses
        
    except Exception as e:
        logger.error(f"Error checking models status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-code")
async def analyze_code(
    code: str = Form(...),
    language: str = Form(default="python")
):
    """Analyze code for bugs, security issues, and improvements"""
    try:
        # Use BLACKBOX.AI for code analysis
        blackbox_service = ai_orchestrator.blackbox
        result = blackbox_service.analyze_code(code, language)
        
        return {
            "success": True,
            "analysis": result,
            "service": "blackbox_ai"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-tests")
async def generate_tests(
    code: str = Form(...),
    language: str = Form(default="python")
):
    """Generate unit tests for the provided code"""
    try:
        blackbox_service = ai_orchestrator.blackbox
        result = blackbox_service.generate_tests(code, language)
        
        return {
            "success": True,
            "tests": result,
            "service": "blackbox_ai"
        }
        
    except Exception as e:
        logger.error(f"Error generating tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refactor-code")
async def refactor_code(
    code: str = Form(...),
    language: str = Form(default="python"),
    instructions: str = Form(default="Improve code quality and readability")
):
    """Refactor code based on best practices"""
    try:
        blackbox_service = ai_orchestrator.blackbox
        result = blackbox_service.refactor_code(code, language, instructions)
        
        return {
            "success": True,
            "refactored_code": result,
            "service": "blackbox_ai"
        }
        
    except Exception as e:
        logger.error(f"Error refactoring code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/git/analyze-changes")
async def analyze_git_changes(
    repo_path: str = Form(...),
    file_path: str = Form(default=None)
):
    """Analyze Git repository changes"""
    try:
        result = git_service.analyze_code_changes(repo_path, file_path)
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing Git changes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include additional routers
from routes.fetch_routes import router as fetch_router
app.include_router(fetch_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting AI Voice Code Assistant...")
    
    # Pre-load Llama model if available
    if os.getenv('LLAMA_PRELOAD', 'false').lower() == 'true':
        logger.info("Pre-loading Llama model...")
        try:
            await ai_orchestrator.llama.load_model()
        except Exception as e:
            logger.warning(f"Failed to load Llama model: {e}")
    
    # Connect to Coral Protocol
    if ai_orchestrator.coral.is_available():
        logger.info("Connecting to Coral Protocol...")
        try:
            await ai_orchestrator.coral.connect()
        except Exception as e:
            logger.warning(f"Failed to connect to Coral: {e}")
    
    logger.info("AI Voice Code Assistant started successfully!")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down AI Voice Code Assistant...")
    
    # Disconnect from Coral
    if ai_orchestrator.coral.is_available():
        try:
            await ai_orchestrator.coral.disconnect()
        except Exception as e:
            logger.warning(f"Error disconnecting from Coral: {e}")
    
    # Cleanup Git temporary directories
    git_service.cleanup_temp_dirs()
    
    logger.info("AI Voice Code Assistant shut down successfully!")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )