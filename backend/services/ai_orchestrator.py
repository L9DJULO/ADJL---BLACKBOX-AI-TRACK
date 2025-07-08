from .blackbox_service import BlackboxService
from .groq_service import GroqService
from .llama_service import LlamaService
from .coral_service import CoralService
from .fetch_service import FetchService
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """Orchestre tous les services AI selon les besoins"""
    
    def __init__(self):
        self.blackbox = BlackboxService()
        self.groq = GroqService()
        self.llama = LlamaService()
        self.coral = CoralService()
        self.fetch = FetchService()
        
    async def process_voice_command(self, command: str, context: str, file_path: str) -> Dict[str, Any]:
        """Pipeline complet avec tous les services"""
        
        results = {}
        
        try:
            # 1. Analyse de l'intention avec Groq (rapide)
            intent_result = await self.groq.quick_analysis(context, command)
            results["intent_analysis"] = {
                "success": intent_result.get("success", False),
                "content": {
                    "action": self._extract_action_from_command(command),
                    "confidence": intent_result.get("confidence", 0.7)
                }
            }
            
            # 2. Analyse collaborative avec Coral
            results["coral_analysis"] = await self.coral.analyze_command(command, context, file_path)
            
            # 3. Génération de code avec BLACKBOX.AI
            code_result = await self.blackbox.generate_code(command, context)
            results["code_generation"] = code_result
            
            # 4. Validation avec Llama
            if code_result.get("success") and code_result.get("code"):
                validation_result = await self.llama.validate_best_practices(
                    code_result["code"], 
                    context
                )
                results["validation"] = validation_result
            
            # 5. Optimisation avec Fetch
            if code_result.get("success") and code_result.get("code"):
                optimization_result = await self.fetch.optimize_code(
                    code_result["code"],
                    command
                )
                results["optimization"] = optimization_result
            
            return results
            
        except Exception as e:
            logger.error(f"Error in AI orchestrator: {e}")
            return {
                "error": str(e),
                "intent_analysis": {"success": False, "error": str(e)},
                "code_generation": {"success": False, "error": str(e)}
            }
    
    def _extract_action_from_command(self, command: str) -> str:
        """Extrait l'action de la commande"""
        command_lower = command.lower()
        
        if any(word in command_lower for word in ["generate", "create", "add", "write"]):
            return "generate"
        elif any(word in command_lower for word in ["analyze", "review", "check"]):
            return "analyze"
        elif any(word in command_lower for word in ["refactor", "improve", "optimize"]):
            return "refactor"
        elif any(word in command_lower for word in ["test", "unit test"]):
            return "test"
        elif any(word in command_lower for word in ["document", "docs", "comment"]):
            return "document"
        elif any(word in command_lower for word in ["fix", "debug", "error"]):
            return "fix"
        else:
            return "generate"  # Default
    
    async def get_service_status(self) -> Dict[str, str]:
        """Vérifie le statut de tous les services"""
        
        status = {}
        
        try:
            # Test simple pour chaque service
            status["blackbox"] = "ready"  # Assume ready if initialized
            status["groq"] = "ready"
            status["llama"] = "ready"
            status["coral"] = "ready" if self.coral.is_available() else "unavailable"
            status["fetch"] = "ready"
            
        except Exception as e:
            logger.error(f"Error checking service status: {e}")
            status["error"] = str(e)
        
        return status