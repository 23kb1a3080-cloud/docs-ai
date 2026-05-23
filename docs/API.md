# DocMind AI - API Documentation

## Base URL

```
Development: http://localhost:8000
Production: https://api.docmind.ai
```

## Authentication

Currently using API key authentication (can be extended to OAuth).

```http
Authorization: Bearer YOUR_API_KEY
```

## API Endpoints

### 1. Repository Management

#### Analyze Repository

```http
POST /api/v1/repositories/analyze
```

**Request Body:**
```json
{
  "github_url": "https://github.com/owner/repo",
  "branch": "main"
}
```

**Response:**
```json
{
  "id": "uuid",
  "name": "repo",
  "owner": "owner",
  "status": "analyzing",
  "message": "Repository analysis started"
}
```

#### Get Repository Details

```http
GET /api/v1/repositories/{repository_id}
```

**Response:**
```json
{
  "id": "uuid",
  "github_url": "https://github.com/owner/repo",
  "name": "repo",
  "owner": "owner",
  "default_branch": "main",
  "last_analyzed": "2024-01-15T10:30:00Z",
  "metadata": {
    "stars": 1234,
    "forks": 56,
    "language": "Python",
    "size_kb": 5000
  },
  "created_at": "2024-01-15T10:00:00Z"
}
```

#### List Repositories

```http
GET /api/v1/repositories?page=1&limit=10
```

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "name": "repo",
      "owner": "owner",
      "last_analyzed": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

#### Get Repository Structure

```http
GET /api/v1/repositories/{repository_id}/structure
```

**Response:**
```json
{
  "tree": [
    {
      "path": "src",
      "type": "directory",
      "children": [
        {
          "path": "src/main.py",
          "type": "file",
          "size": 1024,
          "language": "python"
        }
      ]
    }
  ]
}
```

#### Get File Content

```http
GET /api/v1/repositories/{repository_id}/files?path=src/main.py
```

**Response:**
```json
{
  "path": "src/main.py",
  "content": "# File content here",
  "language": "python",
  "size": 1024,
  "last_modified": "2024-01-15T10:00:00Z"
}
```

### 2. Documentation Management

#### Generate Documentation

```http
POST /api/v1/documentation/generate
```

**Request Body:**
```json
{
  "repository_id": "uuid",
  "doc_types": ["readme", "api", "architecture", "setup"]
}
```

**Response:**
```json
{
  "job_id": "uuid",
  "status": "processing",
  "estimated_time_seconds": 60
}
```

#### Get Documentation

```http
GET /api/v1/documentation/{repository_id}?type=readme
```

**Query Parameters:**
- `type`: readme, api, architecture, setup, overview

**Response:**
```json
{
  "id": "uuid",
  "repository_id": "uuid",
  "doc_type": "readme",
  "content": "# Project Title\n\n...",
  "metadata": {
    "word_count": 500,
    "sections": 8
  },
  "generated_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

#### List Documentation

```http
GET /api/v1/documentation/{repository_id}/list
```

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "doc_type": "readme",
      "generated_at": "2024-01-15T10:30:00Z",
      "version": 1
    },
    {
      "id": "uuid",
      "doc_type": "api",
      "generated_at": "2024-01-15T10:35:00Z",
      "version": 1
    }
  ]
}
```

#### Update Documentation

```http
PUT /api/v1/documentation/{documentation_id}
```

**Request Body:**
```json
{
  "content": "# Updated content",
  "change_summary": "Updated installation instructions"
}
```

**Response:**
```json
{
  "id": "uuid",
  "version": 2,
  "updated_at": "2024-01-15T11:00:00Z"
}
```

#### Get Documentation History

```http
GET /api/v1/documentation/{documentation_id}/history
```

**Response:**
```json
{
  "versions": [
    {
      "version": 2,
      "change_summary": "Updated installation instructions",
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "version": 1,
      "change_summary": "Initial generation",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### 3. Pull Request Analysis

#### Analyze Pull Request

```http
POST /api/v1/prs/analyze
```

**Request Body:**
```json
{
  "repository_id": "uuid",
  "pr_number": 123
}
```

**Response:**
```json
{
  "id": "uuid",
  "pr_number": 123,
  "title": "Add authentication feature",
  "status": "analyzed",
  "analysis": {
    "summary": "Added JWT-based authentication with token refresh",
    "files_changed": 5,
    "lines_added": 250,
    "lines_removed": 30,
    "affected_modules": ["auth", "api", "middleware"],
    "breaking_changes": false
  },
  "suggestions": [
    {
      "type": "documentation",
      "priority": "high",
      "message": "Update API documentation to include new authentication endpoints"
    },
    {
      "type": "documentation",
      "priority": "medium",
      "message": "Add authentication flow diagram to architecture docs"
    }
  ],
  "analyzed_at": "2024-01-15T10:30:00Z"
}
```

#### List Pull Requests

```http
GET /api/v1/prs/{repository_id}?status=open&page=1&limit=10
```

**Response:**
```json
{
  "items": [
    {
      "id": "uuid",
      "pr_number": 123,
      "title": "Add authentication feature",
      "status": "analyzed",
      "analyzed_at": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "limit": 10
}
```

#### Get PR Changes

```http
GET /api/v1/prs/{pr_id}/changes
```

**Response:**
```json
{
  "changes": [
    {
      "file_path": "src/auth/jwt.py",
      "change_type": "added",
      "additions": 120,
      "deletions": 0,
      "diff": "...",
      "analysis": "New JWT authentication module with token generation and validation"
    }
  ]
}
```

### 4. Code Analysis

#### Detect Missing Documentation

```http
POST /api/v1/analysis/missing-docs
```

**Request Body:**
```json
{
  "repository_id": "uuid"
}
```

**Response:**
```json
{
  "undocumented_functions": [
    {
      "file": "src/utils.py",
      "function": "calculate_metrics",
      "line": 45,
      "severity": "high",
      "suggestion": "Add docstring explaining metric calculation logic"
    }
  ],
  "undocumented_apis": [
    {
      "endpoint": "/api/users",
      "method": "POST",
      "file": "src/api/users.py",
      "line": 23,
      "suggestion": "Add OpenAPI documentation"
    }
  ],
  "missing_comments": [
    {
      "file": "src/complex_logic.py",
      "line_range": [100, 150],
      "severity": "medium",
      "suggestion": "Complex algorithm needs explanation"
    }
  ],
  "outdated_sections": [
    {
      "file": "README.md",
      "section": "Installation",
      "reason": "Dependencies have changed",
      "suggestion": "Update dependency versions"
    }
  ]
}
```

#### Generate Architecture Diagram

```http
POST /api/v1/analysis/architecture
```

**Request Body:**
```json
{
  "repository_id": "uuid",
  "diagram_type": "mermaid"
}
```

**Response:**
```json
{
  "diagram": "graph TB\n  A[Frontend] --> B[API]\n  B --> C[Database]",
  "format": "mermaid",
  "components": [
    {
      "name": "Frontend",
      "type": "client",
      "technologies": ["React", "TypeScript"]
    },
    {
      "name": "API",
      "type": "server",
      "technologies": ["FastAPI", "Python"]
    }
  ]
}
```

### 5. RAG Chat

#### Create Chat Session

```http
POST /api/v1/chat/sessions
```

**Request Body:**
```json
{
  "repository_id": "uuid"
}
```

**Response:**
```json
{
  "session_id": "uuid",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Send Chat Message

```http
POST /api/v1/chat/sessions/{session_id}/messages
```

**Request Body:**
```json
{
  "message": "How does authentication work in this project?"
}
```

**Response (Streaming):**
```json
{
  "message_id": "uuid",
  "role": "assistant",
  "content": "The authentication system uses JWT tokens...",
  "sources": [
    {
      "file": "src/auth/jwt.py",
      "line_range": [10, 50],
      "relevance": 0.95
    }
  ],
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Get Chat History

```http
GET /api/v1/chat/sessions/{session_id}/messages?limit=50
```

**Response:**
```json
{
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "How does authentication work?",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "The authentication system uses JWT tokens...",
      "sources": [...],
      "created_at": "2024-01-15T10:30:05Z"
    }
  ]
}
```

#### Search Repository

```http
POST /api/v1/chat/search
```

**Request Body:**
```json
{
  "repository_id": "uuid",
  "query": "authentication implementation",
  "limit": 5
}
```

**Response:**
```json
{
  "results": [
    {
      "file": "src/auth/jwt.py",
      "content": "JWT token generation and validation...",
      "score": 0.95,
      "line_range": [10, 50]
    }
  ]
}
```

### 6. Webhooks

#### Register Webhook

```http
POST /api/v1/webhooks
```

**Request Body:**
```json
{
  "repository_id": "uuid",
  "event_type": "pull_request",
  "callback_url": "https://your-app.com/webhook"
}
```

**Response:**
```json
{
  "webhook_id": "uuid",
  "secret": "webhook_secret_key"
}
```

#### Webhook Payload (PR Event)

```json
{
  "event": "pull_request.opened",
  "repository_id": "uuid",
  "pr_number": 123,
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "title": "Add new feature",
    "author": "username",
    "files_changed": 5
  }
}
```

## Error Responses

### Standard Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid repository URL",
    "details": {
      "field": "github_url",
      "reason": "Must be a valid GitHub URL"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid authentication |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Server error |
| `SERVICE_UNAVAILABLE` | 503 | External service unavailable |

## Rate Limits

| Endpoint | Limit |
|----------|-------|
| Repository Analysis | 10 per hour |
| Documentation Generation | 20 per hour |
| Chat Messages | 100 per hour |
| Other Endpoints | 1000 per hour |

**Rate Limit Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642248000
```

## Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10, max: 100)

**Response Headers:**
```http
X-Total-Count: 250
X-Page: 1
X-Per-Page: 10
Link: <https://api.docmind.ai/api/v1/repositories?page=2>; rel="next"
```

## Filtering & Sorting

**Query Parameters:**
- `sort`: Field to sort by (e.g., `created_at`, `name`)
- `order`: Sort order (`asc` or `desc`)
- `filter[field]`: Filter by field value

**Example:**
```http
GET /api/v1/repositories?sort=created_at&order=desc&filter[language]=Python
```

## Webhooks Signature Verification

Verify webhook authenticity using HMAC:

```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## SDK Examples

### Python

```python
from docmind import DocMindClient

client = DocMindClient(api_key="your_api_key")

# Analyze repository
repo = client.repositories.analyze("https://github.com/owner/repo")

# Generate documentation
docs = client.documentation.generate(repo.id, doc_types=["readme", "api"])

# Chat with repository
session = client.chat.create_session(repo.id)
response = client.chat.send_message(session.id, "How does auth work?")
```

### JavaScript/TypeScript

```typescript
import { DocMindClient } from '@docmind/sdk';

const client = new DocMindClient({ apiKey: 'your_api_key' });

// Analyze repository
const repo = await client.repositories.analyze({
  githubUrl: 'https://github.com/owner/repo'
});

// Generate documentation
const docs = await client.documentation.generate({
  repositoryId: repo.id,
  docTypes: ['readme', 'api']
});

// Chat with repository
const session = await client.chat.createSession({ repositoryId: repo.id });
const response = await client.chat.sendMessage({
  sessionId: session.id,
  message: 'How does auth work?'
});
```

## WebSocket API

### Chat Streaming

```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/chat/stream');

ws.send(JSON.stringify({
  session_id: 'uuid',
  message: 'Explain the authentication flow'
}));

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log(data.content); // Streaming response
};
```

---

For more information, visit our [API documentation portal](https://docs.docmind.ai) or join our [Discord community](https://discord.gg/docmind).
