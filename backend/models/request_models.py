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