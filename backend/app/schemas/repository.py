"""
Pydantic schemas for repositories
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID


# Repository Schemas
class RepositoryAnalyzeRequest(BaseModel):
    """Request to analyze a repository"""
    github_url: str = Field(..., description="GitHub repository URL")
    branch: Optional[str] = Field("main", description="Branch to analyze")


class RepositoryResponse(BaseModel):
    """Repository response"""
    id: UUID
    github_url: str
    name: str
    owner: str
    default_branch: str
    last_analyzed: Optional[datetime]
    metadata: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


class RepositoryListResponse(BaseModel):
    """List of repositories"""
    items: List[RepositoryResponse]
    total: int
    page: int
    limit: int


class RepositoryStructureNode(BaseModel):
    """Repository file tree node"""
    path: str
    type: str  # file or directory
    size: Optional[int] = None
    language: Optional[str] = None
    children: Optional[List['RepositoryStructureNode']] = None


class RepositoryStructureResponse(BaseModel):
    """Repository structure response"""
    tree: List[RepositoryStructureNode]


class FileContentResponse(BaseModel):
    """File content response"""
    path: str
    content: str
    language: Optional[str]
    size: int
    last_modified: Optional[datetime]


# Documentation Schemas
class DocumentationGenerateRequest(BaseModel):
    """Request to generate documentation"""
    repository_id: UUID
    doc_types: List[str] = Field(..., description="Types of documentation to generate")


class DocumentationResponse(BaseModel):
    """Documentation response"""
    id: UUID
    repository_id: UUID
    doc_type: str
    content: str
    metadata: Dict[str, Any]
    generated_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DocumentationListItem(BaseModel):
    """Documentation list item"""
    id: UUID
    doc_type: str
    generated_at: datetime
    version: int


class DocumentationListResponse(BaseModel):
    """List of documentation"""
    items: List[DocumentationListItem]


class DocumentationUpdateRequest(BaseModel):
    """Request to update documentation"""
    content: str
    change_summary: Optional[str] = None


class DocumentationVersionResponse(BaseModel):
    """Documentation version response"""
    version: int
    change_summary: Optional[str]
    created_at: datetime


class DocumentationHistoryResponse(BaseModel):
    """Documentation history response"""
    versions: List[DocumentationVersionResponse]


# Pull Request Schemas
class PullRequestAnalyzeRequest(BaseModel):
    """Request to analyze a pull request"""
    repository_id: UUID
    pr_number: int


class PRAnalysis(BaseModel):
    """PR analysis details"""
    summary: str
    files_changed: int
    lines_added: int
    lines_removed: int
    affected_modules: List[str]
    breaking_changes: bool


class PRSuggestion(BaseModel):
    """PR documentation suggestion"""
    type: str
    priority: str
    message: str


class PullRequestResponse(BaseModel):
    """Pull request response"""
    id: UUID
    pr_number: int
    title: str
    status: str
    analysis: Optional[PRAnalysis]
    suggestions: List[PRSuggestion]
    analyzed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class PullRequestListResponse(BaseModel):
    """List of pull requests"""
    items: List[PullRequestResponse]
    total: int
    page: int
    limit: int


class FileChangeResponse(BaseModel):
    """File change response"""
    file_path: str
    change_type: str
    additions: int
    deletions: int
    diff: Optional[str]
    analysis: Optional[str]


class PRChangesResponse(BaseModel):
    """PR changes response"""
    changes: List[FileChangeResponse]


# Analysis Schemas
class UndocumentedFunction(BaseModel):
    """Undocumented function"""
    file: str
    function: str
    line: int
    severity: str
    suggestion: str


class UndocumentedAPI(BaseModel):
    """Undocumented API endpoint"""
    endpoint: str
    method: str
    file: str
    line: int
    suggestion: str


class MissingComment(BaseModel):
    """Missing comment"""
    file: str
    line_range: List[int]
    severity: str
    suggestion: str


class OutdatedSection(BaseModel):
    """Outdated documentation section"""
    file: str
    section: str
    reason: str
    suggestion: str


class MissingDocsResponse(BaseModel):
    """Missing documentation response"""
    undocumented_functions: List[UndocumentedFunction]
    undocumented_apis: List[UndocumentedAPI]
    missing_comments: List[MissingComment]
    outdated_sections: List[OutdatedSection]


class ComponentInfo(BaseModel):
    """System component information"""
    name: str
    type: str
    technologies: List[str]


class ArchitectureResponse(BaseModel):
    """Architecture diagram response"""
    diagram: str
    format: str
    components: List[ComponentInfo]


# Chat Schemas
class ChatSessionCreateRequest(BaseModel):
    """Request to create chat session"""
    repository_id: UUID


class ChatSessionResponse(BaseModel):
    """Chat session response"""
    session_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatMessageRequest(BaseModel):
    """Request to send chat message"""
    message: str


class SourceReference(BaseModel):
    """Source reference in chat response"""
    file: str
    line_range: List[int]
    relevance: float


class ChatMessageResponse(BaseModel):
    """Chat message response"""
    message_id: UUID
    role: str
    content: str
    sources: Optional[List[SourceReference]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Chat history response"""
    messages: List[ChatMessageResponse]


class SearchRequest(BaseModel):
    """Search request"""
    repository_id: UUID
    query: str
    limit: int = 5


class SearchResult(BaseModel):
    """Search result"""
    file: str
    content: str
    score: float
    line_range: List[int]


class SearchResponse(BaseModel):
    """Search response"""
    results: List[SearchResult]


# Job Schemas
class JobResponse(BaseModel):
    """Background job response"""
    job_id: UUID
    status: str
    estimated_time_seconds: Optional[int]


# Error Schemas
class ErrorDetail(BaseModel):
    """Error detail"""
    field: Optional[str]
    reason: str


class ErrorResponse(BaseModel):
    """Error response"""
    code: str
    message: str
    details: Optional[ErrorDetail]
