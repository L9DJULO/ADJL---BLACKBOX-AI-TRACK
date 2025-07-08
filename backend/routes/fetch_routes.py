from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from services.fetch_service import FetchService
from models.request_models import AIServiceResponse

router = APIRouter(prefix="/api/fetch", tags=["fetch"])

# Initialize Fetch service
fetch_service = FetchService()

@router.post("/agent/deploy")
async def deploy_agent(
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