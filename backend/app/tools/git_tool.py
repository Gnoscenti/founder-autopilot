"""Git tool - version control operations."""
from typing import Dict, Any, Optional
from pathlib import Path
import subprocess


class GitTool:
    """Tool for Git operations."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
    
    def _run_git(self, args: list, cwd: Optional[Path] = None) -> Dict[str, Any]:
        """Run git command."""
        work_dir = cwd or self.workspace_root
        
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def init(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Initialize git repository."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["init"], cwd=repo_path)
    
    def add(self, files: str = ".", path: Optional[str] = None) -> Dict[str, Any]:
        """Stage files."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["add", files], cwd=repo_path)
    
    def commit(self, message: str, path: Optional[str] = None) -> Dict[str, Any]:
        """Commit changes."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["commit", "-m", message], cwd=repo_path)
    
    def status(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Get repository status."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["status"], cwd=repo_path)
    
    def remote_add(self, name: str, url: str, path: Optional[str] = None) -> Dict[str, Any]:
        """Add remote repository."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["remote", "add", name, url], cwd=repo_path)
    
    def push(self, remote: str = "origin", branch: str = "main", path: Optional[str] = None) -> Dict[str, Any]:
        """Push to remote (requires human approval)."""
        repo_path = Path(path) if path else self.workspace_root
        return self._run_git(["push", remote, branch], cwd=repo_path)
