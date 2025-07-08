from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class CodeLanguage(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"

class AnalysisType(str, Enum):
    CODE_REVIEW = "code_review"
    REFACTOR = "refactor"
    OPTIMIZE = "optimize"
    DEBUG = "debug"
    DOCUMENTATION = "documentation"
    TESTS = "tests"
    SECURITY = "security"

class CommandType(str, Enum):
    """Types de commandes supportées"""
    ANALYZE = "analyze"
    GENERATE = "generate"
    REFACTOR = "refactor"
    TEST = "test"
    DOCUMENT = "document"
    FIX = "fix"
    OPTIMIZE = "optimize"

class CodeAnalysisRequest(BaseModel):
    code: str = Field(..., description="Code à analyser")
    language: CodeLanguage = Field(..., description="Langage de programmation")
    analysis_type: AnalysisType = Field(..., description="Type d'analyse demandée")
    context: Optional[str] = Field(None, description="Contexte additionnel")
    file_path: Optional[str] = Field(None, description="Chemin du fichier")

class TextCommandRequest(BaseModel):
    command: str = Field(..., description="Commande texte de l'utilisateur")
    context: Optional[str] = Field(None, description="Contexte du projet")
    file_content: Optional[str] = Field(None, description="Contenu du fichier si applicable")
    language: Optional[CodeLanguage] = Field(None, description="Langage détecté")

class VoiceCommandRequest(BaseModel):
    """Modèle pour les commandes vocales (converties en texte)"""
    command: str = Field(..., description="Commande vocale transcrite")
    code_context: str = Field(..., description="Contexte du code actuel")
    file_path: str = Field(..., description="Chemin du fichier en cours d'édition")
    project_path: str = Field(..., description="Chemin racine du projet")

class FileUploadRequest(BaseModel):
    file_content: str = Field(..., description="Contenu du fichier")
    file_name: str = Field(..., description="Nom du fichier")
    file_type: str = Field(..., description="Type/extension du fichier")

class AIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None

class ServiceStatus(BaseModel):
    """Statut d'un service AI"""
    service_name: str = Field(..., description="Nom du service")
    status: str = Field(..., description="Statut: ready, loading, error")
    last_check: Optional[str] = Field(default=None)
    error_message: Optional[str] = Field(default=None)

class VoiceCommandResponse(BaseModel):
    """Réponse pour une commande vocale"""
    success: bool = Field(..., description="Succès de l'opération")
    transcription: str = Field(..., description="Transcription de la commande")
    command_type: CommandType = Field(..., description="Type de commande détecté")
    ai_analysis: Dict[str, Any] = Field(..., description="Résultats de l'analyse AI")
    branch_name: Optional[str] = Field(default=None, description="Branche Git créée")
    git_status: Optional[Dict[str, Any]] = Field(default=None)
    services_used: List[str] = Field(..., description="Services AI utilisés")
    execution_time: Optional[float] = Field(default=None)

class AIServiceResponse(BaseModel):
    """Réponse générique d'un service AI"""
    success: bool = Field(..., description="Statut de succès")
    result: Dict[str, Any] = Field(..., description="Résultat du service")
    source: str = Field(..., description="Service qui a fourni le résultat")
    timestamp: Optional[str] = Field(default=None)
    error: Optional[str] = Field(default=None)