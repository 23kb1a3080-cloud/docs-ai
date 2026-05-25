"""
AI service for documentation generation and chat
Simplified version using OpenAI only
"""
from typing import List, Dict, Any, Optional
import openai

from app.core.config import settings


class AIService:
    """Service for AI-powered documentation generation"""
    
    def __init__(self):
        # Use OpenAI only for simplified demo
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = getattr(settings, 'LLM_MODEL', 'gpt-4-turbo-preview')
    
    async def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = None
    ) -> str:
        """
        Generate AI completion using OpenAI
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Temperature for generation
            
        Returns:
            Generated text
        """
        temp = temperature or getattr(settings, 'LLM_TEMPERATURE', 0.7)
        max_tokens = getattr(settings, 'LLM_MAX_TOKENS', 4000)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"AI generation error: {e}")
            raise ValueError(f"Failed to generate completion: {e}")
    
    async def generate_chat_response(
        self,
        message: str,
        history: List[Dict[str, str]] = None
    ) -> str:
        """
        Generate chat response (simplified without RAG)
        
        Args:
            message: User message
            history: Chat history
            
        Returns:
            AI response
        """
        system_prompt = """You are a helpful AI assistant for developers. 
Answer questions about code, documentation, and software development."""
        
        try:
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add history
            if history:
                messages.extend(history[-10:])  # Last 10 messages
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Chat generation error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    async def generate_readme(
        self, 
        repo_info: Dict[str, Any], 
        file_structure: List[Dict[str, Any]],
        sample_files: Dict[str, str]
    ) -> str:
        """
        Generate README documentation
        
        Args:
            repo_info: Repository metadata
            file_structure: Repository file structure
            sample_files: Sample file contents
            
        Returns:
            Generated README content
        """
        system_prompt = """You are an expert technical writer specializing in software documentation.
Generate comprehensive, well-structured README documentation for GitHub repositories."""
        
        prompt = f"""Generate a comprehensive README.md for this repository:

Repository Information:
- Name: {repo_info.get('name')}
- Description: {repo_info.get('description', 'N/A')}
- Language: {repo_info.get('language', 'N/A')}
- Topics: {', '.join(repo_info.get('topics', []))}

File Structure:
{self._format_file_structure(file_structure[:20])}

Sample Files:
{self._format_sample_files(sample_files)}

Generate a README with these sections:
1. Project Title and Description
2. Features
3. Installation
4. Usage
5. Project Structure
6. Contributing
7. License

Use markdown formatting. Be concise but informative."""
        
        return await self.generate_completion(prompt, system_prompt)
    
    async def generate_api_documentation(
        self, 
        api_files: Dict[str, str]
    ) -> str:
        """
        Generate API documentation
        
        Args:
            api_files: API-related file contents
            
        Returns:
            Generated API documentation
        """
        system_prompt = """You are an expert at analyzing code and generating API documentation.
Extract endpoints, parameters, and responses from code."""
        
        prompt = f"""Analyze these API files and generate comprehensive API documentation:

{self._format_sample_files(api_files)}

Generate documentation with:
1. API Overview
2. Base URL
3. Authentication
4. Endpoints (method, path, parameters, responses)
5. Error Codes
6. Examples

Use markdown formatting with code blocks."""
        
        return await self.generate_completion(prompt, system_prompt)
    
    async def generate_architecture_doc(
        self, 
        repo_info: Dict[str, Any],
        file_structure: List[Dict[str, Any]],
        key_files: Dict[str, str]
    ) -> str:
        """
        Generate architecture documentation
        
        Args:
            repo_info: Repository metadata
            file_structure: Repository file structure
            key_files: Key file contents
            
        Returns:
            Generated architecture documentation
        """
        system_prompt = """You are a software architect expert at analyzing codebases and documenting system architecture."""
        
        prompt = f"""Analyze this codebase and generate architecture documentation:

Repository: {repo_info.get('name')}
Language: {repo_info.get('language')}

File Structure:
{self._format_file_structure(file_structure[:30])}

Key Files:
{self._format_sample_files(key_files)}

Generate documentation with:
1. System Overview
2. Architecture Pattern (MVC, Microservices, etc.)
3. Component Breakdown
4. Data Flow
5. Technology Stack
6. Design Decisions

Include a Mermaid diagram showing the architecture."""
        
        return await self.generate_completion(prompt, system_prompt)
    
    async def analyze_pr_changes(
        self, 
        pr_info: Dict[str, Any],
        changed_files: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze pull request changes
        
        Args:
            pr_info: Pull request information
            changed_files: List of changed files
            
        Returns:
            Analysis results
        """
        system_prompt = """You are a code review expert. Analyze pull request changes and provide insights."""
        
        files_summary = "\n".join([
            f"- {f['filename']} ({f['status']}): +{f['additions']} -{f['deletions']}"
            for f in changed_files[:10]
        ])
        
        prompt = f"""Analyze this pull request:

Title: {pr_info['title']}
Description: {pr_info.get('body', 'N/A')}

Changed Files:
{files_summary}

Provide:
1. Summary of changes (2-3 sentences)
2. Affected modules/components
3. Breaking changes (yes/no)
4. Documentation update suggestions

Return as JSON with keys: summary, affected_modules (array), breaking_changes (boolean), suggestions (array)"""
        
        response = await self.generate_completion(prompt, system_prompt, temperature=0.3)
        
        # Parse JSON response (simplified - add proper parsing)
        return {
            "summary": response,
            "affected_modules": [],
            "breaking_changes": False,
        }
    
    async def detect_undocumented_code(
        self, 
        file_content: str,
        file_path: str
    ) -> List[Dict[str, Any]]:
        """
        Detect undocumented functions and classes
        
        Args:
            file_content: File content
            file_path: File path
            
        Returns:
            List of undocumented items
        """
        system_prompt = """You are a code quality expert. Identify undocumented functions and classes."""
        
        prompt = f"""Analyze this code file and identify undocumented functions/classes:

File: {file_path}

```
{file_content[:2000]}
```

List all functions and classes that lack documentation (docstrings/comments).
For each, provide: name, line number, severity (high/medium/low), suggestion."""
        
        response = await self.generate_completion(prompt, system_prompt, temperature=0.2)
        
        # Simplified - implement proper parsing
        return []
    
    def _format_file_structure(self, structure: List[Dict[str, Any]]) -> str:
        """Format file structure for prompt"""
        lines = []
        for item in structure:
            indent = "  " * item['path'].count('/')
            lines.append(f"{indent}- {item['path']} ({item['type']})")
        return "\n".join(lines[:50])
    
    def _format_sample_files(self, files: Dict[str, str]) -> str:
        """Format sample files for prompt"""
        lines = []
        for path, content in list(files.items())[:5]:
            lines.append(f"\n### {path}\n```\n{content[:500]}\n```")
        return "\n".join(lines)
