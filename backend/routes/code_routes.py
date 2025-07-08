from flask import Blueprint, request, jsonify
from models.request_models import CodeAnalysisRequest, TextCommandRequest
from services.ai_orchestrator import AIOrchestrator
import asyncio
import logging

logger = logging.getLogger(__name__)
code_bp = Blueprint('code', __name__)
orchestrator = AIOrchestrator()

@code_bp.route('/analyze', methods=['POST'])
def analyze_code():
    """Analyse de code avec orchestration AI"""
    try:
        data = request.get_json()
        
        # Validation des données
        analysis_request = CodeAnalysisRequest(**data)
        
        # Traitement asynchrone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.process_text_command(
                f"Analyze this {analysis_request.language} code: {analysis_request.analysis_type}",
                analysis_request.context,
                analysis_request.code
            )
        )
        loop.close()
        
        return jsonify({
            'success': True,
            'analysis_type': analysis_request.analysis_type,
            'language': analysis_request.language,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Erreur analyse code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@code_bp.route('/command', methods=['POST'])
def process_command():
    """Traitement de commande texte"""
    try:
        data = request.get_json()
        
        # Validation des données
        command_request = TextCommandRequest(**data)
        
        # Traitement asynchrone
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.process_text_command(
                command_request.command,
                command_request.context,
                command_request.file_content
            )
        )
        loop.close()
        
        return jsonify({
            'success': True,
            'command': command_request.command,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Erreur traitement commande: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@code_bp.route('/generate', methods=['POST'])
def generate_code():
    """Génération de code"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        language = data.get('language', 'python')
        context = data.get('context', '')
        
        # Traitement avec orchestrateur
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.process_text_command(
                f"Generate {language} code: {prompt}",
                context,
                None
            )
        )
        loop.close()
        
        return jsonify({
            'success': True,
            'language': language,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Erreur génération code: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@code_bp.route('/refactor', methods=['POST'])
def refactor_code():
    """Refactoring de code"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        instructions = data.get('instructions', 'Refactor this code')
        context = data.get('context', '')
        
        # Traitement avec orchestrateur
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(
            orchestrator.process_text_command(
                f"Refactor: {instructions}",
                context,