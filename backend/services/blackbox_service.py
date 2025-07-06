import os
import requests
import json
import logging
from typing import Dict, List, Optional, Any
from groq import Groq

logger = logging.getLogger(__name__)

class BlackboxService:
    """Service for integrating BLACKBOX.AI with Groq acceleration"""
    
    def __init__(self):
        self.blackbox_api_key = os.getenv('BLACKBOX_API_KEY')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.blackbox_url = "https://api.blackbox.ai/v1"
        
        # Initialize Groq client for fast inference
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
        else:
            self.groq_client = None
            
        # Blackbox headers
        self.headers = {
            'Authorization': f'Bearer {self.blackbox_api_key}',
            'Content-Type': 'application/json'
        }
    
    def is_available(self) -> bool:
        """Check if the service is available"""
        return bool(self.blackbox_api_key)
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Analyze code using BLACKBOX.AI"""
        try:
            payload = {
                "code": code,
                "language": language,
                "tasks": [
                    "analyze",
                    "find_bugs",
                    "suggest_improvements",
                    "security_check",
                    "performance_optimization"
                ]
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/analyze",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Blackbox API error: {response.status_code}")
                return self._fallback_analysis(code, language)
                
        except Exception as e:
            logger.error(f"Error analyzing code: {e}")
            return self._fallback_analysis(code, language)
    
    # FIX: Nouvelle méthode pour correspondre à l'usage dans ai_orchestrator
    async def generate_code(self, command: str, context: str, analysis: Dict[str, Any] = None, external_data: Dict[str, Any] = None, language: str = "python") -> Dict[str, Any]:
        """Generate code using BLACKBOX.AI with enhanced context"""
        try:
            # Construire le prompt enrichi
            enhanced_prompt = self._build_enhanced_prompt(command, context, analysis, external_data)
            
            payload = {
                "prompt": enhanced_prompt,
                "language": language,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "code": result.get("code", ""),
                    "explanation": result.get("explanation", ""),
                    "source": "blackbox_ai"
                }
            else:
                return await self._fallback_generation(enhanced_prompt, language)
                
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return await self._fallback_generation(command, language)
    
    def _build_enhanced_prompt(self, command: str, context: str, analysis: Dict[str, Any] = None, external_data: Dict[str, Any] = None) -> str:
        """Build enhanced prompt with all available context"""
        prompt_parts = [f"Commande: {command}"]
        
        if context:
            prompt_parts.append(f"Contexte du code existant:\n{context}")
        
        if analysis and analysis.get("success"):
            intent = analysis.get("content", "")
            prompt_parts.append(f"Analyse de l'intention:\n{intent}")
        
        if external_data:
            # Ajouter les données externes pertinentes
            if external_data.get("documentation", {}).get("success"):
                doc_content = external_data["documentation"].get("content", "")[:500]
                prompt_parts.append(f"Documentation pertinente:\n{doc_content}")
            
            if external_data.get("examples", {}).get("success"):
                examples = external_data["examples"].get("examples", [])
                if examples:
                    example_content = examples[0].get("content", "")[:300]
                    prompt_parts.append(f"Exemple de code similaire:\n{example_content}")
        
        return "\n\n".join(prompt_parts)
    
    def generate_code_basic(self, prompt: str, language: str = "python") -> Dict[str, Any]:
        """Generate code using BLACKBOX.AI - basic version"""
        try:
            payload = {
                "prompt": prompt,
                "language": language,
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/generate",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_generation(prompt, language)
                
        except Exception as e:
            logger.error(f"Error generating code: {e}")
            return self._fallback_generation(prompt, language)
    
    def refactor_code(self, code: str, language: str = "python", instructions: str = "") -> Dict[str, Any]:
        """Refactor code using BLACKBOX.AI"""
        try:
            payload = {
                "code": code,
                "language": language,
                "instructions": instructions or "Refactor this code to improve readability and performance",
                "preserve_functionality": True
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/refactor",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_refactor(code, language, instructions)
                
        except Exception as e:
            logger.error(f"Error refactoring code: {e}")
            return self._fallback_refactor(code, language, instructions)
    
    def generate_tests(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Generate tests using BLACKBOX.AI"""
        try:
            payload = {
                "code": code,
                "language": language,
                "test_framework": "pytest" if language == "python" else "auto",
                "coverage_target": 80
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/tests",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_tests(code, language)
                
        except Exception as e:
            logger.error(f"Error generating tests: {e}")
            return self._fallback_tests(code, language)
    
    def generate_documentation(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Generate documentation using BLACKBOX.AI"""
        try:
            payload = {
                "code": code,
                "language": language,
                "format": "markdown",
                "include_examples": True
            }
            
            response = requests.post(
                f"{self.blackbox_url}/code/documentation",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._fallback_documentation(code, language)
                
        except Exception as e:
            logger.error(f"Error generating documentation: {e}")
            return self._fallback_documentation(code, language)
    
    def _fallback_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Fallback analysis using Groq + Llama"""
        if not self.groq_client:
            return {"error": "No analysis service available"}
        
        try:
            prompt = f"""
            Analyze this {language} code and provide:
            1. Code quality assessment
            2. Potential bugs or issues
            3. Security vulnerabilities
            4. Performance improvements
            5. Best practices suggestions
            
            Code:
            ```{language}
            {code}
            ```
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "analysis": response.choices[0].message.content,
                "source": "groq_llama",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Fallback analysis error: {e}")
            return {"error": "Analysis failed", "success": False}
    
    async def _fallback_generation(self, prompt: str, language: str) -> Dict[str, Any]:
        """Fallback code generation using Groq + Llama"""
        if not self.groq_client:
            return {"error": "No generation service available", "success": False}
        
        try:
            full_prompt = f"""
            Generate {language} code for the following request:
            {prompt}
            
            Provide only the code with proper formatting and comments.
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": full_prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            
            return {
                "code": response.choices[0].message.content,
                "source": "groq_llama",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Fallback generation error: {e}")
            return {"error": "Generation failed", "success": False}
    
    def _fallback_refactor(self, code: str, language: str, instructions: str) -> Dict[str, Any]:
        """Fallback refactoring using Groq + Llama"""
        if not self.groq_client:
            return {"error": "No refactoring service available"}
        
        try:
            prompt = f"""
            Refactor this {language} code following these instructions: {instructions}
            
            Original code:
            ```{language}
            {code}
            ```
            
            Provide the refactored code with explanations of changes made.
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "refactored_code": response.choices[0].message.content,
                "source": "groq_llama",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Fallback refactor error: {e}")
            return {"error": "Refactoring failed", "success": False}
    
    def _fallback_tests(self, code: str, language: str) -> Dict[str, Any]:
        """Fallback test generation using Groq + Llama"""
        if not self.groq_client:
            return {"error": "No test generation service available"}
        
        try:
            prompt = f"""
            Generate comprehensive unit tests for this {language} code:
            
            ```{language}
            {code}
            ```
            
            Use appropriate testing framework and include edge cases.
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "tests": response.choices[0].message.content,
                "source": "groq_llama",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Fallback tests error: {e}")
            return {"error": "Test generation failed", "success": False}
    
    def _fallback_documentation(self, code: str, language: str) -> Dict[str, Any]:
        """Fallback documentation generation using Groq + Llama"""
        if not self.groq_client:
            return {"error": "No documentation service available"}
        
        try:
            prompt = f"""
            Generate comprehensive documentation for this {language} code:
            
            ```{language}
            {code}
            ```
            
            Include:
            - Function/class descriptions
            - Parameters and return values
            - Usage examples
            - Implementation notes
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=1000
            )
            
            return {
                "documentation": response.choices[0].message.content,
                "source": "groq_llama",
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Fallback documentation error: {e}")
            return {"error": "Documentation generation failed", "success": False}