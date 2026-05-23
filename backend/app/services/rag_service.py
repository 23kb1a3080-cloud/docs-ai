"""
RAG (Retrieval Augmented Generation) service for chat
Simplified version without heavy dependencies
"""
from typing import List, Dict, Any, Optional
import re

from app.core.config import settings
from app.services.ai_service import AIService


class RAGService:
    """Service for RAG-based chat - Simplified version using keyword search"""
    
    def __init__(self):
        # Initialize AI service
        self.ai_service = AIService()
        
        # In-memory storage for demo (replace with vector DB in production)
        self.repository_data: Dict[str, List[Dict[str, Any]]] = {}
    
    def _get_collection_name(self, repository_id: str) -> str:
        """Get collection name for repository"""
        return f"repo_{repository_id.replace('-', '_')}"
    
    def _simple_chunk_text(self, text: str, chunk_size: int = 1000) -> List[str]:
        """Simple text chunking"""
        chunks = []
        words = text.split()
        current_chunk = []
        current_size = 0
        
        for word in words:
            current_chunk.append(word)
            current_size += len(word) + 1
            
            if current_size >= chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def _keyword_search(self, query: str, documents: List[Dict[str, Any]], limit: int = 5) -> List[Dict[str, Any]]:
        """Simple keyword-based search"""
        query_terms = set(re.findall(r'\w+', query.lower()))
        
        scored_docs = []
        for doc in documents:
            content = doc.get('content', '').lower()
            content_terms = set(re.findall(r'\w+', content))
            
            # Calculate simple relevance score
            matches = len(query_terms & content_terms)
            if matches > 0:
                score = matches / len(query_terms)
                scored_docs.append({
                    **doc,
                    'score': score
                })
        
        # Sort by score and return top results
        scored_docs.sort(key=lambda x: x['score'], reverse=True)
        return scored_docs[:limit]
    
    async def index_repository(
        self, 
        repository_id: str,
        files: List[Dict[str, Any]]
    ) -> None:
        """
        Index repository files into memory storage
        
        Args:
            repository_id: Repository ID
            files: List of files with content
        """
        try:
            documents = []
            
            for file in files:
                # Skip binary files and large files
                if file.get('size', 0) > 10 * 1024 * 1024:  # 10MB
                    continue
                
                content = file.get('content', '')
                if not content:
                    continue
                
                # Chunk the content
                chunks = self._simple_chunk_text(content, chunk_size=1000)
                
                for i, chunk in enumerate(chunks):
                    documents.append({
                        'content': chunk,
                        'file_path': file['path'],
                        'file_type': file.get('type', 'unknown'),
                        'chunk_index': i,
                        'repository_id': repository_id,
                    })
            
            # Store in memory
            self.repository_data[repository_id] = documents
            
            print(f"Indexed {len(documents)} chunks from {len(files)} files for repository {repository_id}")
        
        except Exception as e:
            print(f"Failed to index repository: {e}")
            raise ValueError(f"Failed to index repository: {e}")
    
    async def search_repository(
        self, 
        repository_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search repository using keyword search
        
        Args:
            repository_id: Repository ID
            query: Search query
            limit: Number of results
            
        Returns:
            List of relevant chunks
        """
        try:
            documents = self.repository_data.get(repository_id, [])
            
            if not documents:
                return []
            
            # Perform keyword search
            results = self._keyword_search(query, documents, limit)
            
            # Format results
            formatted_results = []
            for doc in results:
                formatted_results.append({
                    "content": doc['content'],
                    "file_path": doc['file_path'],
                    "score": doc['score'],
                })
            
            return formatted_results
        
        except Exception as e:
            print(f"Search failed: {e}")
            return []
    
    async def generate_answer(
        self, 
        repository_id: str,
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Generate answer using RAG
        
        Args:
            repository_id: Repository ID
            question: User question
            chat_history: Previous chat messages
            
        Returns:
            Answer with sources
        """
        try:
            # Search for relevant context
            relevant_chunks = await self.search_repository(
                repository_id, 
                question, 
                limit=5
            )
            
            if not relevant_chunks:
                return {
                    "answer": "I couldn't find relevant information in the repository to answer your question.",
                    "sources": []
                }
            
            # Build context
            context = "\n\n".join([
                f"File: {chunk['file_path']}\n{chunk['content']}"
                for chunk in relevant_chunks
            ])
            
            # Build chat history context
            history_context = ""
            if chat_history:
                history_context = "\n".join([
                    f"{msg['role']}: {msg['content']}"
                    for msg in chat_history[-5:]  # Last 5 messages
                ])
            
            # Generate answer
            system_prompt = """You are a helpful AI assistant that answers questions about code repositories.
Use the provided context from the repository to answer questions accurately.
If the context doesn't contain enough information, say so.
Provide code examples when relevant."""
            
            # Build prompt with history if available
            history_section = f"Previous conversation:\n{history_context}\n" if history_context else ""
            
            prompt = f"""Context from repository:
{context}

{history_section}

Question: {question}

Answer the question based on the context provided. Be specific and reference file names when relevant."""
            
            answer = await self.ai_service.generate_completion(
                prompt, 
                system_prompt,
                temperature=0.7
            )
            
            # Format sources
            sources = [
                {
                    "file": chunk['file_path'],
                    "relevance": chunk['score']
                }
                for chunk in relevant_chunks[:3]
            ]
            
            return {
                "answer": answer,
                "sources": sources
            }
        
        except Exception as e:
            print(f"Failed to generate answer: {e}")
            return {
                "answer": "I encountered an error while processing your question.",
                "sources": []
            }
    
    async def delete_repository_index(self, repository_id: str) -> None:
        """
        Delete repository index from memory
        
        Args:
            repository_id: Repository ID
        """
        try:
            if repository_id in self.repository_data:
                del self.repository_data[repository_id]
                print(f"Deleted index for repository {repository_id}")
        except Exception as e:
            print(f"Failed to delete index: {e}")
