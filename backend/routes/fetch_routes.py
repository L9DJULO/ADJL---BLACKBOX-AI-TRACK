# routes/fetch_routes.py
from fastapi import APIRouter, HTTPException
from services.fetch_service import FetchService, fetch_data_for_command
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/fetch", tags=["fetch"])

class FetchRequest(BaseModel):
    command: str
    context: str = ""
    api_name: Optional[str] = None
    package_name: Optional[str] = None
    search_query: Optional[str] = None

@router.post("/auto")
async def auto_fetch(request: FetchRequest):
    """Fetch automatique basé sur la commande"""
    try:
        result = await fetch_data_for_command(request.command, request.context)
        return {
            "success": True,
            "command": request.command,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documentation/{api_name}")
async def get_documentation(api_name: str, endpoint: Optional[str] = None):
    """Récupère la documentation d'une API"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_api_documentation(api_name, endpoint)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/examples/{language}/{topic}")
async def get_code_examples(language: str, topic: str):
    """Récupère des exemples de code"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_code_examples(language, topic)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/package/npm/{package_name}")
async def get_npm_package(package_name: str):
    """Récupère les infos d'un package NPM"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_npm_package_info(package_name)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/package/pypi/{package_name}")
async def get_pypi_package(package_name: str):
    """Récupère les infos d'un package Python"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_python_package_info(package_name)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stackoverflow")
async def search_stackoverflow(query: str):
    """Recherche sur StackOverflow"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_stackoverflow_solutions(query)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/best-practices/{language}/{topic}")
async def get_best_practices(language: str, topic: str):
    """Récupère les meilleures pratiques"""
    try:
        async with FetchService() as fetch_service:
            result = await fetch_service.fetch_best_practices(language, topic)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))