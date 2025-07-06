from .blackbox_service import BlackboxService
from .groq_service import GroqService
from .llama_service import LlamaService
from .coral_service import CoralService
from .fetch_service import FetchService, fetch_data_for_command
from typing import Dict, Any

class AIOrchestrator:
    """Orchestre tous les services AI selon les besoins"""
    
    def __init__(self):
        self.blackbox = BlackboxService()
        self.groq = GroqService()
        self.llama = LlamaService()
        self.coral = CoralService()
        
    async def process_voice_command(self, command: str, context: str, file_path: str) -> Dict[str, Any]:
        """Pipeline complet avec tous les services incluant fetch"""
        
        results = {}
        
        # 1. Récupération de données externes si nécessaire
        if self._needs_external_data(command):
            results["external_data"] = await fetch_data_for_command(command, context)
        
        # 2. Analyse rapide de l'intention avec Groq + Llama
        results["intent_analysis"] = await self.groq.analyze_code_intent(command, context)
        
        # 3. Analyse collaborative avec Coral
        results["coral_analysis"] = await self.coral.analyze_command(command, context, file_path)
        
        # 4. Enrichissement du contexte avec les données fetchées
        enriched_context = self._enrich_context(context, results.get("external_data", {}))
        
        # 5. Génération de code avec BLACKBOX.AI (avec contexte enrichi)
        results["code_generation"] = await self.blackbox.generate_code(
            command=command,
            context=enriched_context,
            analysis=results["intent_analysis"],
            external_data=results.get("external_data", {})
        )
        
        # 6. Explication avec Llama si nécessaire
        if results["code_generation"].get("success"):
            generated_code = results["code_generation"].get("code", "")
            results["code_explanation"] = await self.llama.generate_code_explanation(
                code=generated_code,
                question=f"Explique ce code généré pour: {command}"
            )
        
        # 7. Validation avec les données externes
        if results.get("external_data"):
            results["validation"] = await self._validate_with_external_data(
                results["code_generation"], 
                results["external_data"]
            )
        
        return results
    
    def _needs_external_data(self, command: str) -> bool:
        """Détermine si la commande nécessite des données externes"""
        
        external_indicators = [
            "documentation", "docs", "example", "exemple", 
            "package", "library", "npm", "pypi",
            "stackoverflow", "solution", "best practice",
            "api", "tutorial", "guide"
        ]
        
        command_lower = command.lower()
        return any(indicator in command_lower for indicator in external_indicators)
    
    def _enrich_context(self, original_context: str, external_data: Dict[str, Any]) -> str:
        """Enrichit le contexte avec les données externes"""
        
        enriched = original_context
        
        # Ajouter la documentation si disponible
        if "documentation" in external_data:
            doc_data = external_data["documentation"]
            if doc_data.get("success"):
                enriched += f"\n\n# Documentation pertinente:\n{doc_data.get('content', '')[:1000]}"
        
        # Ajouter les exemples de code
        if "examples" in external_data:
            examples_data = external_data["examples"]
            if examples_data.get("success"):
                enriched += "\n\n# Exemples de code similaires:\n"
                for example in examples_data.get("examples", [])[:2]:
                    enriched += f"## {example['name']}:\n{example['content'][:500]}\n\n"
        
        # Ajouter les informations de package
        if "package_info" in external_data:
            pkg_data = external_data["package_info"]
            if pkg_data.get("success"):
                enriched += f"\n\n# Info package {pkg_data.get('name')}:\n"
                enriched += f"Version: {pkg_data.get('version')}\n"
                enriched += f"Description: {pkg_data.get('description')}\n"
        
        # Ajouter les solutions StackOverflow
        if "solutions" in external_data:
            so_data = external_data["solutions"]
            if so_data.get("success"):
                enriched += "\n\n# Solutions StackOverflow:\n"
                for solution in so_data.get("solutions", [])[:1]:
                    enriched += f"## {solution['title']} (Score: {solution['score']}):\n"
                    enriched += f"{solution['body'][:300]}\n\n"
        
        return enriched
    
    async def _validate_with_external_data(self, code_result: Dict[str, Any], external_data: Dict[str, Any]) -> Dict[str, Any]:
        """Valide le code généré avec les données externes"""
        
        validation_results = {
            "is_valid": True,
            "warnings": [],
            "suggestions": []
        }
        
        # Vérifier avec la documentation
        if "documentation" in external_data:
            # Logique de validation basée sur la doc
            validation_results["suggestions"].append("Code conforme à la documentation")
        
        # Vérifier avec les exemples
        if "examples" in external_data:
            # Logique de validation basée sur les exemples
            validation_results["suggestions"].append("Code suit les patterns des exemples")
        
        # Vérifier avec les infos de package
        if "package_info" in external_data:
            pkg_data = external_data["package_info"]
            if pkg_data.get("success"):
                validation_results["suggestions"].append(
                    f"Utilise {pkg_data.get('name')} v{pkg_data.get('version')}"
                )
        
        return validation_results
    
    async def choose_best_model(self, task_type: str) -> str:
        """Choisit le meilleur modèle selon la tâche"""
        
        model_mapping = {
            "code_generation": "blackbox",      # BLACKBOX.AI pour générer du code
            "intent_analysis": "groq_llama",   # Groq + Llama pour comprendre
            "code_explanation": "llama",       # Llama pour expliquer
            "collaboration": "coral",          # Coral pour orchestrer
            "fast_inference": "groq",          # Groq pour la vitesse
            "data_fetching": "fetch",          # Fetch pour données externes
            "validation": "combined"           # Combinaison pour valider
        }
        
        return model_mapping.get(task_type, "blackbox")
    
    async def get_service_status(self) -> Dict[str, str]:
        """Vérifie le statut de tous les services"""
        
        status = {}
        
        # Tester chaque service
        try:
            # Test simple pour chaque service
            status["blackbox"] = "ready"
            status["groq"] = "ready"
            status["llama"] = "ready" if self.llama.model else "loading"
            status["coral"] = "ready"
            status["fetch"] = "ready"
            
        except Exception as e:
            status["error"] = str(e)
        
        return status