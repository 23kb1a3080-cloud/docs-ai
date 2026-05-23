"""
Chat API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List

from app.core.database import get_db
from app.models import Repository, ChatSession, ChatMessage
from app.schemas.repository import (
    ChatSessionCreateRequest,
    ChatSessionResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ChatHistoryResponse,
    SearchRequest,
    SearchResponse,
)
from app.services.rag_service import RAGService

router = APIRouter()


@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    request: ChatSessionCreateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new chat session
    """
    # Verify repository exists
    result = await db.execute(
        select(Repository).where(Repository.id == request.repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Create session
    session = ChatSession(repository_id=request.repository_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    
    return {
        "session_id": session.id,
        "created_at": session.created_at
    }


@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_chat_message(
    session_id: UUID,
    request: ChatMessageRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message in chat session
    """
    # Get session
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    user_message = ChatMessage(
        session_id=session_id,
        role="user",
        content=request.message
    )
    db.add(user_message)
    
    # Get chat history
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    )
    history = result.scalars().all()
    history_list = [
        {"role": msg.role, "content": msg.content}
        for msg in reversed(history)
    ]
    
    # Generate response using RAG
    rag_service = RAGService()
    response_data = await rag_service.generate_answer(
        str(session.repository_id),
        request.message,
        history_list
    )
    
    # Save assistant message
    assistant_message = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=response_data['answer'],
        metadata={"sources": response_data.get('sources', [])}
    )
    db.add(assistant_message)
    
    await db.commit()
    await db.refresh(assistant_message)
    
    return {
        "message_id": assistant_message.id,
        "role": assistant_message.role,
        "content": assistant_message.content,
        "sources": [
            {
                "file": src['file'],
                "line_range": [0, 0],
                "relevance": src.get('relevance', 0.0)
            }
            for src in response_data.get('sources', [])
        ],
        "created_at": assistant_message.created_at
    }


@router.get("/sessions/{session_id}/messages", response_model=ChatHistoryResponse)
async def get_chat_history(
    session_id: UUID,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """
    Get chat history
    """
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at.asc())
        .limit(limit)
    )
    messages = result.scalars().all()
    
    formatted_messages = []
    for msg in messages:
        formatted_messages.append({
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "sources": msg.metadata.get('sources', []) if msg.role == "assistant" else None,
            "created_at": msg.created_at
        })
    
    return {"messages": formatted_messages}


@router.post("/search", response_model=SearchResponse)
async def search_repository(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Search repository content
    """
    # Verify repository exists
    result = await db.execute(
        select(Repository).where(Repository.id == request.repository_id)
    )
    repository = result.scalar_one_or_none()
    
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Search using RAG
    rag_service = RAGService()
    results = await rag_service.search_repository(
        str(request.repository_id),
        request.query,
        request.limit
    )
    
    formatted_results = [
        {
            "file": r['file_path'],
            "content": r['content'],
            "score": r['score'],
            "line_range": [0, 0]  # Simplified
        }
        for r in results
    ]
    
    return {"results": formatted_results}
