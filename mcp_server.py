"""
Azure DevOps MCP Server - Modular Version
Manages Azure DevOps work items through Model Context Protocol.
"""

import logging
import os
import sys

from fastmcp import FastMCP

# Add current directory to Python path for module imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modular components
from core.config import get_current_config
from services.work_items import WorkItemService
from utils.helpers import setup_logging, format_error_message

# Initialize logging
setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MCP server
mcp = FastMCP("Azure DevOps MCP Server")

# Initialize services
work_item_service = WorkItemService()


@mcp.tool()
def create_work_item(
    work_item_type: str,
    title: str,
    description: str = "",
    assigned_to: str = "",
    priority: int = None,
    tags: str = ""
) -> str:
    """
    Creates a new work item in Azure DevOps.

    Uses helper function:
    - _create_work_item_internal() - Handles the actual work item creation

    Args:
        work_item_type: The type of work item to create ("Task" or "Epic")
        title: The title of the work item
        description: Description of the work item. For Tasks, follow
                    Work Item ID 89 comprehensive structure with all required
                    sections: Objective, Technical Requirements, Implementation
                    Steps, Acceptance Criteria, and Business Context
        assigned_to: Email address of the person to assign
        priority: Priority level (1-4, where 1 is highest)
        tags: Semicolon-separated tags

    Returns:
        URL of the created work item if successful, error message otherwise
    """
    try:
        return work_item_service.create_work_item(
            work_item_type=work_item_type,
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            tags=tags
        )
    except Exception as e:
        logger.error(f"Error creating work item: {e}")
        return format_error_message("create_work_item", e)


@mcp.tool()
def create_epic_with_tasks(
    epic_title: str,
    epic_description: str = "",
    task_titles: str = "",
    task_descriptions: str = "",
    assigned_to: str = "",
    priority: int = None,
    tags: str = ""
) -> str:
    """
    Creates an Epic with multiple Tasks and links them together.
    
    Provides a comprehensive summary with URLs.

    This is the RECOMMENDED workflow for creating Epics with multiple
    tasks in a single operation. The function automatically creates all
    work items, establishes parent-child relationships, and provides
    a detailed breakdown table with URLs for immediate access.

    Uses helper functions:
    - _create_work_item_internal() - Creates both the Epic and all Tasks
    - _link_task_to_epic_internal() - Links each Task to the Epic

    Args:
        epic_title: The title of the Epic to create
        epic_description: Description of the Epic (supports HTML formatting)
        task_titles: Comma-separated list of Task titles
        task_descriptions: Comma-separated list of COMPREHENSIVE Task
                          descriptions. Each description MUST follow the
                          proven structure from Work Item ID 89.
        assigned_to: Email address to assign the Epic and Tasks to
        priority: Priority level (1-4, where 1 is highest)
        tags: Semicolon-separated tags to apply to all work items

    Returns:
        Comprehensive summary table with Epic and Task URLs, linking
        status, and next steps. This breakdown provides immediate access
        to all created work items with their direct Azure DevOps URLs.
    """
    try:
        return work_item_service.create_epic_with_tasks(
            epic_title=epic_title,
            epic_description=epic_description,
            task_titles=task_titles,
            task_descriptions=task_descriptions,
            assigned_to=assigned_to,
            priority=priority,
            tags=tags
        )
    except Exception as e:
        logger.error(f"Error creating epic with tasks: {e}")
        return format_error_message("create_epic_with_tasks", e)


@mcp.tool()
def get_work_item(item_id: int) -> str:
    """
    Retrieves detailed information about a work item from Azure DevOps.
    
    For Epics, automatically shows a comprehensive table of all linked
    child work items with their URLs.

    This function is particularly useful when you need to see the complete
    breakdown of an Epic with all its associated Tasks, including direct
    URLs for quick access to each work item.

    Uses helper functions:
    - build_workitem_url() - Constructs the Azure DevOps API URL for
                            the work item with relations expansion
    - get_auth_headers() - Creates proper authorization headers

    Args:
        item_id: The ID of the work item to retrieve

    Returns:
        Formatted work item details if successful, error message otherwise.
        For Epics: Includes a complete breakdown table showing all child
        Tasks with IDs, titles, states, assignees, and direct Azure DevOps
        URLs for immediate access.
    """
    try:
        return work_item_service.get_work_item(item_id)
    except Exception as e:
        logger.error(f"Error getting work item {item_id}: {e}")
        return format_error_message("get_work_item", e)


@mcp.tool()
def update_work_item(
    item_id: int,
    title: str = None,
    description: str = None,
    assigned_to: str = None,
    priority: int = None,
    tags: str = None
) -> str:
    """
    Updates an existing work item in Azure DevOps.

    Uses helper functions:
    - process_description_text() - Converts escape sequences to proper
                                  HTML paragraph formatting
    - build_workitem_url() - Constructs the Azure DevOps API URL
    - get_json_patch_headers() - Creates proper headers for JSON Patch

    Args:
        item_id: The ID of the work item to update
        title: New title for the work item
        description: New description for Tasks should follow Work Item ID 89
                    comprehensive structure with Objective, Technical
                    Requirements, Implementation Steps, Acceptance Criteria,
                    and Business Context sections
        assigned_to: Email address to assign or "" to unassign
        priority: New priority level (1-4)
        tags: New tags or "" to remove all tags

    Returns:
        Success message with URL if successful, error message otherwise
    """
    try:
        return work_item_service.update_work_item(
            item_id=item_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            tags=tags
        )
    except Exception as e:
        logger.error(f"Error updating work item {item_id}: {e}")
        return format_error_message("update_work_item", e)


@mcp.tool()
def delete_work_item(item_id: int) -> str:
    """
    Deletes a work item from Azure DevOps.

    Uses helper functions:
    - build_workitem_url() - Constructs the Azure DevOps API URL
    - get_auth_headers() - Creates proper authorization headers

    Args:
        item_id: The ID of the work item to delete

    Returns:
        Success message if deletion was successful, error message otherwise
    """
    try:
        return work_item_service.delete_work_item(item_id)
    except Exception as e:
        logger.error(f"Error deleting work item {item_id}: {e}")
        return format_error_message("delete_work_item", e)


@mcp.tool()
def link_task_to_epic(epic_id: int, task_id: int) -> str:
    """
    Establishes a parent-child hierarchical relationship between Epic/Task.

    Uses helper function:
    - _link_task_to_epic_internal() - Handles the actual linking logic
                                      with validation

    Args:
        epic_id: The ID of the Epic work item (parent)
        task_id: The ID of the Task work item (child)

    Returns:
        Success message if link was created, error message otherwise
    """
    try:
        return work_item_service.link_task_to_epic(epic_id, task_id)
    except Exception as e:
        logger.error(f"Error linking task {task_id} to epic {epic_id}: {e}")
        return format_error_message("link_task_to_epic", e)


@mcp.tool()
def get_current_project() -> str:
    """
    Retrieves the currently configured Azure DevOps project name.

    Uses helper function:
    - get_current_config() - Gets configuration from environment variables

    Returns:
        The current project name from environment variables
    """
    try:
        config = get_current_config()
        return f"Current project: {config['project']}"
    except Exception as e:
        logger.error(f"Error getting current project: {e}")
        return format_error_message("get_current_project", e)


@mcp.tool()
def set_project(new_project_name: str) -> str:
    """
    Updates the Azure DevOps project configuration.

    Args:
        new_project_name: The name of the new project to switch to

    Returns:
        Confirmation message of the project change
    """
    try:
        return work_item_service.set_project(new_project_name)
    except Exception as e:
        logger.error(f"Error setting project: {e}")
        return format_error_message("set_project", e)


if __name__ == "__main__":
    # Run the MCP server with streamable-http transport
    logger.info("Starting Azure DevOps MCP Server...")
    logger.info("Server will be available at: http://localhost:8001/mcp/")
    mcp.run(transport="streamable-http", host="localhost", port=8001)
