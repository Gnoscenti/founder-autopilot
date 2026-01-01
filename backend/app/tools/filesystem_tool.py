"""Filesystem tool - read/write files and manage directories."""
from pathlib import Path
from typing import Optional, List
import json


class FilesystemTool:
    """Tool for filesystem operations."""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.workspace_root.mkdir(parents=True, exist_ok=True)
    
    def _resolve_path(self, path: str) -> Path:
        """Resolve and validate path within workspace."""
        full_path = (self.workspace_root / path).resolve()
        
        # Security: ensure path is within workspace
        if not str(full_path).startswith(str(self.workspace_root)):
            raise ValueError(f"Path {path} is outside workspace")
        
        return full_path
    
    def read_file(self, path: str) -> str:
        """Read file contents."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        
        return full_path.read_text(encoding="utf-8")
    
    def write_file(self, path: str, content: str):
        """Write content to file."""
        full_path = self._resolve_path(path)
        
        # Create parent directories
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        full_path.write_text(content, encoding="utf-8")
    
    def append_file(self, path: str, content: str):
        """Append content to file."""
        existing = ""
        try:
            existing = self.read_file(path)
        except FileNotFoundError:
            pass
        
        self.write_file(path, existing + content)
    
    def list_directory(self, path: str = ".") -> List[str]:
        """List files and directories."""
        full_path = self._resolve_path(path)
        
        if not full_path.exists():
            raise FileNotFoundError(f"Directory not found: {path}")
        
        if not full_path.is_dir():
            raise ValueError(f"Not a directory: {path}")
        
        return [item.name for item in full_path.iterdir()]
    
    def create_directory(self, path: str):
        """Create directory."""
        full_path = self._resolve_path(path)
        full_path.mkdir(parents=True, exist_ok=True)
    
    def delete_file(self, path: str):
        """Delete file."""
        full_path = self._resolve_path(path)
        
        if full_path.exists() and full_path.is_file():
            full_path.unlink()
    
    def file_exists(self, path: str) -> bool:
        """Check if file exists."""
        try:
            full_path = self._resolve_path(path)
            return full_path.exists() and full_path.is_file()
        except ValueError:
            return False
    
    def save_json(self, path: str, data: dict):
        """Save data as JSON."""
        content = json.dumps(data, indent=2)
        self.write_file(path, content)
    
    def load_json(self, path: str) -> dict:
        """Load JSON file."""
        content = self.read_file(path)
        return json.loads(content)
