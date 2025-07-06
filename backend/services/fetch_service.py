import os
import json
import asyncio
import aiohttp
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class FetchService:
    """Service for integrating with Fetch.ai network"""
    
    def __init__(self):
        self.fetch_api_key = os.getenv('FETCH_API_KEY')
        self.fetch_network_url = os.getenv('FETCH_NETWORK_URL', 'https://api.fetch.ai/v1')
        self.agent_registry = {}
        self.session = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    'Authorization': f'Bearer {self.fetch_api_key}',
                    'Content-Type': 'application/json'
                }
            )
        return self.session
    
    async def deploy_agent(self, code: str, name: str, description: str = None) -> Dict[str, Any]:
        """Deploy a new Fetch.ai agent"""
        try:
            session = await self._get_session()
            
            payload = {
                "name": name,
                "code": code,
                "description": description or f"AI Code Assistant Agent: {name}",
                "skills": ["code_analysis", "code_generation", "collaboration"],
                "resources": {
                    "memory": "512MB",
                    "cpu": "0.5"
                }
            }
            
            async with session.post(
                f"{self.fetch_network_url}/agents/deploy",
                json=payload
            ) as response:
                
                if response.status == 201:
                    result = await response.json()
                    agent_id = result.get('agent_id')
                    
                    # Store in local registry
                    self.agent_registry[agent_id] = {
                        "name": name,
                        "deployed_at": datetime.now().isoformat(),
                        "status": "active"
                    }
                    
                    return {
                        "agent_id": agent_id,
                        "status": "deployed",
                        "endpoint": result.get('endpoint'),
                        "message": f"Agent {name} deployed successfully"
                    }
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error deploying agent: {e}")
            return {"error": str(e), "success": False}
    
    async def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get status of a deployed agent"""
        try:
            session = await self._get_session()
            
            async with session.get(
                f"{self.fetch_network_url}/agents/{agent_id}/status"
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    
                    # Update local registry
                    if agent_id in self.agent_registry:
                        self.agent_registry[agent_id]["last_check"] = datetime.now().isoformat()
                        self.agent_registry[agent_id]["status"] = result.get("status", "unknown")
                    
                    return result
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error getting agent status: {e}")
            return {"error": str(e), "success": False}
    
    async def communicate_with_agent(self, agent_id: str, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Send message to a Fetch.ai agent"""
        try:
            session = await self._get_session()
            
            payload = {
                "message": message,
                "context": context,
                "timestamp": datetime.now().isoformat()
            }
            
            async with session.post(
                f"{self.fetch_network_url}/agents/{agent_id}/communicate",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "response": result.get("response"),
                        "agent_id": agent_id,
                        "timestamp": result.get("timestamp"),
                        "success": True
                    }
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error communicating with agent: {e}")
            return {"error": str(e), "success": False}
    
    async def search_network_resources(self, query: str, resource_type: str, max_results: int = 10) -> Dict[str, Any]:
        """Search Fetch.ai network for resources"""
        try:
            session = await self._get_session()
            
            params = {
                "q": query,
                "type": resource_type,
                "limit": max_results
            }
            
            async with session.get(
                f"{self.fetch_network_url}/search",
                params=params
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "resources": result.get("results", []),
                        "total": result.get("total", 0),
                        "query": query,
                        "type": resource_type,
                        "success": True
                    }
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error searching network: {e}")
            return {"error": str(e), "success": False}
    
    async def fetch_data_for_command(self, command: str, context: str, sources: List[str] = None) -> Dict[str, Any]:
        """Fetch external data to enhance command processing"""
        sources = sources or ["documentation", "examples", "packages", "solutions"]
        results = {}
        
        # Execute searches concurrently
        tasks = []
        for source in sources:
            if source == "documentation":
                tasks.append(self._fetch_documentation(command, context))
            elif source == "examples":
                tasks.append(self._fetch_code_examples(command, context))
            elif source == "packages":
                tasks.append(self._fetch_package_info(command, context))
            elif source == "solutions":
                tasks.append(self._fetch_solutions(command, context))
        
        # Wait for all tasks to complete
        try:
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(task_results):
                source = sources[i] if i < len(sources) else f"source_{i}"
                if isinstance(result, Exception):
                    results[source] = {"error": str(result), "success": False}
                else:
                    results[source] = result
                    
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            results["error"] = str(e)
        
        return results
    
    async def _fetch_documentation(self, command: str, context: str) -> Dict[str, Any]:
        """Fetch relevant documentation"""
        try:
            session = await self._get_session()
            
            # Extract potential library/framework names from command and context
            search_terms = self._extract_search_terms(command, context)
            
            async with session.get(
                f"{self.fetch_network_url}/docs/search",
                params={"q": " ".join(search_terms), "limit": 5}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "docs": result.get("docs", []),
                        "content": result.get("content", ""),
                        "sources": result.get("sources", [])
                    }
                else:
                    return {"success": False, "error": "Documentation not found"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _fetch_code_examples(self, command: str, context: str) -> Dict[str, Any]:
        """Fetch code examples"""
        try:
            session = await self._get_session()
            
            search_terms = self._extract_search_terms(command, context)
            
            async with session.get(
                f"{self.fetch_network_url}/examples/search",
                params={"q": " ".join(search_terms), "limit": 3}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "examples": result.get("examples", []),
                        "total": result.get("total", 0)
                    }
                else:
                    return {"success": False, "error": "Examples not found"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _fetch_package_info(self, command: str, context: str) -> Dict[str, Any]:
        """Fetch package information"""
        try:
            session = await self._get_session()
            
            # Extract package names from command
            potential_packages = self._extract_package_names(command, context)
            
            if not potential_packages:
                return {"success": False, "error": "No packages identified"}
            
            package_info = {}
            for package in potential_packages[:3]:  # Limit to 3 packages
                async with session.get(
                    f"{self.fetch_network_url}/packages/{package}"
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        package_info[package] = result
            
            return {
                "success": True,
                "packages": package_info,
                "count": len(package_info)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _fetch_solutions(self, command: str, context: str) -> Dict[str, Any]:
        """Fetch solutions from community"""
        try:
            session = await self._get_session()
            
            search_query = f"{command} {context}"[:100]  # Limit query length
            
            async with session.get(
                f"{self.fetch_network_url}/solutions/search",
                params={"q": search_query, "limit": 5}
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "solutions": result.get("solutions", []),
                        "total": result.get("total", 0)
                    }
                else:
                    return {"success": False, "error": "Solutions not found"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _extract_search_terms(self, command: str, context: str) -> List[str]:
        """Extract relevant search terms from command and context"""
        import re
        
        # Common programming terms and patterns
        programming_terms = re.findall(r'\b(?:import|from|class|def|function|method|api|library|framework|package)\s+(\w+)', 
                                     command.lower() + " " + context.lower())
        
        # Extract quoted terms
        quoted_terms = re.findall(r'["\']([^"\']+)["\']', command + " " + context)
        
        # Extract capitalized words (likely library names)
        capitalized_words = re.findall(r'\b[A-Z][a-z]+\b', command + " " + context)
        
        # Combine all terms
        all_terms = programming_terms + quoted_terms + capitalized_words
        
        # Remove duplicates and return
        return list(set(term.lower() for term in all_terms if len(term) > 2))
    
    def _extract_package_names(self, command: str, context: str) -> List[str]:
        """Extract potential package names"""
        import re
        
        # Common package patterns
        patterns = [
            r'\bimport\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bfrom\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'\bpip\s+install\s+([a-zA-Z_][a-zA-Z0-9_-]*)',
            r'\bnpm\s+install\s+([a-zA-Z_][a-zA-Z0-9_-]*)',
        ]
        
        packages = []
        full_text = command + " " + context
        
        for pattern in patterns:
            matches = re.findall(pattern, full_text.lower())
            packages.extend(matches)
        
        return list(set(packages))
    
    async def list_available_agents(self) -> Dict[str, Any]:
        """List available agents on the network"""
        try:
            session = await self._get_session()
            
            async with session.get(
                f"{self.fetch_network_url}/agents"
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "agents": result.get("agents", []),
                        "total": result.get("total", 0)
                    }
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error listing agents: {e}")
            return {"error": str(e), "success": False}
    
    async def request_collaboration(self, task: str, skills: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """Request collaboration from network agents"""
        try:
            session = await self._get_session()
            
            payload = {
                "task": task,
                "required_skills": skills,
                "context": context,
                "max_agents": 3,
                "timeout": 300  # 5 minutes
            }
            
            async with session.post(
                f"{self.fetch_network_url}/collaboration/request",
                json=payload
            ) as response:
                
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "collaboration_id": result.get("collaboration_id"),
                        "participating_agents": result.get("agents", []),
                        "estimated_time": result.get("estimated_time")
                    }
                else:
                    return await self._handle_error(response)
                    
        except Exception as e:
            logger.error(f"Error requesting collaboration: {e}")
            return {"error": str(e), "success": False}
    
    async def _handle_error(self, response: aiohttp.ClientResponse) -> Dict[str, Any]:
        """Handle API errors"""
        try:
            error_data = await response.json()
            return {
                "error": error_data.get("message", "Unknown error"),
                "status_code": response.status,
                "success": False
            }
        except:
            return {
                "error": f"HTTP {response.status}",
                "status_code": response.status,
                "success": False
            }
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

# Global function for easy access
async def fetch_data_for_command(command: str, context: str, sources: List[str] = None) -> Dict[str, Any]:
    """Global function to fetch data for command enhancement"""
    fetch_service = FetchService()
    try:
        return await fetch_service.fetch_data_for_command(command, context, sources)
    finally:
        await fetch_service.close()