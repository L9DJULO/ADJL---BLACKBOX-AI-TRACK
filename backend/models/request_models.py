from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class CommandType(str, Enum):
    ANALYZE = "analyze"
    GENERATE = "generate"
    REFACTOR = "refactor"
    TEST = "test"
    DOCUMENT = "document"
    FIX = "fix"
    OPTIMIZE = "optimize"

class Language(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"

class VoiceCommandRequest(BaseModel):
    command: str = Field(..., description="Voice command transcribed")
    context: str = Field(..., description="Current code context")
    file_path: str = Field(..., description="Path to the file being edited")
    project_path: str = Field(..., description="Root project path")
    language: Language = Field(default=Language.PYTHON, description="Programming language")
    
class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code to analyze")
    language: Language = Field(default=Language.PYTHON)
    analysis_type: List[str] = Field(default=["bugs", "security", "performance"])
    
class CodeGenerationRequest(BaseModel):
    prompt: str = Field(..., description="Generation prompt")
    language: Language = Field(default=Language.PYTHON)
    context: Optional[str] = Field(default="", description="Additional context")
    max_tokens: int = Field(default=1000, ge=100, le=2000)
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)

class RefactorRequest(BaseModel):
    code: str = Field(..., description="Code to refactor")
    language: Language = Field(default=Language.PYTHON)
    instructions: str = Field(default="Improve code quality and readability")
    preserve_functionality: bool = Field(default=True)

class TestGenerationRequest(BaseModel):
    code: str = Field(..., description="Code to generate tests for")
    language: Language = Field(default=Language.PYTHON)
    test_framework: Optional[str] = Field(default=None)
    coverage_target: int = Field(default=80, ge=50, le=100)

class DocumentationRequest(BaseModel):
    code: str = Field(..., description="Code to document")
    language: Language = Field(default=Language.PYTHON)
    format: str = Field(default="markdown")
    include_examples: bool = Field(default=True)

class AIServiceResponse(BaseModel):
    success: bool = Field(..., description="Success status")
    result: Dict[str, Any] = Field(..., description="Service result")
    source: str = Field(..., description="Service that provided the result")
    timestamp: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)

class VoiceCommandResponse(BaseModel):
    success: bool = Field(..., description="Overall success")
    transcription: str = Field(..., description="Voice transcription")
    command_type: CommandType = Field(..., description="Detected command type")
    ai_analysis: Dict[str, Any] = Field(..., description="AI analysis results")
    branch_name: Optional[str] = Field(default=None, description="Git branch created")
    git_status: Optional[Dict[str, str]] = Field(default=None)
    services_used: List[str] = Field(..., description="AI services used")
    execution_time: Optional[float] = Field(default=None)
    
class ServiceStatus(BaseModel):
    service_name: str = Field(..., description="Name of the service")
    status: str = Field(..., description="Status: ready, loading, error")
    last_check: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

class ProjectInfo(BaseModel):
    name: str = Field(..., description="Project name")
    path: str = Field(..., description="Project path")
    language: Language = Field(..., description="Main language")
    files: List[str] = Field(default=[], description="Project files")
    git_status: Optional[Dict[str, Any]] = Field(default=None)