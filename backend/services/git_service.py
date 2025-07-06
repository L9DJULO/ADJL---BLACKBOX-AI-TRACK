import os
import git
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import tempfile
import shutil

logger = logging.getLogger(__name__)

class GitService:
    """Service for Git version control operations"""
    
    def __init__(self):
        self.repos = {}  # Cache for repository objects
        self.temp_dirs = []  # Track temporary directories
    
    def is_available(self) -> bool:
        """Check if Git service is available"""
        try:
            git.cmd.Git().version()
            return True
        except Exception:
            return False
    
    def clone_repository(self, repo_url: str, local_path: Optional[str] = None) -> Dict[str, Any]:
        """Clone a repository"""
        try:
            if not local_path:
                local_path = tempfile.mkdtemp()
                self.temp_dirs.append(local_path)
            
            repo = git.Repo.clone_from(repo_url, local_path)
            self.repos[local_path] = repo
            
            return {
                "success": True,
                "local_path": local_path,
                "repo_url": repo_url,
                "current_branch": repo.active_branch.name,
                "commit_count": len(list(repo.iter_commits()))
            }
            
        except Exception as e:
            logger.error(f"Error cloning repository: {e}")
            return {"success": False, "error": str(e)}
    
    def get_repo_info(self, repo_path: str) -> Dict[str, Any]:
        """Get repository information"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            # Get basic info
            info = {
                "success": True,
                "path": repo_path,
                "current_branch": repo.active_branch.name,
                "is_dirty": repo.is_dirty(),
                "untracked_files": repo.untracked_files,
                "remote_url": None,
                "commit_count": len(list(repo.iter_commits())),
                "branches": [branch.name for branch in repo.branches],
                "tags": [tag.name for tag in repo.tags]
            }
            
            # Get remote URL if exists
            if repo.remotes:
                info["remote_url"] = repo.remotes.origin.url
            
            # Get recent commits
            recent_commits = []
            for commit in repo.iter_commits(max_count=10):
                recent_commits.append({
                    "hash": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": commit.author.name,
                    "date": commit.committed_datetime.isoformat(),
                    "files_changed": len(commit.stats.files)
                })
            
            info["recent_commits"] = recent_commits
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting repo info: {e}")
            return {"success": False, "error": str(e)}
    
    def get_file_content(self, repo_path: str, file_path: str, branch: str = None) -> Dict[str, Any]:
        """Get content of a file from the repository"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            if branch and branch != repo.active_branch.name:
                repo.git.checkout(branch)
            
            full_path = os.path.join(repo_path, file_path)
            if not os.path.exists(full_path):
                return {"success": False, "error": "File not found"}
            
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                "success": True,
                "file_path": file_path,
                "content": content,
                "branch": repo.active_branch.name,
                "last_modified": datetime.fromtimestamp(os.path.getmtime(full_path)).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            return {"success": False, "error": str(e)}
    
    def get_file_history(self, repo_path: str, file_path: str, max_commits: int = 10) -> Dict[str, Any]:
        """Get commit history for a specific file"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            commits = []
            for commit in repo.iter_commits(paths=file_path, max_count=max_commits):
                commits.append({
                    "hash": commit.hexsha[:8],
                    "message": commit.message.strip(),
                    "author": commit.author.name,
                    "date": commit.committed_datetime.isoformat(),
                    "changes": self._get_file_changes(repo, commit, file_path)
                })
            
            return {
                "success": True,
                "file_path": file_path,
                "commits": commits
            }
            
        except Exception as e:
            logger.error(f"Error getting file history: {e}")
            return {"success": False, "error": str(e)}
    
    def get_diff(self, repo_path: str, commit1: str = None, commit2: str = None) -> Dict[str, Any]:
        """Get diff between commits or working directory"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            if commit1 and commit2:
                # Diff between two commits
                diff = repo.git.diff(commit1, commit2)
            elif commit1:
                # Diff between commit and working directory
                diff = repo.git.diff(commit1)
            else:
                # Diff of working directory changes
                diff = repo.git.diff()
            
            return {
                "success": True,
                "diff": diff,
                "commit1": commit1,
                "commit2": commit2
            }
            
        except Exception as e:
            logger.error(f"Error getting diff: {e}")
            return {"success": False, "error": str(e)}
    
    def get_changed_files(self, repo_path: str) -> Dict[str, Any]:
        """Get list of changed files"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            changed_files = []
            
            # Modified files
            for item in repo.index.diff(None):
                changed_files.append({
                    "file": item.a_path,
                    "status": "modified",
                    "change_type": item.change_type
                })
            
            # Staged files
            for item in repo.index.diff("HEAD"):
                changed_files.append({
                    "file": item.a_path,
                    "status": "staged",
                    "change_type": item.change_type
                })
            
            # Untracked files
            for file in repo.untracked_files:
                changed_files.append({
                    "file": file,
                    "status": "untracked",
                    "change_type": "new"
                })
            
            return {
                "success": True,
                "changed_files": changed_files,
                "total_changes": len(changed_files)
            }
            
        except Exception as e:
            logger.error(f"Error getting changed files: {e}")
            return {"success": False, "error": str(e)}
    
    def analyze_code_changes(self, repo_path: str, file_path: str = None) -> Dict[str, Any]:
        """Analyze code changes for insights"""
        try:
            repo = self._get_repo(repo_path)
            if not repo:
                return {"success": False, "error": "Repository not found"}
            
            analysis = {
                "success": True,
                "repository": repo_path,
                "analysis_date": datetime.utcnow().isoformat(),
                "metrics": {}
            }
            
            # Get commits for analysis
            commits = list(repo.iter_commits(max_count=100))
            
            # Analyze commit patterns
            analysis["metrics"]["total_commits"] = len(commits)
            analysis["metrics"]["contributors"] = len(set(commit.author.name for commit in commits))
            
            # Analyze file changes
            if file_path:
                file_commits = list(repo.iter_commits(paths=file_path, max_count=50))
                analysis["metrics"]["file_commits"] = len(file_commits)
                
                # Calculate change frequency
                if file_commits:
                    first_commit = file_commits[-1]
                    last_commit = file_commits[0]
                    days_diff = (last_commit.committed_datetime - first_commit.committed_datetime).days
                    if days_diff > 0:
                        analysis["metrics"]["change_frequency"] = len(file_commits) / days_diff
            
            # Language analysis
            language_stats = self._analyze_languages(repo_path)
            analysis["metrics"]["languages"] = language_stats
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing code changes: {e}")
            return {"success": False, "error": str(e)}
    
    def _get_repo(self, repo_path: str) -> Optional[git.Repo]:
        """Get or create repository object"""
        try:
            if repo_path not in self.repos:
                if os.path.exists(repo_path):
                    self.repos[repo_path] = git.Repo(repo_path)
                else:
                    return None
            
            return self.repos[repo_path]
            
        except Exception as e:
            logger.error(f"Error getting repo: {e}")
            return None
    
    def _get_file_changes(self, repo: git.Repo, commit: git.Commit, file_path: str) -> Dict[str, Any]:
        """Get changes made to a file in a specific commit"""
        try:
            if commit.parents:
                diffs = commit.diff(commit.parents[0], paths=file_path)
                if diffs:
                    diff = diffs[0]
                    return {
                        "lines_added": diff.inserted_lines if hasattr(diff, 'inserted_lines') else 0,
                        "lines_removed": diff.deleted_lines if hasattr(diff, 'deleted_lines') else 0,
                        "change_type": diff.change_type
                    }
            
            return {"lines_added": 0, "lines_removed": 0, "change_type": "A"}
            
        except Exception as e:
            logger.error(f"Error getting file changes: {e}")
            return {"lines_added": 0, "lines_removed": 0, "change_type": "unknown"}
    
    def _analyze_languages(self, repo_path: str) -> Dict[str, int]:
        """Analyze programming languages in the repository"""
        language_extensions = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.html': 'HTML',
            '.css': 'CSS',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.md': 'Markdown'
        }
        
        language_stats = {}
        
        try:
            for root, dirs, files in os.walk(repo_path):
                # Skip .git directory
                if '.git' in root:
                    continue
                
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in language_extensions:
                        lang = language_extensions[ext]
                        language_stats[lang] = language_stats.get(lang, 0) + 1
            
            return language_stats
            
        except Exception as e:
            logger.error(f"Error analyzing languages: {e}")
            return {}
    
    def cleanup_temp_dirs(self):
        """Clean up temporary directories"""
        for temp_dir in self.temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
                    logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.error(f"Error cleaning up {temp_dir}: {e}")
        
        self.temp_dirs.clear()
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.cleanup_temp_dirs()