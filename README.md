# Azure DevOps Work Item Manager - MCP Server

This is a Model Context Protocol (MCP) server that provides tools for managing Azure DevOps work items. It allows you to create, update, delete, and retrieve work items, as well as manage project settings and create hierarchical relationships between Epics and Tasks.

## ⭐ Key Features

- **Individual Work Items**: Create and manage Tasks and Epics one at a time
- **Streamlined Epic Creation**: Create an Epic with multiple Tasks in a single command with automatic linking
- **Comprehensive Summaries**: Get formatted tables with URLs for all created work items
- **Professional Templates**: Built-in description templates with structured format (Objective, Technical Requirements, Implementation Steps, Acceptance Criteria, Business Context)
- **Markdown Support**: Full Markdown formatting in descriptions (headers, lists, code blocks, links)
- **Detailed Guidance**: Comprehensive task descriptions that provide clear implementation guidance
- **Project Management**: Switch between projects and manage configurations
- **Interactive Guides**: Built-in prompts for common workflows

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
2. **Azure DevOps Personal Access Token (PAT)**
3. **FastMCP** (installed automatically)

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   uv add fastmcp
   # or
   pip install fastmcp
   ```

3. Create a `.env` file with your Azure DevOps configuration:
   ```env
   AZURE_DEVOPS_PAT=your_personal_access_token_here
   AZURE_DEVOPS_PROJECT=your_project_name
   AZURE_DEVOPS_ORGANIZATION_URL=https://dev.azure.com/your_organization
   ```

4. Run the MCP server:
   ```bash
   python mcp_server.py
   ```

5. In VS Code with the MCP extension installed, the server will be automatically available for use with your Azure DevOps project.

## 🛠️ Available Tools

### 1. `create_work_item`
Creates a new work item (Task or Epic) in Azure DevOps.

**Parameters:**
- `work_item_type` (string): "Task" or "Epic"
- `title` (string): The title of the work item
- `description` (string, optional): Description of the work item (supports Markdown formatting - MUST use \n for line breaks)
- `assigned_to` (string, optional): Email address of the person to assign
- `priority` (int, optional): Priority level (1-4, where 1 is highest)
- `tags` (string, optional): Semicolon-separated tags

**IMPORTANT:** Work item descriptions support full Markdown formatting as Azure DevOps renders them as .md files. **MUST use \n characters for line breaks** to ensure human readability. Use headers, lists, checkboxes, code blocks, links, and other Markdown features.

**Example:**
```python
create_work_item(
    work_item_type="Task",
    title="Implement user authentication",
    description="## Objective\nAdd login/logout functionality\n\n## Tasks\n- [ ] Create login form\n- [ ] Implement authentication logic\n- [ ] Add logout functionality\n\n## Acceptance Criteria\n- Users can log in with email/password\n- Session management works correctly",
    assigned_to="user@company.com",
    priority=1,
    tags="feature; security"
)
```

### 2. `update_work_item`
Updates an existing work item in Azure DevOps.

**Parameters:**
- `item_id` (int): The ID of the work item to update
- `title` (string, optional): New title for the work item
- `description` (string, optional): New description (supports Markdown formatting - MUST use \n for line breaks)
- `assigned_to` (string, optional): Email address to assign or "" to unassign
- `priority` (int, optional): New priority level (1-4)
- `tags` (string, optional): New tags or "" to remove all tags

### 3. `delete_work_item`
Deletes a work item from Azure DevOps.

**Parameters:**
- `item_id` (int): The ID of the work item to delete

### 4. `get_work_item`
Retrieves detailed information about a work item.

**Parameters:**
- `item_id` (int): The ID of the work item to retrieve

### 5. `link_task_to_epic`
Establishes a parent-child hierarchical relationship between an Epic and a Task.

**Parameters:**
- `epic_id` (int): The ID of the Epic work item (parent)
- `task_id` (int): The ID of the Task work item (child)

### 6. `get_current_project`
Retrieves the currently configured Azure DevOps project name.

### 7. `set_project`
Updates the Azure DevOps project configuration for the current session.

**Parameters:**
- `new_project_name` (string): The name of the new project to switch to

### 8. `create_epic_with_tasks`
Creates an Epic with multiple Tasks and automatically links them, providing a summary table with URLs.

**Parameters:**
- `epic_title` (string): The title of the Epic to create
- `epic_description` (string, optional): Epic description (supports Markdown formatting - MUST use \n for line breaks)
- `task_titles` (string): Comma-separated list of Task titles (e.g., "Setup API, Create UI, Write tests")
- `task_descriptions` (string, optional): Comma-separated list of Task descriptions (must match task_titles count - MUST use \n for line breaks)
- `assigned_to` (string, optional): Email address to assign all work items to
- `priority` (int, optional): Priority level (1-4, where 1 is highest)
- `tags` (string, optional): Semicolon-separated tags to apply to all work items

**Example:**
```python
create_epic_with_tasks(
    epic_title="Epic: User Authentication System",
    epic_description="## Overview\nImplement comprehensive user authentication\n\n## Features\n- [ ] Login/Logout\n- [ ] Password reset\n- [ ] Multi-factor authentication\n\n## Success Criteria\n- [ ] Secure authentication\n- [ ] User-friendly interface\n- [ ] Performance optimized",
    task_titles="Setup authentication framework, Create login API, Implement password reset, Add MFA support",
    task_descriptions="## Objective\nSet up core authentication infrastructure\n\n## Tasks\n- Install auth libraries\n- Configure security, ## Objective\nCreate login and logout endpoints\n\n## Tasks\n- Design API endpoints\n- Implement JWT tokens, ## Objective\nAdd password reset functionality\n\n## Tasks\n- Email verification\n- Reset token generation, ## Objective\nImplement multi-factor authentication\n\n## Tasks\n- SMS/Email 2FA\n- Backup codes",
    assigned_to="developer@company.com",
    priority=2,
    tags="authentication;security;user-management"
)
```

**Returns:**
A formatted summary table with:
- Epic and Task IDs and URLs
- Linking status for each Task
- Next steps guidance

## 🧭 Interactive Prompts

The MCP server includes helpful prompts to guide you through common workflows:

### `epic_management_guide`
Interactive guide for Epic and Task management workflows.

**Use Cases:**
- Creating a new Epic with multiple related Tasks
- Adding a single Task to an existing Epic
- Learning best practices for Epic organization

**Parameters:**
- `action_type`: Choose "create_epic_with_tasks" or "add_task_to_epic"
- `epic_title`: For new Epics (title of Epic to create)
- `epic_id`: For existing Epics (ID of Epic to add Task to)
- `task_titles`: Comma-separated list of Task titles
- `assignee_email`: Optional email for assignments

## 📚 Knowledge Resources

The server provides comprehensive documentation through built-in resources:

### `ado://guide/user-friendly`
**Complete User Guide** - Comprehensive guide covering all MCP server functionality, best practices, common workflows, and troubleshooting tips.

### `ado://guide/epic-workflow`
**Epic & Task Workflow Guide** - Detailed step-by-step guide for Epic creation, Task breakdown, linking strategies, and team collaboration patterns.

These resources provide:
- ✅ Step-by-step workflows
- ✅ Best practice templates
- ✅ Troubleshooting guides
- ✅ Team collaboration tips
- ✅ Project management strategies

## 🎯 Workflow Recommendations

### When to Use `create_epic_with_tasks` (Recommended)
- ✅ Starting a new feature with multiple related tasks
- ✅ You have a clear list of tasks planned out
- ✅ Tasks don't require highly customized individual descriptions
- ✅ You want automatic linking and URL summary
- ✅ **Fastest workflow for most scenarios**

### When to Use Individual Tools (`create_work_item`, `link_task_to_epic`)
- ✅ Tasks need highly detailed, customized descriptions
- ✅ Different team members need different task configurations
- ✅ Adding tasks to existing epics over time
- ✅ Complex dependency scenarios requiring manual setup

### Quick Comparison
| Feature | `create_epic_with_tasks` | Individual Tools |
|---------|-------------------------|------------------|
| Speed | ⚡ Very Fast | 🐌 Slower |
| URL Summary | ✅ Automatic | ❌ Manual |
| Auto-linking | ✅ Yes | ❌ Manual |
| Customization | 🔶 Good | ✅ Maximum |
| Error Recovery | ✅ Easy | 🔶 Complex |

## 🔧 VS Code Configuration

This project is designed specifically for VS Code with MCP integration. Here's how to set it up:

### Prerequisites

1. **Install VS Code MCP Extension**
   - Install the MCP extension for VS Code
   - Ensure you have Python 3.11+ installed

2. **Project Setup**
   - Clone/download this project
   - Install dependencies: `uv sync` or `pip install -r requirements.txt`
   - Configure your `.env` file with Azure DevOps credentials

### VS Code MCP Configuration

The MCP configuration is stored in `.vscode/mcp.json`:

```json
{
  "servers": {
    "ADO-server": {
      "url": "http://localhost:8000/mcp/",
      "type": "http"
    }
  },
  "inputs": []
}
```

### Running the Server

1. **Start the MCP Server:**
   ```bash
   python mcp_server.py
   ```
   
2. **Verify Connection:**
   - The server runs on `http://localhost:8000/mcp/`
   - VS Code MCP extension should automatically connect
   - You'll see Azure DevOps tools available in VS Code

### Environment Configuration

Ensure your `.env` file contains:

```env
AZURE_DEVOPS_PAT=your_personal_access_token
AZURE_DEVOPS_PROJECT=your_project_name
AZURE_DEVOPS_ORGANIZATION_URL=https://dev.azure.com/your_organization
MCP_SERVER_PORT=8000
```

### VS Code Integration Features

- 🛠️ **Tools Integration** - All Azure DevOps tools available in VS Code
- 🧭 **Interactive Prompts** - Guided workflows for Epic and Task management
- 📚 **Built-in Documentation** - Access user guides and best practices
- 🔄 **Live Connection** - Real-time connection to your Azure DevOps project
- 🎯 **Context Aware** - Tools adapt to your current project settings

## 📋 Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete work items
- ✅ **Work Item Types** - Support for Tasks and Epics
- ✅ **Hierarchical Relationships** - Link Tasks to Epics
- ✅ **Project Management** - Switch between different projects
- ✅ **Environment Variables** - Secure configuration management
- ✅ **Error Handling** - Comprehensive error messages
- ✅ **Validation** - Input validation and type checking
- ✅ **Optimized Code** - DRY principles with helper functions

## 🔐 Security

- Uses Personal Access Tokens for authentication
- Environment variables for sensitive data
- No hardcoded credentials in source code

## 🐳 Docker Support

All Docker-related files are located in the `docker/` folder. See `docker/README.md` for detailed instructions.

### Quick Start with Docker

1. **Build the image:**
   ```bash
   # Using Docker directly
   docker build -f docker/Dockerfile -t ado-mcp-server .
   
   # Or using the helper script (Windows)
   .\docker\docker-script.ps1 build
   
   # Or using the helper script (Linux/Mac)
   ./docker/docker-script.sh build
   ```

2. **Run the container:**
   ```bash
   # Using Docker Compose (recommended)
   docker-compose -f docker/docker-compose.yml up -d
   
   # Or using Docker directly
   docker run -d --name ado-mcp-server -p 8000:8000 --env-file .env ado-mcp-server
   
   # Or using the helper script
   .\docker\docker-script.ps1 run    # Windows
   ./docker/docker-script.sh run     # Linux/Mac
   ```

3. **Check server status:**
   ```bash
   # Server should be accessible at http://localhost:8000/mcp/
   # Check VS Code MCP extension for connection status
   ```

### Docker Scripts

Use the provided scripts for easier Docker management:

**Windows (PowerShell):**
```powershell
.\docker\docker-script.ps1 [build|run|stop|logs|shell|clean]
```

**Linux/Mac (Bash):**
```bash
./docker/docker-script.sh [build|run|stop|logs|shell|clean]
```

### Production Deployment

For production environments, use the production Docker Compose file:

```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

This includes:
- Resource limits (512MB memory, 0.5 CPU)
- Proper logging configuration
- Health checks
- Restart policies

### Environment Variables

When using Docker, ensure these environment variables are set:

```env
AZURE_DEVOPS_PAT=your_personal_access_token
AZURE_DEVOPS_PROJECT=your_project_name
AZURE_DEVOPS_ORGANIZATION_URL=https://dev.azure.com/your_organization
MCP_SERVER_PORT=8000
```

## 🧪 Testing

The MCP server can be tested through the HTTP endpoints:

```bash
# MCP endpoint
curl http://localhost:8000/mcp/
```

## 📚 Azure DevOps API

This MCP server uses the Azure DevOps REST API v7.0:
- Work Items API for CRUD operations
- Relations API for hierarchical linking
- JSON Patch format for updates

## 🔗 Dependencies

- `fastmcp` - MCP server framework
- `requests` - HTTP client for Azure DevOps API
- `python-dotenv` - Environment variable management
- `uvicorn` - ASGI server for HTTP transport
- `fastapi` - Web framework for health endpoints

## 📝 License

This project is provided as-is for educational and development purposes.
