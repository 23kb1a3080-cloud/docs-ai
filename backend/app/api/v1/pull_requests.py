"""
Pull Request API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.core.database import get_db
from app.models import Repository, PullRequest
from app.schemas.repository import (
    PullRequestAnalyzeRequest,
    PullRequestResponse,
)
from app.services.github_service import GitHubService
from app.services.ai_service import AIService

router = APIRouter()


@router.post("/analyze", response_model=PullRequestResponse)
async def analyze_pull_request(
    request: PullRequestAnalyzeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Analyze a pull request
    """
    # Get repository
    result = await db.execute(
        select(Repository).where(Repository.id == request.repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Get PR from GitHub
    github_service = GitHubService()
    pr_data = await github_service.get_pull_request(
        repository.github_url,
        request.pr_number
    )
    
    # Analyze with AI
    ai_service = AIService()
    analysis = await ai_service.analyze_pr_changes(pr_data, pr_data['files'])
    
    # Save to database
    pr = PullRequest(
        repository_id=request.repository_id,
        pr_number=request.pr_number,
        title=pr_data['title'],
        status="analyzed",
        analysis={
            "summary": analysis.get('summary', ''),
            "files_changed": len(pr_data['files']),
            "lines_added": sum(f['additions'] for f in pr_data['files']),
            "lines_removed": sum(f['deletions'] for f in pr_data['files']),
            "affected_modules": analysis.get('affected_modules', []),
            "breaking_changes": analysis.get('breaking_changes', False),
        },
        suggestions=[
            {
                "type": "documentation",
                "priority": "high",
                "message": "Update documentation to reflect changes"
            }
        ]
    )
    db.add(pr)
    await db.commit()
    await db.refresh(pr)
    
    return pr
