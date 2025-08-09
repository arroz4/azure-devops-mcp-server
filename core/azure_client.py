"""Azure DevOps API client for work item operations."""

import requests
from typing import Dict, Any, Optional
from core.config import get_current_config, get_auth_headers, get_json_patch_headers


class AzureDevOpsClient:
    """Client for Azure DevOps REST API operations."""
    
    def __init__(self):
        """Initialize the Azure DevOps client."""
        self.config = get_current_config()
        self.base_url = (f"https://dev.azure.com/{self.config['organization']}/"
                        f"{self.config['project']}/_apis/wit")
    
    def create_work_item(self, work_item_type: str, 
                        fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a work item in Azure DevOps.
        
        Args:
            work_item_type: Type of work item (Task, Epic, etc.)
            fields: Dictionary of field values
            
        Returns:
            Dict containing the created work item data
        """
        url = f"{self.base_url}/workitems/${work_item_type}?api-version=7.1"
        
        # Convert fields to JSON Patch format
        patch_document = []
        for field_name, field_value in fields.items():
            if field_value is not None and field_value != "":
                patch_document.append({
                    "op": "add",
                    "path": f"/fields/{field_name}",
                    "value": field_value
                })
        
        response = requests.post(
            url,
            json=patch_document,
            headers=get_json_patch_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_work_item(self, work_item_id: int, 
                     expand: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a work item by ID.
        
        Args:
            work_item_id: The work item ID
            expand: Optional expansion parameters
            
        Returns:
            Dict containing the work item data
        """
        url = f"{self.base_url}/workitems/{work_item_id}?api-version=7.1"
        if expand:
            url += f"&$expand={expand}"
        
        response = requests.get(url, headers=get_auth_headers())
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def update_work_item(self, work_item_id: int, 
                        fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a work item.
        
        Args:
            work_item_id: The work item ID
            fields: Dictionary of field values to update
            
        Returns:
            Dict containing the updated work item data
        """
        url = f"{self.base_url}/workitems/{work_item_id}?api-version=7.1"
        
        # Convert fields to JSON Patch format
        patch_document = []
        for field_name, field_value in fields.items():
            if field_value is not None:
                if field_value == "":
                    # Remove field if empty string
                    patch_document.append({
                        "op": "remove",
                        "path": f"/fields/{field_name}"
                    })
                else:
                    # Add or update field
                    patch_document.append({
                        "op": "add",
                        "path": f"/fields/{field_name}",
                        "value": field_value
                    })
        
        response = requests.patch(
            url,
            json=patch_document,
            headers=get_json_patch_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
    
    def delete_work_item(self, work_item_id: int) -> bool:
        """
        Delete a work item.
        
        Args:
            work_item_id: The work item ID
            
        Returns:
            bool: True if deletion was successful
        """
        url = f"{self.base_url}/workitems/{work_item_id}?api-version=7.1"
        
        response = requests.delete(url, headers=get_auth_headers())
        
        return response.status_code == 200
    
    def create_work_item_link(self, source_id: int, target_id: int, 
                             link_type: str = "System.LinkTypes.Hierarchy-Forward") -> bool:
        """
        Create a link between two work items.
        
        Args:
            source_id: Source work item ID (parent)
            target_id: Target work item ID (child)
            link_type: Type of link to create
            
        Returns:
            bool: True if link creation was successful
        """
        url = f"{self.base_url}/workitems/{source_id}?api-version=7.1"
        
        patch_document = [{
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": link_type,
                "url": (f"https://dev.azure.com/{self.config['organization']}/"
                       f"{self.config['project']}/_apis/wit/workItems/{target_id}")
            }
        }]
        
        response = requests.patch(
            url,
            json=patch_document,
            headers=get_json_patch_headers()
        )
        
        return response.status_code == 200
