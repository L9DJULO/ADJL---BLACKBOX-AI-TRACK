import os
import json
import logging
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import io
from typing import Dict, Any, Optional
import requests
from groq import Groq
import soundfile as sf
import librosa
import numpy as np

logger = logging.getLogger(__name__)

class SpeechService:
    """Service for processing voice commands and text-to-speech"""
    
    def __init__(self):
        self.groq_client = None
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        if self.groq_api_key:
            self.groq_client = Groq(api_key=self.groq_api_key)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate microphone
        self._calibrate_microphone()
        
        # Voice command patterns
        self.command_patterns = {
            'analyze_code': ['analyze', 'review', 'check', 'examine'],
            'generate_code': ['generate', 'create', 'write', 'build'],
            'refactor_code': ['refactor', 'improve', 'optimize', 'clean'],
            'generate_tests': ['test', 'unit test', 'testing', 'tests'],
            'generate_docs': ['document', 'documentation', 'docs', 'comment'],
            'fix_bugs': ['fix', 'debug', 'solve', 'repair'],
            'explain_code': ['explain', 'describe', 'what does', 'how does']
        }
    
    def is_available(self) -> bool:
        """Check if speech service is available"""
        return bool(self.groq_api_key)
    
    def _calibrate_microphone(self):
        """Calibrate microphone for ambient noise"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone calibrated for ambient noise")
        except Exception as e:
            logger.error(f"Failed to calibrate microphone: {e}")
    
    def listen_for_command(self, timeout: int = 5) -> Dict[str, Any]:
        """Listen for voice command from microphone"""
        try:
            with self.microphone as source:
                logger.info("Listening for voice command...")
                audio = self.recognizer.listen(source, timeout=timeout)
                
            # Convert speech to text
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Voice command recognized: {text}")
            
            # Process command
            command_info = self._process_voice_command(text)
            
            return {
                "text": text,
                "command": command_info,
                "success": True
            }
            
        except sr.WaitTimeoutError:
            return {"error": "No speech detected within timeout", "success": False}
        except sr.UnknownValueError:
            return {"error": "Could not understand audio", "success": False}
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return {"error": f"Speech recognition service error: {e}", "success": False}
        except Exception as e:
            logger.error(f"Unexpected error in voice command: {e}")
            return {"error": str(e), "success": False}
    
    def process_audio_file(self, audio_data: bytes) -> Dict[str, Any]:
        """Process audio file and extract voice command"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # Load audio with speech_recognition
            with sr.AudioFile(temp_file_path) as source:
                audio = self.recognizer.record(source)
            
            # Convert to text
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Audio file processed: {text}")
            
            # Clean up
            os.unlink(temp_file_path)
            
            # Process command
            command_info = self._process_voice_command(text)
            
            return {
                "text": text,
                "command": command_info,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            return {"error": str(e), "success": False}
    
    def _process_voice_command(self, text: str) -> Dict[str, Any]:
        """Process voice command text to extract intent and parameters"""
        text_lower = text.lower()
        
        # Find matching command
        for command, patterns in self.command_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return {
                    "action": command,
                    "original_text": text,
                    "confidence": 0.8,
                    "parameters": self._extract_parameters(text, command)
                }
        
        # If no direct match, use AI to understand the command
        return self._ai_command_understanding(text)
    
    def _extract_parameters(self, text: str, command: str) -> Dict[str, Any]:
        """Extract parameters from voice command"""
        params = {}
        text_lower = text.lower()
        
        # Language detection
        languages = ['python', 'javascript', 'java', 'c++', 'c#', 'go', 'rust', 'php', 'ruby']
        for lang in languages:
            if lang in text_lower:
                params['language'] = lang
                break
        
        # File type detection
        if 'function' in text_lower:
            params['target'] = 'function'
        elif 'class' in text_lower:
            params['target'] = 'class'
        elif 'file' in text_lower:
            params['target'] = 'file'
        
        # Specific instructions
        if 'performance' in text_lower:
            params['focus'] = 'performance'
        elif 'security' in text_lower:
            params['focus'] = 'security'
        elif 'readability' in text_lower:
            params['focus'] = 'readability'
        
        return params
    
    def _ai_command_understanding(self, text: str) -> Dict[str, Any]:
        """Use AI to understand unclear voice commands"""
        if not self.groq_client:
            return {
                "action": "unknown",
                "original_text": text,
                "confidence": 0.0,
                "parameters": {}
            }
        
        try:
            prompt = f"""
            Analyze this voice command and determine what coding action the user wants:
            
            Voice command: "{text}"
            
            Possible actions:
            - analyze_code: Review and analyze code
            - generate_code: Create new code
            - refactor_code: Improve existing code
            - generate_tests: Create unit tests
            - generate_docs: Create documentation
            - fix_bugs: Debug and fix issues
            - explain_code: Explain how code works
            
            Return JSON with: action, confidence (0-1), and parameters (language, target, focus).
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            result["original_text"] = text
            return result
            
        except Exception as e:
            logger.error(f"AI command understanding error: {e}")
            return {
                "action": "unknown",
                "original_text": text,
                "confidence": 0.0,
                "parameters": {},
                "error": str(e)
            }
    
    def text_to_speech(self, text: str, voice: str = "en-US-1") -> bytes:
        """Convert text to speech audio"""
        try:
            # Use a TTS service or generate audio
            # For demo purposes, we'll return a simple response
            logger.info(f"Converting text to speech: {text[:50]}...")
            
            # In a real implementation, you would use a TTS service
            # For now, we'll return an empty audio file
            return b""
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return b""
    
    def get_voice_feedback(self, result: Dict[str, Any]) -> str:
        """Generate voice feedback based on operation result"""
        if result.get("success"):
            action = result.get("action", "operation")
            return f"Successfully completed {action}. The result is ready."
        else:
            error = result.get("error", "unknown error")
            return f"Sorry, there was an error: {error}. Please try again."
    
    def continuous_listening(self, callback_function, stop_event):
        """Continuously listen for voice commands"""
        logger.info("Starting continuous voice listening...")
        
        while not stop_event.is_set():
            try:
                result = self.listen_for_command(timeout=2)
                if result.get("success"):
                    callback_function(result)
                
            except KeyboardInterrupt:
                logger.info("Stopping continuous listening...")
                break
            except Exception as e:
                logger.error(f"Error in continuous listening: {e}")
                
        logger.info("Continuous listening stopped")
    
    def process_voice_command_with_context(self, text: str, code_context: str, language: str) -> Dict[str, Any]:
        """Process voice command with code context for better understanding"""
        try:
            if not self.groq_client:
                return self._process_voice_command(text)
            
            prompt = f"""
            Given this voice command and code context, determine the exact action needed:
            
            Voice command: "{text}"
            Code language: {language}
            Code context: {code_context[:500]}...
            
            Based on the context, what specific action should be taken?
            Return JSON with: action, confidence, parameters, and specific_instructions.
            """
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=300
            )
            
            result = json.loads(response.choices[0].message.content)
            result["original_text"] = text
            return result
            
        except Exception as e:
            logger.error(f"Context-aware command processing error: {e}")
            return self._process_voice_command(text)