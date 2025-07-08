import aiohttp
import asyncio
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class BlackboxService:
    def __init__(self):
        self.api_key = "YOUR_BLACKBOX_API_KEY"  # À configurer
        self.base_url = "https://api.blackbox.ai"
        self.session = None
    
    async def _get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def generate_code(self, prompt: str, context: str = None) -> Dict[str, Any]:
        """Génération de code avec BLACKBOX.AI"""
        try:
            session = await self._get_session()
            
            payload = {
                "prompt": prompt,
                "context": context or "",
                "mode": "code_generation",
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{self.base_url}/v1/code/generate",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'code': data.get('code', ''),
                        'explanation': data.get('explanation', ''),
                        'language': data.get('language', 'unknown'),
                        'confidence': data.get('confidence', 0.8)
                    }
                else:
                    return {
                        'success': False,
                        'error': f"BLACKBOX API Error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Erreur BLACKBOX génération: {e}")
            return {'success': False, 'error': str(e)}
    
    async def analyze_code(self, code: str, query: str = None) -> Dict[str, Any]:
        """Analyse de code avec BLACKBOX.AI"""
        try:
            session = await self._get_session()
            
            payload = {
                "code": code,
                "query": query or "Analyze this code",
                "mode": "code_analysis",
                "include_suggestions": True,
                "include_security": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{self.base_url}/v1/code/analyze",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'analysis': data.get('analysis', {}),
                        'suggestions': data.get('suggestions', []),
                        'issues': data.get('issues', []),
                        'security_concerns': data.get('security_concerns', []),
                        'complexity_score': data.get('complexity_score', 0)
                    }
                else:
                    return {
                        'success': False,
                        'error': f"BLACKBOX API Error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Erreur BLACKBOX analyse: {e}")
            return {'success': False, 'error': str(e)}
    
    async def refactor_code(self, code: str, instructions: str) -> Dict[str, Any]:
        """Refactoring avec BLACKBOX.AI"""
        try:
            session = await self._get_session()
            
            payload = {
                "code": code,
                "instructions": instructions,
                "mode": "refactoring",
                "preserve_functionality": True,
                "optimize_performance": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{self.base_url}/v1/code/refactor",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'refactored_code': data.get('refactored_code', ''),
                        'changes': data.get('changes', []),
                        'improvements': data.get('improvements', []),
                        'diff': data.get('diff', '')
                    }
                else:
                    return {
                        'success': False,
                        'error': f"BLACKBOX API Error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Erreur BLACKBOX refactoring: {e}")
            return {'success': False, 'error': str(e)}
    
    async def debug_code(self, code: str, error_description: str = None) -> Dict[str, Any]:
        """Débogage avec BLACKBOX.AI"""
        try:
            session = await self._get_session()
            
            payload = {
                "code": code,
                "error_description": error_description or "Find and fix bugs",
                "mode": "debugging",
                "include_fixes": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{self.base_url}/v1/code/debug",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'bugs_found': data.get('bugs_found', []),
                        'fixes': data.get('fixes', []),
                        'fixed_code': data.get('fixed_code', ''),
                        'severity_levels': data.get('severity_levels', {})
                    }
                else:
                    return {
                        'success': False,
                        'error': f"BLACKBOX API Error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Erreur BLACKBOX débogage: {e}")
            return {'success': False, 'error': str(e)}
    
    async def general_query(self, query: str, context: str = None) -> Dict[str, Any]:
        """Requête générale avec BLACKBOX.AI"""
        try:
            session = await self._get_session()
            
            payload = {
                "query": query,
                "context": context or "",
                "mode": "general",
                "include_code_examples": True
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with session.post(
                f"{self.base_url}/v1/chat",
                json=payload,
                headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'success': True,
                        'response': data.get('response', ''),
                        'code_examples': data.get('code_examples', []),
                        'related_topics': data.get('related_topics', [])
                    }
                else:
                    return {
                        'success': False,
                        'error': f"BLACKBOX API Error: {response.status}"
                    }
                    
        except Exception as e:
            logger.error(f"Erreur BLACKBOX requête générale: {e}")
            return {'success': False, 'error': str(e)}
    
    async def close(self):
        """Fermeture de la session"""
        if self.session:
            await self.session.close()
