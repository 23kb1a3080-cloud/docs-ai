"""
Repository API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.models import Repository, File
from app.schemas.repository import (
    RepositoryAnalyzeRequest,
    RepositoryResponse,
    RepositoryListResponse,
    RepositoryStructureResponse,
    FileContentResponse,
)
from app.services.github_service import GitHubService
# RAG service disabled for minimal setup
# from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/analyze", response_model=RepositoryResponse)
async def analyze_repository(
    request: RepositoryAnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a GitHub repository
    """
    try:
        github_service = GitHubService()
        # RAG service disabled for minimal setup
        # rag_service = RAGService()
        
        # Get repository info from GitHub
        repo_info = await github_service.get_repository_info(request.github_url)
        
        # Check if repository already exists
        result = await db.execute(
            select(Repository).where(Repository.github_url == request.github_url)
        )
        repository = result.scalar_one_or_none()
        
        if repository:
            # Update existing repository
            repository.last_analyzed = None  # Will be updated after analysis
            repository.metadata = repo_info
        else:
            # Create new repository
            repository = Repository(
                github_url=request.github_url,
                name=repo_info['name'],
                owner=repo_info['owner'],
                default_branch=repo_info['default_branch'],
                metadata=repo_info,
            )
            db.add(repository)
        
        await db.commit()
        await db.refresh(repository)
        
        # Get repository structure
        structure = await github_service.get_repository_structure(
            request.github_url,
            request.branch or repo_info['default_branch']
        )
        
        # Store files in database
        for item in structure:
            if item['type'] == 'file':
                # Get file content
                try:
                    file_data = await github_service.get_file_content(
                        request.github_url,
                        item['path'],
                        request.branch or repo_info['default_branch']
                    )
                    
                    file = File(
                        repository_id=repository.id,
                        path=item['path'],
                        file_type=item['path'].split('.')[-1] if '.' in item['path'] else 'unknown',
                        content=file_data['content'],
                    )
                    db.add(file)
                except Exception as e:
                    print(f"Failed to fetch file {item['path']}: {e}")
        
        await db.commit()
        
        # Index repository for RAG (disabled for minimal setup)
        # result = await db.execute(
        #     select(File).where(File.repository_id == repository.id)
        # )
        # files = result.scalars().all()
        # 
        # file_data = [
        #     {
        #         'path': f.path,
        #         'content': f.content,
        #         'type': f.file_type,
        #         'size': len(f.content) if f.content else 0
        #     }
        #     for f in files
        # ]
        # 
        # await rag_service.index_repository(str(repository.id), file_data)
        
        # Update last_analyzed timestamp
        from datetime import datetime
        repository.last_analyzed = datetime.utcnow()
        await db.commit()
        await db.refresh(repository)
        
        return repository
    
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Failed to analyze repository: {e}")
        print(f"Full error: {error_details}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{repository_id}", response_model=RepositoryResponse)
async def get_repository(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get repository details
    """
    result = await db.execute(
        select(Repository).where(Repository.id == repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return repository


@router.get("", response_model=RepositoryListResponse)
async def list_repositories(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    List all repositories
    """
    # Get total count
    count_result = await db.execute(select(Repository))
    total = len(count_result.scalars().all())
    
    # Get paginated results
    offset = (page - 1) * limit
    result = await db.execute(
        select(Repository)
        .offset(offset)
        .limit(limit)
    )
    repositories = result.scalars().all()
    
    return {
        "items": repositories,
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/{repository_id}/structure", response_model=RepositoryStructureResponse)
async def get_repository_structure(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get repository file structure
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
    
    # Build tree structure
    tree = []
    for file in files:
        tree.append({
            "path": file.path,
            "type": "file",
            "size": len(file.content) if file.content else 0,
            "language": file.file_type,
        })
    
    return {"tree": tree}


@router.get("/{repository_id}/files", response_model=FileContentResponse)
async def get_file_content(
    repository_id: UUID,
    path: str = Query(..., description="File path"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get file content
    """
    result = await db.execute(
        select(File).where(
            File.repository_id == repository_id,
            File.path == path
        )
    )
    file = result.scalar_one_or_none()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "path": file.path,
        "content": file.content or "",
        "language": file.file_type,
        "size": len(file.content) if file.content else 0,
        "last_modified": file.last_updated,
    }


@router.delete("/{repository_id}")
async def delete_repository(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete repository
    """
    result = await db.execute(
        select(Repository).where(Repository.id == repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Delete from vector database (disabled for minimal setup)
    # rag_service = RAGService()
    # await rag_service.delete_repository_index(str(repository_id))
    
    # Delete from database
    await db.delete(repository)
    await db.commit()
    
    return {"message": "Repository deleted successfully"}
