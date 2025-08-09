"""Work item management services."""

from typing import Optional, Dict, Any
from core.azure_client import AzureDevOpsClient
from core.config import build_workitem_url, WorkItemType
from services.formatting import process_description_text, split_task_descriptions


class WorkItemService:
    """Service for managing Azure DevOps work items."""

    def __init__(self):
        """Initialize the work item service."""
        self.client = AzureDevOpsClient()

    def create_work_item(
        self,
        work_item_type: str,
        title: str,
        description: str = "",
        assigned_to: str = "",
        priority: Optional[int] = None,
        tags: str = ""
    ) -> str:
        """
        Create a work item in Azure DevOps.

        Args:
            work_item_type: The type of work item to create
            title: The title of the work item
            description: Description of the work item
            assigned_to: Email address of the person to assign
            priority: Priority level (1-4, where 1 is highest)
            tags: Semicolon-separated tags

        Returns:
            Success message with work item details
        """
        try:
            # Process description text for proper HTML formatting
            processed_description = process_description_text(description)

            # Prepare fields
            fields = {
                "System.Title": title,
                "System.Description": processed_description
            }

            if assigned_to:
                fields["System.AssignedTo"] = assigned_to

            if priority is not None:
                fields["Microsoft.VSTS.Common.Priority"] = priority

            if tags:
                fields["System.Tags"] = tags

            # Create work item
            result = self.client.create_work_item(work_item_type, fields)

            work_item_id = result["id"]
            work_item_url = build_workitem_url(work_item_id)

            return (f"{work_item_type} created successfully! "
                   f"ID: {work_item_id}, URL: {work_item_url}")

        except Exception as e:
            return f"Error creating {work_item_type.lower()}: {e}"

    def get_work_item(self, item_id: int) -> str:
        """
        Retrieve and format work item details.

        Args:
            item_id: The ID of the work item to retrieve

        Returns:
            Formatted work item details with URLs
        """
        try:
            # Get work item with relations for Epic breakdown
            work_item = self.client.get_work_item(item_id, expand="relations")

            fields = work_item["fields"]
            work_item_type = fields.get("System.WorkItemType", "Unknown")
            title = fields.get("System.Title", "No Title")
            state = fields.get("System.State", "Unknown")
            assigned_to = fields.get("System.AssignedTo", {}).get("displayName", "Unassigned")
            priority = fields.get("Microsoft.VSTS.Common.Priority", "Not Set")
            tags = fields.get("System.Tags", "No Tags")
            created_date = fields.get("System.CreatedDate", "Unknown")
            description = fields.get("System.Description", "No Description")

            work_item_url = build_workitem_url(item_id)

            # Format basic details
            details = f"""
=== {work_item_type} Details ===
ID: {item_id}
Title: {title}
State: {state}
Assigned To: {assigned_to}
Priority: {priority}
Tags: {tags}
Created: {created_date}
Description: {description}
URL: {work_item_url}
==============================="""

            # For Epics, show child work items breakdown
            if (work_item_type == "Epic" and
                "relations" in work_item and work_item["relations"]):

                child_items = []
                for relation in work_item["relations"]:
                    if relation["rel"] == "System.LinkTypes.Hierarchy-Forward":
                        child_url = relation["url"]
                        child_id = int(child_url.split("/")[-1])
                        try:
                            child_item = self.client.get_work_item(child_id)
                            child_fields = child_item["fields"]
                            child_items.append({
                                "id": child_id,
                                "type": child_fields.get("System.WorkItemType", "Unknown"),
                                "title": child_fields.get("System.Title", "No Title"),
                                "state": child_fields.get("System.State", "Unknown"),
                                "assigned_to": child_fields.get("System.AssignedTo", {}).get("displayName", "Unassigned"),
                                "url": build_workitem_url(child_id)
                            })
                        except Exception:
                            # Skip if child item cannot be retrieved
                            continue

                if child_items:
                    details += f"\n\n🔗 **Child Work Items ({len(child_items)} total):**\n"
                    details += "| ID | Type | Title | State | Assigned To | URL |\n"
                    details += "|----|------|-------|-------|-------------|-----|\n"

                    for child in child_items:
                        details += (f"| {child['id']} | {child['type']} | "
                                  f"{child['title']} | {child['state']} | "
                                  f"{child['assigned_to']} | {child['url']} |\n")

                    details += "\n💡 **Tip:** Use get_work_item with individual child IDs for detailed information."

            return details

        except Exception as e:
            return f"Failed to retrieve work item: {e}"

    def update_work_item(
        self,
        item_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        assigned_to: Optional[str] = None,
        priority: Optional[int] = None,
        tags: Optional[str] = None
    ) -> str:
        """
        Update an existing work item.

        Args:
            item_id: The ID of the work item to update
            title: New title for the work item
            description: New description
            assigned_to: Email address to assign or "" to unassign
            priority: New priority level (1-4)
            tags: New tags or "" to remove all tags

        Returns:
            Success message with URL
        """
        try:
            fields = {}

            if title is not None:
                fields["System.Title"] = title

            if description is not None:
                processed_description = process_description_text(description)
                fields["System.Description"] = processed_description

            if assigned_to is not None:
                fields["System.AssignedTo"] = assigned_to

            if priority is not None:
                fields["Microsoft.VSTS.Common.Priority"] = priority

            if tags is not None:
                fields["System.Tags"] = tags

            # Update work item
            self.client.update_work_item(item_id, fields)
            work_item_url = build_workitem_url(item_id)

            return f"Work item updated successfully! URL: {work_item_url}"

        except Exception as e:
            return f"Error updating work item: {e}"

    def delete_work_item(self, item_id: int) -> str:
        """
        Delete a work item.

        Args:
            item_id: The ID of the work item to delete

        Returns:
            Success or error message
        """
        try:
            success = self.client.delete_work_item(item_id)
            if success:
                return f"Work item deleted successfully! Deleted Work item ID: {item_id}"
            else:
                return f"Failed to delete work item {item_id}"
        except Exception as e:
            return f"Error deleting work item: {e}"

    def link_task_to_epic(self, epic_id: int, task_id: int) -> str:
        """
        Link a task to an epic.

        Args:
            epic_id: The ID of the Epic work item (parent)
            task_id: The ID of the Task work item (child)

        Returns:
            Success or error message
        """
        try:
            success = self.client.create_work_item_link(epic_id, task_id)
            if success:
                return f"Successfully linked Task {task_id} to Epic {epic_id}"
            else:
                return f"Failed to link Task {task_id} to Epic {epic_id}"
        except Exception as e:
            return f"Error linking work items: {e}"

    def create_epic_with_tasks(
        self,
        epic_title: str,
        epic_description: str = "",
        task_titles: str = "",
        task_descriptions: str = "",
        assigned_to: str = "",
        priority: Optional[int] = None,
        tags: str = ""
    ) -> str:
        """
        Create an Epic with multiple Tasks and link them together.

        Args:
            epic_title: The title of the Epic to create
            epic_description: Description of the Epic
            task_titles: Comma-separated list of Task titles
            task_descriptions: Descriptions for each task, separated by |||
            assigned_to: Email address to assign work items to
            priority: Priority level (1-4, where 1 is highest)
            tags: Semicolon-separated tags

        Returns:
            Comprehensive summary with URLs
        """
        try:
            # Create the Epic first
            epic_result = self.create_work_item(
                work_item_type="Epic",
                title=epic_title,
                description=epic_description,
                assigned_to=assigned_to,
                priority=priority,
                tags=tags
            )

            if "created successfully!" not in epic_result:
                return f"Error creating Epic: {epic_result}"

            # Parse Epic ID and URL
            epic_id_start = epic_result.find("ID: ") + 4
            epic_id_end = epic_result.find(",", epic_id_start)
            epic_id = int(epic_result[epic_id_start:epic_id_end])

            epic_url_start = epic_result.find("URL: ") + 5
            epic_url = epic_result[epic_url_start:].strip()

            # Process tasks if provided
            if not task_titles.strip():
                return (f"Epic created successfully!\n\n"
                       f"📋 **Epic Summary**\n"
                       f"| Work Item | ID | URL |\n"
                       f"|-----------|----|----- |\n"
                       f"| {epic_title} | {epic_id} | {epic_url} |\n\n"
                       f"No tasks were created. Use task_titles parameter to add tasks.")

            task_list = [
                title.strip() for title in task_titles.split(",")
                if title.strip()
            ]

            # Split task descriptions using enhanced logic
            desc_list = split_task_descriptions(task_descriptions, len(task_list))

            # Create tasks and collect results
            created_tasks = []
            for i, task_title in enumerate(task_list):
                task_description = desc_list[i] if i < len(desc_list) else ""

                task_result = self.create_work_item(
                    work_item_type="Task",
                    title=task_title,
                    description=task_description,
                    assigned_to=assigned_to,
                    priority=priority,
                    tags=tags
                )

                if "created successfully!" in task_result:
                    # Parse Task ID and URL
                    task_id_start = task_result.find("ID: ") + 4
                    task_id_end = task_result.find(",", task_id_start)
                    task_id = int(task_result[task_id_start:task_id_end])

                    task_url_start = task_result.find("URL: ") + 5
                    task_url = task_result[task_url_start:].strip()

                    # Link task to epic
                    link_result = self.link_task_to_epic(epic_id, task_id)

                    created_tasks.append({
                        "title": task_title,
                        "id": task_id,
                        "url": task_url,
                        "linked": "✅" if "Successfully linked" in link_result else "❌"
                    })
                else:
                    return f"Error creating task '{task_title}': {task_result}"

            # Generate summary
            summary = "Epic with Tasks created successfully!\n\n"
            summary += "📋 **Work Items Summary**\n"
            summary += "| Work Item | Type | ID | Linked | URL |\n"
            summary += "|-----------|------|----|---------|----- |\n"
            summary += f"| {epic_title} | Epic | {epic_id} | - | {epic_url} |\n"

            for task in created_tasks:
                summary += (f"| {task['title']} | Task | {task['id']} | "
                          f"{task['linked']} | {task['url']} |\n")

            summary += "\n🎯 **Next Steps:**\n"
            summary += "- Review and update work item descriptions with detailed acceptance criteria\n"
            summary += "- Assign specific team members to individual tasks if needed\n"
            summary += "- Set up any additional dependencies or blockers\n"
            summary += "- Update Epic progress as tasks are completed\n"

            return summary

        except Exception as e:
            return f"Error creating Epic with Tasks: {e}"
