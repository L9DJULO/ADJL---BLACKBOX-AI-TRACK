from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any

class LlamaService:
    def __init__(self):
        self.model_name = "meta-llama/Llama-2-7b-chat-hf"  # ou Llama-3 si disponible
        self.tokenizer = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    async def load_model(self):
        """Charge le modèle Llama (une seule fois)"""
        if self.model is None:
            print("Chargement du modèle Llama...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto"
            )
            print("Modèle Llama chargé avec succès")
    
    async def generate_code_explanation(self, code: str, question: str) -> Dict[str, Any]:
        """Génère une explication du code avec Llama"""
        await self.load_model()
        
        prompt = f"""
        [INST] Explique ce code et réponds à la question:
        
        Code: {code}
        Question: {question}
        
        Réponds de manière concise et technique. [/INST]
        """
        
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=300,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extraire seulement la réponse (après [/INST])
            response = response.split("[/INST]")[-1].strip()
            
            return {
                "success": True,
                "explanation": response,
                "model": self.model_name
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }