"""Shell tool - execute shell commands safely."""
import subprocess
from typing import Dict, Any, List, Optional


class ShellTool:
    """Tool for executing shell commands."""
    
    def __init__(self, workspace_root: str, allowed_commands: Optional[List[str]] = None):
        self.workspace_root = workspace_root
        self.allowed_commands = allowed_commands or [
            "npm", "pnpm", "yarn", "node",
            "python", "pip",
            "git",
            "vercel", "netlify",
            "gcloud",
            "ls", "cat", "mkdir", "cp", "mv",
        ]
    
    def execute(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 60
    ) -> Dict[str, Any]:
        """Execute a shell command safely."""
        
        # Parse command
        parts = command.split()
        if not parts:
            return {"success": False, "error": "Empty command"}
        
        base_command = parts[0]
        
        # Security: check if command is allowed
        if base_command not in self.allowed_commands:
            return {
                "success": False,
                "error": f"Command '{base_command}' not allowed. Allowed: {', '.join(self.allowed_commands)}"
            }
        
        # Set working directory
        work_dir = cwd or self.workspace_root
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=work_dir,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds"
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def npm_install(self, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Run npm install."""
        return self.execute("npm install", cwd=cwd, timeout=300)
    
    def git_init(self, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Initialize git repository."""
        return self.execute("git init", cwd=cwd)
    
    def deploy_vercel(self, cwd: Optional[str] = None) -> Dict[str, Any]:
        """Deploy to Vercel."""
        return self.execute("vercel --prod", cwd=cwd, timeout=300)
