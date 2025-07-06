import os
import json
import logging
import asyncio
import websockets
from typing import Dict, List, Optional, Any
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)

class CoralService:
    """Service for integrating Coral Protocol for decentralized AI collaboration"""
    
    def __init__(self):
        self.coral_api_key = os.getenv('CORAL_API_KEY')
        self.coral_endpoint = os.getenv('CORAL_ENDPOINT', 'wss://coral.protocol.ai/v1')
        self.node_id = os.getenv('CORAL_NODE_ID', 'ai-code-assistant')
        self.session_id = None
        self.websocket = None
        self.active_agents = {}
        
        # Initialize async session
        self.session = None
    
    def is_available(self) -> bool:
        """Check if Coral service is available"""
        return bool(self.coral_api_key)
    
    async def connect(self):
        """Connect to Coral Protocol network"""
        try:
            if not self.coral_api_key:
                logger.warning("Coral API key not provided")
                return False
            
            # Initialize async session
            self.session = aiohttp.ClientSession()
            
            # Connect to Coral websocket
            headers = {
                'Authorization': f'Bearer {self.coral_api_key}',
                'X-Node-ID': self.node_id
            }
            
            self.websocket = await websockets.connect(
                self.coral_endpoint,
                extra_headers=headers
            )
            
            # Register node
            await self._register_node()
            
            logger.info("Connected to Coral Protocol network")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Coral: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Coral Protocol network"""
        try:
            if self.websocket:
                await self.websocket.close()
            if self.session:
                await self.session.close()
            logger.info("Disconnected from Coral Protocol network")
        except Exception as e:
            logger.error(f"Error disconnecting from Coral: {e}")
    
    async def _register_node(self):
        """Register this node in the Coral network"""
        registration_data = {
            "type": "register",
            "node_id": self.node_id,
            "capabilities": [
                "code_analysis",
                "code_generation",
                "code_refactoring",
                "test_generation",
                "documentation_generation"
            ],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.websocket.send(json.dumps(registration_data))
        response = await self.websocket.recv()
        response_data = json.loads(response)
        
        if response_data.get("status") == "success":
            self.session_id = response_data.get("session_id")
            logger.info(f"Node registered with session ID: {self.session_id}")
        else:
            logger.error(f"Node registration failed: {response_data}")
    
    async def create_agent_collaboration(self, task: str, code: str, language: str) -> Dict[str, Any]:
        """Create a collaboration session with multiple AI agents"""
        try:
            if not self.websocket:
                await self.connect()
            
            collaboration_request = {
                "type": "create_collaboration",
                "session_id": self.session_id,
                "task": task,
                "context": {
                    "code": code,
                    "language": language,
                    "timestamp": datetime.utcnow().isoformat()
                },
                "required_agents": [
                    "code_analyzer",
                    "security_auditor",
                    "performance_optimizer",
                    "documentation_generator"
                ]
            }
            
            await self.websocket.send(json.dumps(collaboration_request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("status") == "success":
                collaboration_id = response_data.get("collaboration_id")
                return await self._monitor_collaboration(collaboration_id)
            else:
                logger.error(f"Collaboration creation failed: {response_data}")
                return {"error": "Failed to create collaboration", "success": False}
                
        except Exception as e:
            logger.error(f"Error creating agent collaboration: {e}")
            return {"error": str(e), "success": False}
    
    async def _monitor_collaboration(self, collaboration_id: str) -> Dict[str, Any]:
        """Monitor collaboration progress and collect results"""
        results = {
            "collaboration_id": collaboration_id,
            "agents_results": {},
            "status": "in_progress",
            "start_time": datetime.utcnow().isoformat()
        }
        
        timeout = 60  # 60 seconds timeout
        start_time = datetime.utcnow()
        
        try:
            while (datetime.utcnow() - start_time).seconds < timeout:
                response = await asyncio.wait_for(self.websocket.recv(), timeout=5)
                data = json.loads(response)
                
                if data.get("collaboration_id") == collaboration_id:
                    if data.get("type") == "agent_result":
                        agent_id = data.get("agent_id")
                        results["agents_results"][agent_id] = data.get("result")
                        
                    elif data.get("type") == "collaboration_complete":
                        results["status"] = "completed"
                        results["end_time"] = datetime.utcnow().isoformat()
                        results["summary"] = data.get("summary")
                        break
                        
                    elif data.get("type") == "collaboration_error":
                        results["status"] = "error"
                        results["error"] = data.get("error")
                        break
                        
                await asyncio.sleep(0.1)
            
            if results["status"] == "in_progress":
                results["status"] = "timeout"
                results["error"] = "Collaboration timeout"
            
            return results
            
        except asyncio.TimeoutError:
            logger.error(f"Collaboration {collaboration_id} timed out")
            results["status"] = "timeout"
            results["error"] = "Collaboration timeout"
            return results
        except Exception as e:
            logger.error(f"Error monitoring collaboration: {e}")
            results["status"] = "error"
            results["error"] = str(e)
            return results
    
    async def get_available_agents(self) -> List[Dict[str, Any]]:
        """Get list of available agents in the Coral network"""
        try:
            if not self.websocket:
                await self.connect()
            
            request = {
                "type": "list_agents",
                "session_id": self.session_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.websocket.send(json.dumps(request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("status") == "success":
                return response_data.get("agents", [])
            else:
                logger.error(f"Failed to get agents: {response_data}")
                return []
                
        except Exception as e:
            logger.error(f"Error getting available agents: {e}")
            return []
    
    async def request_agent_task(self, agent_id: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Request a specific agent to perform a task"""
        try:
            if not self.websocket:
                await self.connect()
            
            task_request = {
                "type": "agent_task",
                "session_id": self.session_id,
                "agent_id": agent_id,
                "task": task,
                "context": context,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await self.websocket.send(json.dumps(task_request))
            response = await self.websocket.recv()
            response_data = json.loads(response)
            
            if response_data.get("status") == "success":
                return {
                    "task_id": response_data.get("task_id"),
                    "result": response_data.get("result"),
                    "success": True
                }
            else:
                logger.error(f"Agent task failed: {response_data}")
                return {"error": response_data.get("error"), "success": False}
                
        except Exception as e:
            logger.error(f"Error requesting agent task: {e}")
            return {"error": str(e), "success": False}
    
    def sync_create_collaboration(self, task: str, code: str, language: str) -> Dict[str, Any]:
        """Synchronous wrapper for creating agent collaboration"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.create_agent_collaboration(task, code, language)
            )
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in sync collaboration: {e}")
            return {"error": str(e), "success": False}
    
    def sync_get_agents(self) -> List[Dict[str, Any]]:
        """Synchronous wrapper for getting available agents"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self.get_available_agents())
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in sync get agents: {e}")
            return []
    
    def sync_request_agent(self, agent_id: str, task: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for requesting agent task"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.request_agent_task(agent_id, task, context)
            )
            loop.close()
            return result
        except Exception as e:
            logger.error(f"Error in sync agent request: {e}")
            return {"error": str(e), "success": False}