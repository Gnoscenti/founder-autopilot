"""Tool permissions and access control."""
from typing import List, Dict, Set
from enum import Enum


class ToolPermission(str, Enum):
    """Available tool permissions."""
    FILESYSTEM = "filesystem"
    SHELL = "shell"
    GIT = "git"
    STRIPE = "stripe"
    GCLOUD = "gcloud"
    PLAYWRIGHT = "playwright"
    EMAIL = "email"
    SOCIAL = "social"


class PermissionLevel(str, Enum):
    """Permission levels for tools."""
    NONE = "none"
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


# Default permissions for each agent type
AGENT_PERMISSIONS: Dict[str, Set[ToolPermission]] = {
    "orchestrator": {
        ToolPermission.FILESYSTEM,
        ToolPermission.SHELL,
        ToolPermission.GIT,
    },
    "business_builder": {
        ToolPermission.FILESYSTEM,
    },
    "webdev": {
        ToolPermission.FILESYSTEM,
        ToolPermission.SHELL,
        ToolPermission.GIT,
        ToolPermission.PLAYWRIGHT,
    },
    "stripe_agent": {
        ToolPermission.FILESYSTEM,
        ToolPermission.STRIPE,
        ToolPermission.PLAYWRIGHT,
    },
    "marketing": {
        ToolPermission.FILESYSTEM,
        ToolPermission.EMAIL,
        ToolPermission.SOCIAL,
        ToolPermission.PLAYWRIGHT,
    },
    "reviewer": {
        ToolPermission.FILESYSTEM,
    },
}


# Dangerous operations that require human approval
REQUIRES_HUMAN_APPROVAL = {
    "stripe_create_product",
    "stripe_create_price",
    "stripe_create_webhook",
    "email_send_campaign",
    "social_post_content",
    "shell_sudo",
    "git_push",
    "playwright_submit_form",
}


class PermissionManager:
    """Manages tool permissions for agents."""
    
    def __init__(self):
        self.agent_permissions = AGENT_PERMISSIONS.copy()
        self.requires_approval = REQUIRES_HUMAN_APPROVAL.copy()
    
    def has_permission(self, agent_name: str, tool: ToolPermission) -> bool:
        """Check if an agent has permission to use a tool."""
        if agent_name not in self.agent_permissions:
            return False
        return tool in self.agent_permissions[agent_name]
    
    def grant_permission(self, agent_name: str, tool: ToolPermission):
        """Grant a tool permission to an agent."""
        if agent_name not in self.agent_permissions:
            self.agent_permissions[agent_name] = set()
        self.agent_permissions[agent_name].add(tool)
    
    def revoke_permission(self, agent_name: str, tool: ToolPermission):
        """Revoke a tool permission from an agent."""
        if agent_name in self.agent_permissions:
            self.agent_permissions[agent_name].discard(tool)
    
    def requires_human_approval(self, operation: str) -> bool:
        """Check if an operation requires human approval."""
        return operation in self.requires_approval
    
    def get_agent_permissions(self, agent_name: str) -> List[str]:
        """Get all permissions for an agent."""
        if agent_name not in self.agent_permissions:
            return []
        return [p.value for p in self.agent_permissions[agent_name]]


# Global permission manager instance
permission_manager = PermissionManager()
