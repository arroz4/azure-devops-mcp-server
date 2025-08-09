"""Configuration management for Azure DevOps MCP Server."""

import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class WorkItemType(Enum):
    """Enumeration for Azure DevOps work item types."""
    TASK = "Task"
    EPIC = "Epic"


def get_current_config():
    """
    Get current Azure DevOps configuration from environment variables.
    Supports both old and new environment variable naming conventions.
    
    Returns:
        dict: Configuration containing organization, project, and token
    """
    # Try new naming convention first, then fall back to old convention
    organization = (os.getenv("AZURE_DEVOPS_ORGANIZATION") or
                    os.getenv("AZURE_DEVOPS_ORGANIZATION_URL", "")
                    .replace("https://dev.azure.com/", ""))
    project = os.getenv("AZURE_DEVOPS_PROJECT")
    token = os.getenv("AZURE_DEVOPS_TOKEN") or os.getenv("AZURE_DEVOPS_PAT")
    
    if not all([organization, project, token]):
        missing = []
        if not organization:
            missing.append("AZURE_DEVOPS_ORGANIZATION or "
                           "AZURE_DEVOPS_ORGANIZATION_URL")
        if not project:
            missing.append("AZURE_DEVOPS_PROJECT")
        if not token:
            missing.append("AZURE_DEVOPS_TOKEN or AZURE_DEVOPS_PAT")
        missing_vars = ', '.join(missing)
        raise ValueError(f"Missing required environment variables: "
                         f"{missing_vars}")
    
    return {
        "organization": organization,
        "project": project,
        "token": token
    }


def build_workitem_url(work_item_id: int) -> str:
    """
    Build the Azure DevOps work item URL.
    
    Args:
        work_item_id: The work item ID
        
    Returns:
        str: Complete Azure DevOps work item URL
    """
    config = get_current_config()
    org = config['organization']
    proj = config['project']
    return f"https://dev.azure.com/{org}/{proj}/_workitems/edit/{work_item_id}"


def get_auth_headers() -> dict:
    """
    Get authentication headers for Azure DevOps API requests.
    
    Returns:
        dict: Headers with authorization token
    """
    config = get_current_config()
    import base64
    
    credentials = base64.b64encode(f":{config['token']}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json-patch+json"
    }


def get_json_patch_headers() -> dict:
    """
    Get headers for JSON Patch requests to Azure DevOps API.
    
    Returns:
        dict: Headers for JSON Patch operations
    """
    return get_auth_headers()
