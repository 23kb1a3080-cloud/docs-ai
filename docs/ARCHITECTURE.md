# DocMind AI - System Architecture

## 🏗️ High-Level Architecture

```mermaid
graph TB
    subgraph "Frontend Layer"
        A[Next.js App]
        B[React Components]
        C[State Management]
        D[API Client]
    end
    
    subgraph "API Gateway"
        E[FastAPI Server]
        F[Authentication Middleware]
        G[Rate Limiting]
    end
    
    subgraph "Service Layer"
        H[GitHub Service]
        I[Documentation Service]
        J[RAG Service]
        K[Analysis Service]
    end
    
    subgraph "AI Layer"
        L[OpenAI/Gemini API]
        M[LangChain Pipeline]
        N[Prompt Templates]
    end
    
    subgraph "Data Layer"
        O[PostgreSQL]
        P[ChromaDB]
        Q[Redis Cache]
    end
    
    subgraph "External APIs"
        R[GitHub API]
    end
    
    A --> D
    D --> E
    E --> F
    F --> G
    G --> H
    G --> I
    G --> J
    G --> K
    
    H --> R
    I --> L
    J --> M
    J --> P
    K --> L
    
    M --> L
    M --> P
    
    H --> O
    I --> O
    J --> O
    K --> O
    
    I --> Q
    J --> Q
```

## 📦 Component Architecture

### Frontend Architecture

```mermaid
graph LR
    A[Pages] --> B[Layouts]
    B --> C[Components]
    C --> D[UI Components]
    C --> E[Feature Components]
    
    A --> F[API Hooks]
    F --> G[API Client]
    
    A --> H[State Management]
    H --> I[Context Providers]
```

#### Key Components

1. **Dashboard Layout**
   - Left Sidebar: Repository tree, PR history
   - Center Panel: Documentation viewer
   - Right Sidebar: AI chat assistant
   - Top Bar: Repository input, actions

2. **Repository Explorer**
   - File tree visualization
   - File content viewer
   - Syntax highlighting

3. **Documentation Viewer**
   - Markdown renderer
   - Code block highlighting
   - Mermaid diagram support
   - Table of contents

4. **Chat Interface**
   - Message history
   - Streaming responses
   - Code snippet rendering
   - Context indicators

5. **PR Analyzer**
   - Diff viewer
   - Change summary
   - Documentation suggestions

### Backend Architecture

```mermaid
graph TB
    A[FastAPI App] --> B[Router Layer]
    B --> C[Repository Routes]
    B --> D[Documentation Routes]
    B --> E[Chat Routes]
    B --> F[Analysis Routes]
    
    C --> G[GitHub Service]
    D --> H[Documentation Service]
    E --> I[RAG Service]
    F --> J[Analysis Service]
    
    G --> K[GitHub API Client]
    H --> L[AI Generator]
    I --> M[Vector Store]
    J --> L
    
    L --> N[OpenAI/Gemini]
    M --> O[ChromaDB]
    
    G --> P[Database]
    H --> P
    I --> P
    J --> P
```

#### Service Layer

1. **GitHub Service**
   - Repository fetching
   - File content retrieval
   - PR analysis
   - Commit history

2. **Documentation Service**
   - Content generation
   - Template management
   - Version control
   - Export functionality

3. **RAG Service**
   - Document chunking
   - Embedding generation
   - Vector storage
   - Semantic search
   - Context retrieval

4. **Analysis Service**
   - Code parsing
   - Function detection
   - API endpoint extraction
   - Missing doc detection

## 🔄 Data Flow

### 1. Repository Analysis Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant G as GitHub API
    participant AI as AI Service
    participant DB as Database
    
    U->>F: Enter GitHub URL
    F->>B: POST /api/repositories/analyze
    B->>G: Fetch repository data
    G-->>B: Repository structure
    B->>DB: Store repository info
    B->>AI: Generate documentation
    AI-->>B: Generated docs
    B->>DB: Store documentation
    B-->>F: Analysis complete
    F-->>U: Display documentation
```

### 2. RAG Chat Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant V as Vector DB
    participant AI as AI Service
    
    U->>F: Ask question
    F->>B: POST /api/chat
    B->>V: Semantic search
    V-->>B: Relevant chunks
    B->>AI: Generate answer with context
    AI-->>B: Streaming response
    B-->>F: Stream answer
    F-->>U: Display answer
```

### 3. PR Analysis Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant G as GitHub API
    participant AI as AI Service
    
    U->>F: Select PR
    F->>B: POST /api/prs/analyze
    B->>G: Fetch PR diff
    G-->>B: Changed files
    B->>AI: Analyze changes
    AI-->>B: Change summary
    B->>AI: Suggest doc updates
    AI-->>B: Suggestions
    B-->>F: Analysis results
    F-->>U: Display analysis
```

## 💾 Database Schema

```mermaid
erDiagram
    REPOSITORY ||--o{ DOCUMENTATION : has
    REPOSITORY ||--o{ PULL_REQUEST : contains
    REPOSITORY ||--o{ FILE : contains
    DOCUMENTATION ||--o{ DOCUMENTATION_VERSION : has
    PULL_REQUEST ||--o{ FILE_CHANGE : includes
    REPOSITORY ||--o{ CHAT_SESSION : has
    CHAT_SESSION ||--o{ CHAT_MESSAGE : contains
    
    REPOSITORY {
        uuid id PK
        string github_url
        string name
        string owner
        string default_branch
        timestamp last_analyzed
        jsonb metadata
        timestamp created_at
    }
    
    DOCUMENTATION {
        uuid id PK
        uuid repository_id FK
        string doc_type
        text content
        jsonb metadata
        timestamp generated_at
        timestamp updated_at
    }
    
    DOCUMENTATION_VERSION {
        uuid id PK
        uuid documentation_id FK
        int version_number
        text content
        string change_summary
        timestamp created_at
    }
    
    PULL_REQUEST {
        uuid id PK
        uuid repository_id FK
        int pr_number
        string title
        string status
        text analysis
        jsonb suggestions
        timestamp analyzed_at
    }
    
    FILE {
        uuid id PK
        uuid repository_id FK
        string path
        string type
        text content
        boolean is_documented
        timestamp last_updated
    }
    
    FILE_CHANGE {
        uuid id PK
        uuid pull_request_id FK
        uuid file_id FK
        string change_type
        text diff
        text analysis
    }
    
    CHAT_SESSION {
        uuid id PK
        uuid repository_id FK
        timestamp created_at
        timestamp last_message_at
    }
    
    CHAT_MESSAGE {
        uuid id PK
        uuid session_id FK
        string role
        text content
        jsonb metadata
        timestamp created_at
    }
    
    VECTOR_DOCUMENT {
        uuid id PK
        uuid repository_id FK
        uuid file_id FK
        string chunk_id
        text content
        vector embedding
        jsonb metadata
    }
```

## 🤖 AI Pipeline Architecture

### Documentation Generation Pipeline

```mermaid
graph LR
    A[Repository Files] --> B[Code Parser]
    B --> C[Structure Analyzer]
    C --> D[Prompt Builder]
    D --> E[LLM API]
    E --> F[Response Parser]
    F --> G[Markdown Formatter]
    G --> H[Documentation Output]
```

### RAG Pipeline

```mermaid
graph TB
    A[Repository Content] --> B[Text Splitter]
    B --> C[Chunk Processor]
    C --> D[Embedding Model]
    D --> E[Vector Store]
    
    F[User Query] --> G[Query Embedding]
    G --> H[Similarity Search]
    E --> H
    H --> I[Context Retrieval]
    I --> J[Prompt Construction]
    J --> K[LLM Generation]
    K --> L[Response]
```

## 🔐 Security Architecture

### Authentication & Authorization

```mermaid
graph TB
    A[User Request] --> B{Has Token?}
    B -->|No| C[Return 401]
    B -->|Yes| D{Valid Token?}
    D -->|No| C
    D -->|Yes| E{Has Permission?}
    E -->|No| F[Return 403]
    E -->|Yes| G[Process Request]
```

### API Security Layers

1. **Rate Limiting**
   - Per-IP limits
   - Per-user limits
   - Endpoint-specific limits

2. **Input Validation**
   - Pydantic schemas
   - URL validation
   - Content sanitization

3. **API Key Management**
   - Environment variables
   - Secret rotation
   - Encrypted storage

## 📊 Caching Strategy

```mermaid
graph LR
    A[Request] --> B{Cache Hit?}
    B -->|Yes| C[Return Cached]
    B -->|No| D[Process Request]
    D --> E[Store in Cache]
    E --> F[Return Response]
```

### Cache Layers

1. **Repository Metadata** - 1 hour TTL
2. **Generated Documentation** - 24 hours TTL
3. **File Contents** - 6 hours TTL
4. **Vector Embeddings** - Persistent
5. **API Responses** - 5 minutes TTL

## 🚀 Scalability Considerations

### Horizontal Scaling

- **Frontend**: Deploy multiple Next.js instances behind load balancer
- **Backend**: Multiple FastAPI workers with shared database
- **Vector DB**: ChromaDB cluster or migrate to Pinecone/Weaviate
- **Cache**: Redis cluster for distributed caching

### Performance Optimizations

1. **Lazy Loading**: Load repository files on-demand
2. **Streaming**: Stream AI responses for better UX
3. **Background Jobs**: Queue heavy processing tasks
4. **CDN**: Cache static assets and documentation
5. **Database Indexing**: Optimize query performance

## 🔄 Deployment Architecture

```mermaid
graph TB
    A[GitHub Repository] --> B[CI/CD Pipeline]
    B --> C[Build Frontend]
    B --> D[Build Backend]
    
    C --> E[Vercel]
    D --> F[Railway/Render]
    
    F --> G[PostgreSQL]
    F --> H[Redis]
    F --> I[ChromaDB]
    
    E --> J[Users]
    F --> J
```

### Infrastructure Components

1. **Frontend Hosting**: Vercel (auto-scaling, edge network)
2. **Backend Hosting**: Railway/Render (containerized deployment)
3. **Database**: Supabase/Neon (managed PostgreSQL)
4. **Cache**: Upstash Redis (serverless Redis)
5. **Vector DB**: ChromaDB (self-hosted) or Pinecone (managed)
6. **Monitoring**: Sentry for error tracking
7. **Analytics**: PostHog for usage analytics

## 📈 Monitoring & Observability

### Key Metrics

1. **Application Metrics**
   - Request latency
   - Error rates
   - API usage
   - Cache hit rates

2. **AI Metrics**
   - Token usage
   - Generation time
   - Quality scores
   - Cost tracking

3. **Business Metrics**
   - Repositories analyzed
   - Documentation generated
   - Chat interactions
   - User engagement

### Logging Strategy

```python
# Structured logging with context
{
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "INFO",
    "service": "documentation-service",
    "repository_id": "uuid",
    "action": "generate_documentation",
    "duration_ms": 1500,
    "tokens_used": 2500
}
```

## 🎯 Technology Decisions

### Why Next.js?
- Server-side rendering for better SEO
- API routes for BFF pattern
- Excellent developer experience
- Built-in optimization

### Why FastAPI?
- High performance (async support)
- Automatic API documentation
- Type safety with Pydantic
- Easy integration with Python AI libraries

### Why ChromaDB?
- Simple setup for MVP
- Built-in embedding support
- Good for hackathon speed
- Can migrate to Pinecone later

### Why PostgreSQL?
- Robust relational database
- JSON support for flexibility
- Vector extension available (pgvector)
- Wide hosting support

---

This architecture is designed for rapid development while maintaining scalability and maintainability for future growth.
