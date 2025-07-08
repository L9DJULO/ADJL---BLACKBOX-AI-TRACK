import asyncio
from typing import Dict, Any, List
from .blackbox_service import BlackboxService
from .coral_service import CoralService
from .fetch_service import FetchService
from .groq_service import GroqService
from .llama_service import LlamaService
import logging

logger = logging.getLogger(__name__)

class AIOrchestrator:
    def __init__(self):
        self.blackbox = BlackboxService()
        self.coral = CoralService()
        self.fetch = FetchService()
        self.groq = GroqService()
        self.llama = LlamaService()
    
    async def process_text_command(self, command: str, context: str = None, 
                                  file_content: str = None) -> Dict[str, Any]:
        """
        Traite une commande texte en orchestrant les différents services AI
        """
        try:
            # 1. Analyse de la commande avec Coral Protocol
            coral_analysis = await self.coral.analyze_command(command, context)
            
            # 2. Déterminer le service principal selon le type de commande
            command_type = coral_analysis.get('type', 'code_analysis')
            
            if command_type == 'code_generation':
                return await self._handle_code_generation(command, context, file_content)
            elif command_type == 'code_analysis':
                return await self._handle_code_analysis(command, context, file_content)
            elif command_type == 'refactoring':
                return await self._handle_refactoring(command, context, file_content)
            elif command_type == 'debugging':
                return await self._handle_debugging(command, context, file_content)
            else:
                return await self._handle_general_query(command, context, file_content)
                
        except Exception as e:
            logger.error(f"Erreur dans l'orchestrateur: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_code_generation(self, command: str, context: str, 
                                    file_content: str) -> Dict[str, Any]:
        """Génération de code avec BLACKBOX.AI comme service principal"""
        try:
            # BLACKBOX.AI pour la génération (obligatoire)
            blackbox_result = await self.blackbox.generate_code(command, context)
            
            # Fetch.AI pour optimisation et suggestions
            fetch_optimization = await self.fetch.optimize_code(
                blackbox_result.get('code', ''), command
            )
            
            # Coral pour coordination et validation
            coral_validation = await self.coral.validate_solution(
                blackbox_result, fetch_optimization
            )
            
            return {
                'success': True,
                'type': 'code_generation',
                'primary_result': blackbox_result,
                'optimization': fetch_optimization,
                'validation': coral_validation,
                'metadata': {
                    'services_used': ['blackbox', 'fetch', 'coral'],
                    'primary_service': 'blackbox'
                }
            }
        except Exception as e:
            logger.error(f"Erreur génération de code: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_code_analysis(self, command: str, context: str, 
                                   file_content: str) -> Dict[str, Any]:
        """Analyse de code avec coordination multi-agents"""
        try:
            # BLACKBOX.AI pour l'analyse principale
            blackbox_analysis = await self.blackbox.analyze_code(file_content, command)
            
            # Groq pour analyse rapide complémentaire
            groq_analysis = await self.groq.quick_analysis(file_content, command)
            
            # Coral pour synthèse et priorisation
            coral_synthesis = await self.coral.synthesize_analysis(
                blackbox_analysis, groq_analysis
            )
            
            return {
                'success': True,
                'type': 'code_analysis',
                'primary_analysis': blackbox_analysis,
                'quick_analysis': groq_analysis,
                'synthesis': coral_synthesis,
                'metadata': {
                    'services_used': ['blackbox', 'groq', 'coral'],
                    'primary_service': 'blackbox'
                }
            }
        except Exception as e:
            logger.error(f"Erreur analyse de code: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_refactoring(self, command: str, context: str, 
                                 file_content: str) -> Dict[str, Any]:
        """Refactoring avec BLACKBOX.AI et optimisation Fetch.AI"""
        try:
            # BLACKBOX.AI pour le refactoring principal
            blackbox_refactor = await self.blackbox.refactor_code(file_content, command)
            
            # Fetch.AI pour suggestions d'amélioration
            fetch_improvements = await self.fetch.suggest_improvements(
                file_content, blackbox_refactor.get('refactored_code', '')
            )
            
            # Llama pour validation des bonnes pratiques
            llama_validation = await self.llama.validate_best_practices(
                blackbox_refactor.get('refactored_code', ''), context
            )
            
            return {
                'success': True,
                'type': 'refactoring',
                'refactored_code': blackbox_refactor,
                'improvements': fetch_improvements,
                'validation': llama_validation,
                'metadata': {
                    'services_used': ['blackbox', 'fetch', 'llama'],
                    'primary_service': 'blackbox'
                }
            }
        except Exception as e:
            logger.error(f"Erreur refactoring: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_debugging(self, command: str, context: str, 
                               file_content: str) -> Dict[str, Any]:
        """Débogage avec analyse multi-agents"""
        try:
            # BLACKBOX.AI pour détection de bugs
            blackbox_debug = await self.blackbox.debug_code(file_content, command)
            
            # Groq pour analyse rapide des erreurs
            groq_errors = await self.groq.detect_errors(file_content)
            
            # Coral pour priorisation des corrections
            coral_priorities = await self.coral.prioritize_fixes(
                blackbox_debug, groq_errors
            )
            
            return {
                'success': True,
                'type': 'debugging',
                'debug_analysis': blackbox_debug,
                'error_detection': groq_errors,
                'fix_priorities': coral_priorities,
                'metadata': {
                    'services_used': ['blackbox', 'groq', 'coral'],
                    'primary_service': 'blackbox'
                }
            }
        except Exception as e:
            logger.error(f"Erreur débogage: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _handle_general_query(self, command: str, context: str, 
                                   file_content: str) -> Dict[str, Any]:
        """Requête générale avec distribution intelligente"""
        try:
            # Fetch.AI pour compréhension de l'intention
            fetch_intent = await self.fetch.understand_intent(command, context)
            
            # BLACKBOX.AI pour réponse technique
            blackbox_response = await self.blackbox.general_query(command, context)
            
            # Coral pour orchestration de la réponse
            coral_orchestration = await self.coral.orchestrate_response(
                fetch_intent, blackbox_response
            )
            
            return {
                'success': True,
                'type': 'general_query',
                'intent': fetch_intent,
                'response': blackbox_response,
                'orchestration': coral_orchestration,
                'metadata': {
                    'services_used': ['fetch', 'blackbox', 'coral'],
                    'primary_service': 'blackbox'
                }
            }
        except Exception as e:
            logger.error(f"Erreur requête générale: {e}")
            return {'success': False, 'error': str(e)}