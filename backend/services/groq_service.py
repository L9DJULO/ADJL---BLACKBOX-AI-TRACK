import os
from groq import Groq
from typing import Dict, Any, List

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
    async def accelerate_inference(self, model_name: str, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        """Utilise Groq pour accélérer l'inférence des modèles"""
        try:
            # Groq optimise l'exécution des modèles comme Llama
            response = self.client.chat.completions.create(
                model=model_name,  # "llama3-70b-8192" ou "llama3-8b-8192"
                messages=[
                    {"role": "system", "content": "Tu es un assistant de code intelligent."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.3,
                top_p=0.9,
                stream=False
            )
            
            return {
                "success": True,
                "content": response.choices[0].message.content,
                "model": model_name,
                "usage": response.usage._asdict() if response.usage else None
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def analyze_code_intent(self, voice_command: str, code_context: str) -> Dict[str, Any]:
        """Analyse l'intention de la commande vocale avec Llama via Groq"""
        
        prompt = f"""
        Analyse cette commande vocale dans le contexte du code donné:
        
        Commande: {voice_command}
        Contexte du code: {code_context}
        
        Réponds en JSON avec:
        {{
            "action": "create|modify|delete|refactor|test|document",
            "target": "fonction|classe|variable|commentaire",
            "description": "description détaillée de ce qui doit être fait",
            "confidence": 0.0-1.0
        }}
        """
        
        result = await self.accelerate_inference("llama3-70b-8192", prompt, 500)
        return result