import aiohttp
import asyncio
from typing import Dict, Any, List, Optional
import json
import os
from urllib.parse import urljoin, urlparse

class FetchService:
    """Service pour récupérer des données externes (APIs, documentation, exemples de code)"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'AI-Voice-Code-Assistant/1.0',
            'Accept': 'application/json, text/plain, */*'
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_api_documentation(self, api_name: str, endpoint: str = None) -> Dict[str, Any]:
        """Récupère la documentation d'une API"""
        
        api_docs = {
            "github": "https://docs.github.com/en/rest",
            "openai": "https://platform.openai.com/docs/api-reference",
            "fastapi": "https://fastapi.tiangolo.com/",
            "react": "https://react.dev/reference/react",
            "python": "https://docs.python.org/3/library/",
        }
        
        if api_name.lower() not in api_docs:
            return {"error": f"Documentation pour {api_name} non disponible"}
        
        url = api_docs[api_name.lower()]
        if endpoint:
            url = urljoin(url, endpoint)
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    return {
                        "success": True,
                        "url": url,
                        "content": content[:5000],  # Limiter pour éviter overflow
                        "status": response.status
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}",
                        "url": url
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url
            }
    
    async def fetch_code_examples(self, language: str, topic: str) -> Dict[str, Any]:
        """Récupère des exemples de code depuis GitHub ou autres sources"""
        
        # GitHub API pour chercher des exemples
        search_url = f"https://api.github.com/search/code"
        params = {
            "q": f"{topic} language:{language}",
            "sort": "indexed",
            "per_page": 5
        }
        
        try:
            async with self.session.get(search_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    examples = []
                    
                    for item in data.get("items", [])[:3]:  # Limiter à 3 exemples
                        # Récupérer le contenu du fichier
                        file_content = await self.fetch_file_content(item["url"])
                        examples.append({
                            "name": item["name"],
                            "repository": item["repository"]["full_name"],
                            "url": item["html_url"],
                            "content": file_content.get("content", "")[:1000]  # Limiter
                        })
                    
                    return {
                        "success": True,
                        "examples": examples,
                        "total_count": data.get("total_count", 0)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"GitHub API error: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fetch_file_content(self, api_url: str) -> Dict[str, Any]:
        """Récupère le contenu d'un fichier depuis l'API GitHub"""
        try:
            async with self.session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    # Décoder le contenu base64
                    import base64
                    content = base64.b64decode(data["content"]).decode("utf-8")
                    return {
                        "success": True,
                        "content": content,
                        "size": data["size"]
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def fetch_npm_package_info(self, package_name: str) -> Dict[str, Any]:
        """Récupère les informations d'un package NPM"""
        url = f"https://registry.npmjs.org/{package_name}"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "name": data.get("name"),
                        "version": data.get("dist-tags", {}).get("latest"),
                        "description": data.get("description"),
                        "homepage": data.get("homepage"),
                        "repository": data.get("repository", {}).get("url"),
                        "dependencies": list(data.get("versions", {}).get(
                            data.get("dist-tags", {}).get("latest", ""), {}
                        ).get("dependencies", {}).keys())[:10]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Package {package_name} non trouvé"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fetch_python_package_info(self, package_name: str) -> Dict[str, Any]:
        """Récupère les informations d'un package Python depuis PyPI"""
        url = f"https://pypi.org/pypi/{package_name}/json"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    info = data.get("info", {})
                    return {
                        "success": True,
                        "name": info.get("name"),
                        "version": info.get("version"),
                        "description": info.get("summary"),
                        "homepage": info.get("home_page"),
                        "docs_url": info.get("docs_url"),
                        "requires_python": info.get("requires_python"),
                        "keywords": info.get("keywords", "").split(",")[:5]
                    }
                else:
                    return {
                        "success": False,
                        "error": f"Package {package_name} non trouvé"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fetch_stackoverflow_solutions(self, query: str) -> Dict[str, Any]:
        """Récupère des solutions depuis StackOverflow API"""
        url = "https://api.stackexchange.com/2.3/search/advanced"
        params = {
            "order": "desc",
            "sort": "votes",
            "q": query,
            "site": "stackoverflow",
            "pagesize": 3,
            "filter": "withbody"
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    solutions = []
                    
                    for item in data.get("items", []):
                        solutions.append({
                            "title": item.get("title"),
                            "score": item.get("score"),
                            "answer_count": item.get("answer_count"),
                            "url": item.get("link"),
                            "tags": item.get("tags", []),
                            "body": item.get("body", "")[:500]  # Limiter
                        })
                    
                    return {
                        "success": True,
                        "solutions": solutions,
                        "total": data.get("total", 0)
                    }
                else:
                    return {
                        "success": False,
                        "error": f"StackOverflow API error: {response.status}"
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def fetch_best_practices(self, language: str, topic: str) -> Dict[str, Any]:
        """Récupère les meilleures pratiques pour un langage/sujet"""
        
        # Sources de meilleures pratiques
        sources = {
            "python": [
                "https://pep8.org/",
                "https://docs.python-guide.org/",
            ],
            "javascript": [
                "https://javascript.info/",
                "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            ],
            "typescript": [
                "https://www.typescriptlang.org/docs/",
            ]
        }
        
        language_sources = sources.get(language.lower(), [])
        if not language_sources:
            return {
                "success": False,
                "error": f"Meilleures pratiques pour {language} non disponibles"
            }
        
        # Récupérer depuis la première source
        url = language_sources[0]
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text()
                    return {
                        "success": True,
                        "language": language,
                        "topic": topic,
                        "source": url,
                        "content": content[:3000]  # Limiter
                    }
                else:
                    return {
                        "success": False,
                        "error": f"HTTP {response.status}",
                        "url": url
                    }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Fonction utilitaire pour utiliser le service
async def fetch_data_for_command(command: str, context: str) -> Dict[str, Any]:
    """Fonction principale pour récupérer des données selon la commande"""
    
    async with FetchService() as fetch_service:
        results = {}
        
        # Analyser la commande pour déterminer quoi récupérer
        command_lower = command.lower()
        
        if "documentation" in command_lower or "docs" in command_lower:
            # Extraire le nom de l'API/librairie
            for api in ["github", "openai", "fastapi", "react", "python"]:
                if api in command_lower:
                    results["documentation"] = await fetch_service.fetch_api_documentation(api)
                    break
        
        if "example" in command_lower or "exemple" in command_lower:
            # Détecter le langage depuis le contexte
            language = detect_language_from_context(context)
            topic = extract_topic_from_command(command)
            results["examples"] = await fetch_service.fetch_code_examples(language, topic)
        
        if "package" in command_lower or "library" in command_lower:
            package_name = extract_package_name(command)
            if package_name:
                language = detect_language_from_context(context)
                if language == "python":
                    results["package_info"] = await fetch_service.fetch_python_package_info(package_name)
                elif language in ["javascript", "typescript"]:
                    results["package_info"] = await fetch_service.fetch_npm_package_info(package_name)
        
        if "stackoverflow" in command_lower or "solution" in command_lower:
            query = extract_search_query(command)
            results["solutions"] = await fetch_service.fetch_stackoverflow_solutions(query)
        
        if "best practice" in command_lower or "bonne pratique" in command_lower:
            language = detect_language_from_context(context)
            topic = extract_topic_from_command(command)
            results["best_practices"] = await fetch_service.fetch_best_practices(language, topic)
        
        return results

def detect_language_from_context(context: str) -> str:
    """Détecte le langage de programmation depuis le contexte"""
    if "def " in context or "import " in context:
        return "python"
    elif "function" in context or "const" in context or "let" in context:
        return "javascript"
    elif "interface" in context or "type" in context:
        return "typescript"
    elif "public class" in context:
        return "java"
    return "python"  # default

def extract_topic_from_command(command: str) -> str:
    """Extrait le sujet principal de la commande"""
    # Mots-clés techniques courants
    keywords = ["api", "database", "authentication", "validation", "testing", "async", "promise"]
    for keyword in keywords:
        if keyword in command.lower():
            return keyword
    return "general"

def extract_package_name(command: str) -> str:
    """Extrait le nom du package de la commande"""
    # Logique simple pour extraire le nom du package
    words = command.split()
    for i, word in enumerate(words):
        if word.lower() in ["package", "library", "module"] and i + 1 < len(words):
            return words[i + 1]
    return ""

def extract_search_query(command: str) -> str:
    """Extrait la requête de recherche de la commande"""
    # Supprimer les mots de commande pour garder le sujet
    stop_words = ["cherche", "trouve", "search", "find", "stackoverflow", "solution"]
    words = [word for word in command.split() if word.lower() not in stop_words]
    return " ".join(words)