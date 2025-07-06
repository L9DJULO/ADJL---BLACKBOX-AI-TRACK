from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any
from services.fetch_service import FetchService
from models.request_models import AIServiceResponse

router = APIRouter(prefix="/api/fetch", tags=["fetch"])

# Initialize Fetch service
fetch_service = FetchService()

@router.post("/agent/deploy")
async def deploy_fetch_agent(
    agent_code: str,
    agent_name: str,
    description: Optional[str] = None
):
    """Deploy a new Fetch.ai agent"""
    try:
        result = await fetch_service.deploy_agent(
            code=agent_code,
            name=agent_name,
            description=description
        )
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent/status/{agent_id}")
async def get_agent_status(agent_id: str):
    """Get status of a deployed agent"""
    try:
        result = await fetch_service.get_agent_status(agent_id)
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/agent/communicate")
async def communicate_with_agent(
    agent_id: str,
    message: str,
    context: Optional[Dict[str, Any]] = None
):
    """Send message to Fetch.ai agent"""
    try:
        result = await fetch_service.communicate_with_agent(
            agent_id=agent_id,
            message=message,
            context=context or {}
        )
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network/search")
async def search_network_resources(
    query: str,
    resource_type: str = Query("documentation", description="Type of resource to search"),
    max_results: int = Query(10, ge=1, le=50)
):
    """Search Fetch.ai network for resources"""
    try:
        result = await fetch_service.search_network_resources(
            query=query,
            resource_type=resource_type,
            max_results=max_results
        )
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data/fetch")
async def fetch_external_data(
    command: str,
    context: str,
    data_sources: Optional[List[str]] = None
):
    """Fetch external data for command enhancement"""
    try:
        result = await fetch_service.fetch_data_for_command(
            command=command,
            context=context,
            sources=data_sources or ["documentation", "examples", "packages"]
        )
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/network/agents")
async def list_available_agents():
    """List available agents on the network"""
    try:
        result = await fetch_service.list_available_agents()
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/collaboration/request")
async def request_collaboration(
    task_description: str,
    required_skills: List[str],
    context: Dict[str, Any]
):
    """Request collaboration from network agents"""
    try:
        result = await fetch_service.request_collaboration(
            task=task_description,
            skills=required_skills,
            context=context
        )
        
        return AIServiceResponse(
            success=True,
            result=result,
            source="fetch_ai"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))