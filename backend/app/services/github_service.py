"""
GitHub integration service
"""
from github import Github, GithubException
from typing import Dict, List, Optional, Any
import base64

from app.core.config import settings


class GitHubService:
    """Service for GitHub API integration"""
    
    def __init__(self):
        self.client = Github(settings.GITHUB_TOKEN)
    
    def parse_github_url(self, url: str) -> tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo name
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Tuple of (owner, repo_name)
        """
        # Remove trailing slashes and .git
        url = url.rstrip('/').replace('.git', '')
        
        # Extract owner and repo from URL
        parts = url.split('github.com/')[-1].split('/')
        if len(parts) >= 2:
            return parts[0], parts[1]
        raise ValueError("Invalid GitHub URL format")
    
    async def get_repository_info(self, github_url: str) -> Dict[str, Any]:
        """
        Get repository information
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Repository metadata
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            return {
                "name": repo.name,
                "owner": owner,
                "default_branch": repo.default_branch,
                "description": repo.description,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count,
                "language": repo.language,
                "size_kb": repo.size,
                "topics": repo.get_topics(),
                "created_at": repo.created_at.isoformat(),
                "updated_at": repo.updated_at.isoformat(),
            }
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to fetch repository: {e}")
    
    async def get_repository_structure(
        self, 
        github_url: str, 
        branch: str = "main"
    ) -> List[Dict[str, Any]]:
        """
        Get repository file structure
        
        Args:
            github_url: GitHub repository URL
            branch: Branch name
            
        Returns:
            List of file/directory nodes
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            # Get repository contents recursively
            contents = repo.get_contents("", ref=branch)
            tree = []
            
            while contents:
                file_content = contents.pop(0)
                node = {
                    "path": file_content.path,
                    "type": file_content.type,
                    "size": file_content.size if file_content.type == "file" else None,
                }
                
                if file_content.type == "dir":
                    node["children"] = []
                    # Get directory contents
                    dir_contents = repo.get_contents(file_content.path, ref=branch)
                    contents.extend(dir_contents)
                
                tree.append(node)
            
            return tree
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to fetch repository structure: {e}")
    
    async def get_file_content(
        self, 
        github_url: str, 
        file_path: str, 
        branch: str = "main"
    ) -> Dict[str, Any]:
        """
        Get file content from repository
        
        Args:
            github_url: GitHub repository URL
            file_path: Path to file
            branch: Branch name
            
        Returns:
            File content and metadata
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            file_content = repo.get_contents(file_path, ref=branch)
            
            # Decode content
            content = base64.b64decode(file_content.content).decode('utf-8')
            
            return {
                "path": file_content.path,
                "content": content,
                "size": file_content.size,
                "sha": file_content.sha,
            }
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to fetch file content: {e}")
    
    async def get_pull_request(
        self, 
        github_url: str, 
        pr_number: int
    ) -> Dict[str, Any]:
        """
        Get pull request information
        
        Args:
            github_url: GitHub repository URL
            pr_number: Pull request number
            
        Returns:
            Pull request data
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            pr = repo.get_pull(pr_number)
            
            # Get changed files
            files = []
            for file in pr.get_files():
                files.append({
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch,
                })
            
            return {
                "number": pr.number,
                "title": pr.title,
                "body": pr.body,
                "state": pr.state,
                "author": pr.user.login,
                "created_at": pr.created_at.isoformat(),
                "updated_at": pr.updated_at.isoformat(),
                "files": files,
            }
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to fetch pull request: {e}")
    
    async def list_pull_requests(
        self, 
        github_url: str, 
        state: str = "open"
    ) -> List[Dict[str, Any]]:
        """
        List pull requests
        
        Args:
            github_url: GitHub repository URL
            state: PR state (open, closed, all)
            
        Returns:
            List of pull requests
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            prs = repo.get_pulls(state=state)
            
            return [
                {
                    "number": pr.number,
                    "title": pr.title,
                    "state": pr.state,
                    "author": pr.user.login,
                    "created_at": pr.created_at.isoformat(),
                }
                for pr in prs
            ]
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to list pull requests: {e}")
    
    async def get_repository_languages(self, github_url: str) -> Dict[str, int]:
        """
        Get repository programming languages
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Dictionary of languages and their byte counts
        """
        try:
            owner, repo_name = self.parse_github_url(github_url)
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            
            return repo.get_languages()
        except GithubException as e:
            print(f"GitHub API error: {e}")
            raise ValueError(f"Failed to fetch repository languages: {e}")
