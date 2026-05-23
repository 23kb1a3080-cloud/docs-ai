"""
Repository database models
"""
from sqlalchemy import Column, String, DateTime, JSON, Integer, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.core.database import Base


class Repository(Base):
    """Repository model"""
    __tablename__ = "repositories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_url = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    owner = Column(String, nullable=False, index=True)
    default_branch = Column(String, default="main")
    last_analyzed = Column(DateTime, nullable=True)
    repo_metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    documentations = relationship("Documentation", back_populates="repository", cascade="all, delete-orphan")
    pull_requests = relationship("PullRequest", back_populates="repository", cascade="all, delete-orphan")
    files = relationship("File", back_populates="repository", cascade="all, delete-orphan")
    chat_sessions = relationship("ChatSession", back_populates="repository", cascade="all, delete-orphan")


class Documentation(Base):
    """Documentation model"""
    __tablename__ = "documentations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    doc_type = Column(String, nullable=False, index=True)  # readme, api, architecture, setup
    content = Column(Text, nullable=False)
    doc_metadata = Column(JSON, default={})
    generated_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    repository = relationship("Repository", back_populates="documentations")
    versions = relationship("DocumentationVersion", back_populates="documentation", cascade="all, delete-orphan")


class DocumentationVersion(Base):
    """Documentation version history"""
    __tablename__ = "documentation_versions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    documentation_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    version_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    change_summary = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documentation = relationship("Documentation", back_populates="versions")


class PullRequest(Base):
    """Pull Request model"""
    __tablename__ = "pull_requests"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    pr_number = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, analyzed
    analysis = Column(JSON, default={})
    suggestions = Column(JSON, default=[])
    analyzed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    repository = relationship("Repository", back_populates="pull_requests")
    file_changes = relationship("FileChange", back_populates="pull_request", cascade="all, delete-orphan")


class File(Base):
    """File model"""
    __tablename__ = "files"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    path = Column(String, nullable=False, index=True)
    file_type = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    is_documented = Column(Boolean, default=False)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    repository = relationship("Repository", back_populates="files")


class FileChange(Base):
    """File change in PR"""
    __tablename__ = "file_changes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pull_request_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    file_id = Column(UUID(as_uuid=True), nullable=True)
    file_path = Column(String, nullable=False)
    change_type = Column(String, nullable=False)  # added, modified, deleted
    diff = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pull_request = relationship("PullRequest", back_populates="file_changes")


class ChatSession(Base):
    """Chat session model"""
    __tablename__ = "chat_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    repository = relationship("Repository", back_populates="chat_sessions")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    role = Column(String, nullable=False)  # user, assistant
    content = Column(Text, nullable=False)
    message_metadata = Column(JSON, default={})  # sources, tokens, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ChatSession", back_populates="messages")
