"""
Documentation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from datetime import datetime

from app.core.database import get_db
from app.models import Repository, Documentation, DocumentationVersion, File
from app.schemas.repository import (
    DocumentationGenerateRequest,
    DocumentationResponse,
    DocumentationListResponse,
    DocumentationUpdateRequest,
    JobResponse,
)
from app.services.ai_service import AIService
from app.services.github_service import GitHubService

router = APIRouter()


@router.post("/generate", response_model=JobResponse)
async def generate_documentation(
    request: DocumentationGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate documentation for repository
    """
    # Get repository
    result = await db.execute(
        select(Repository).where(Repository.id == request.repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get files
    result = await db.execute(
        select(File).where(File.repository_id == request.repository_id)
    )
    files = result.scalars().all()
    
    # Initialize services
    ai_service = AIService()
    
    # Generate documentation for each type
    for doc_type in request.doc_types:
        try:
            content = ""
            
            if doc_type == "readme":
                # Prepare sample files
                sample_files = {}
                for f in files[:10]:  # First 10 files
                    if f.content:
                        sample_files[f.path] = f.content[:1000]
                
                content = await ai_service.generate_readme(
                    repository.metadata,
                    [{"path": f.path, "type": "file"} for f in files],
                    sample_files
                )
            
            elif doc_type == "api":
                # Find API files
                api_files = {}
                for f in files:
                    if any(keyword in f.path.lower() for keyword in ['api', 'route', 'endpoint', 'controller']):
                        if f.content:
                            api_files[f.path] = f.content
                
                if api_files:
                    content = await ai_service.generate_api_documentation(api_files)
                else:
                    content = "# API Documentation\n\nNo API files detected in this repository."
            
            elif doc_type == "architecture":
                # Get key files
                key_files = {}
                for f in files[:15]:
                    if f.content:
                        key_files[f.path] = f.content[:1500]
                
                content = await ai_service.generate_architecture_doc(
                    repository.metadata,
                    [{"path": f.path, "type": "file"} for f in files],
                    key_files
                )
            
            elif doc_type == "setup":
                content = f"""# Setup Instructions

## Prerequisites
- {repository.metadata.get('language', 'Programming language')}

## Installation
1. Clone the repository
```bash
git clone {repository.github_url}
cd {repository.name}
```

2. Install dependencies
(Add specific instructions based on detected package manager)

3. Run the application
(Add specific run instructions)
"""
            
            # Save documentation
            doc = Documentation(
                repository_id=request.repository_id,
                doc_type=doc_type,
                content=content,
                metadata={"generated_by": "ai", "version": 1}
            )
            db.add(doc)
            
            # Create version
            version = DocumentationVersion(
                documentation_id=doc.id,
                version_number=1,
                content=content,
                change_summary="Initial generation"
            )
            db.add(version)
        
        except Exception as e:
            print(f"Failed to generate {doc_type} documentation: {e}")
    
    await db.commit()
    
    return {
        "job_id": request.repository_id,
        "status": "completed",
        "estimated_time_seconds": 0
    }


@router.get("/{repository_id}", response_model=DocumentationResponse)
async def get_documentation(
    repository_id: UUID,
    type: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get documentation by type
    """
    result = await db.execute(
        select(Documentation).where(
            Documentation.repository_id == repository_id,
            Documentation.doc_type == type
        )
    )
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    return doc


@router.get("/{repository_id}/list", response_model=DocumentationListResponse)
async def list_documentation(
    repository_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    List all documentation for repository
    """
    result = await db.execute(
        select(Documentation).where(Documentation.repository_id == repository_id)
    )
    docs = result.scalars().all()
    
    items = [
        {
            "id": doc.id,
            "doc_type": doc.doc_type,
            "generated_at": doc.generated_at,
            "version": doc.metadata.get("version", 1)
        }
        for doc in docs
    ]
    
    return {"items": items}


@router.put("/{documentation_id}", response_model=DocumentationResponse)
async def update_documentation(
    documentation_id: UUID,
    request: DocumentationUpdateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Update documentation
    """
    result = await db.execute(
        select(Documentation).where(Documentation.id == documentation_id)
    )
    doc = result.scalar_one_or_none()
    
    if not doc:
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    # Update content
    doc.content = request.content
    doc.updated_at = datetime.utcnow()
    
    # Increment version
    current_version = doc.metadata.get("version", 1)
    new_version = current_version + 1
    doc.metadata["version"] = new_version
    
    # Create version history
    version = DocumentationVersion(
        documentation_id=documentation_id,
        version_number=new_version,
        content=request.content,
        change_summary=request.change_summary or "Manual update"
    )
    db.add(version)
    
    await db.commit()
    await db.refresh(doc)
    
    return doc
