"""
Code analysis API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.models import Repository, File
from app.schemas.repository import (
    MissingDocsResponse,
    ArchitectureResponse,
)

router = APIRouter()


@router.post("/missing-docs", response_model=MissingDocsResponse)
async def detect_missing_documentation(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Detect missing documentation in repository
    """
    # Get repository
    result = await db.execute(
        select(Repository).where(Repository.id == repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get files
    result = await db.execute(
        select(File).where(File.repository_id == repository_id)
    )
    files = result.scalars().all()
    
    # Simplified analysis - in production, use AI service
    undocumented_functions = []
    undocumented_apis = []
    missing_comments = []
    outdated_sections = []
    
    for file in files:
        if not file.content:
            continue
        
        # Simple heuristic: check for functions without docstrings
        if file.file_type in ['py', 'js', 'ts']:
            lines = file.content.split('\n')
            for i, line in enumerate(lines):
                if 'def ' in line or 'function ' in line:
                    # Check if next line has docstring/comment
                    if i + 1 < len(lines) and not any(c in lines[i + 1] for c in ['"""', "'''", '//', '/*']):
                        func_name = line.split('(')[0].split()[-1]
                        undocumented_functions.append({
                            "file": file.path,
                            "function": func_name,
                            "line": i + 1,
                            "severity": "medium",
                            "suggestion": f"Add docstring for {func_name}"
                        })
    
    return {
        "undocumented_functions": undocumented_functions[:20],  # Limit results
        "undocumented_apis": undocumented_apis,
        "missing_comments": missing_comments,
        "outdated_sections": outdated_sections,
    }


@router.post("/architecture", response_model=ArchitectureResponse)
async def generate_architecture_diagram(
    repository_id: UUID,
    diagram_type: str = "mermaid",
    db: AsyncSession = Depends(get_db)
):
    """
    Generate architecture diagram
    """
    # Get repository
    result = await db.execute(
        select(Repository).where(Repository.id == repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get files to analyze structure
    result = await db.execute(
        select(File).where(File.repository_id == repository_id)
    )
    files = result.scalars().all()
    
    # Simplified diagram generation
    components = []
    has_frontend = any('frontend' in f.path or 'client' in f.path for f in files)
    has_backend = any('backend' in f.path or 'server' in f.path or 'api' in f.path for f in files)
    has_database = any('model' in f.path or 'schema' in f.path for f in files)
    
    diagram = "graph TB\n"
    
    if has_frontend:
        diagram += "    A[Frontend]\n"
        components.append({
            "name": "Frontend",
            "type": "client",
            "technologies": [repository.metadata.get('language', 'JavaScript')]
        })
    
    if has_backend:
        diagram += "    B[Backend API]\n"
        if has_frontend:
            diagram += "    A --> B\n"
        components.append({
            "name": "Backend API",
            "type": "server",
            "technologies": [repository.metadata.get('language', 'Python')]
        })
    
    if has_database:
        diagram += "    C[Database]\n"
        if has_backend:
            diagram += "    B --> C\n"
        components.append({
            "name": "Database",
            "type": "database",
            "technologies": ["PostgreSQL"]
        })
    
    return {
        "diagram": diagram,
        "format": diagram_type,
        "components": components
    }
