#!/usr/bin/env python3
"""
Azure DevOps Work Item Management MCP Server
Azure DevOps is also referred to as ADO.
The purpose of this ADO is to manage software development projects efficiently.
To do this there is a hierarchy where the work items are organized into Epics as parent items and Tasks as child items.

This MCP server provides tools for managing Azure DevOps work items including:
- Creating Tasks and Epics
- Updating work items
- Deleting work items
- Retrieving work item details with comprehensive URL breakdowns
- Linking Tasks to Epics
- Project management

KEY FEATURE: URL Breakdown Functionality
- create_epic_with_tasks: Provides immediate summary table with all work item URLs after creation
- get_work_item: Shows detailed breakdown with URLs for Epics and all their child Tasks
- Both functions provide direct Azure DevOps URLs for instant access to work items

IMPORTANT: Work item descriptions support HTML formatting as confirmed by Microsoft Azure DevOps documentation.
The Description field has Data type=HTML and proper HTML formatting renders perfectly in Azure DevOps.
Based on successful testing (work item ID 75), use HTML paragraph structure for optimal rendering:
- Use <p> tags for paragraphs: <p>Content here</p>
- Use <strong> for bold text: <p><strong>Section:</strong></p>
- Use <ul><li> for unordered lists and <ol><li> for ordered lists
- Use <br> tags for line breaks within paragraphs
- Always use \\n characters for line separations (converts to proper HTML structure)

CRITICAL: The process_description_text() function automatically converts \\n to proper HTML paragraph formatting for perfect Azure DevOps rendering!

Company context:
The company is called Omar's Solutions. We specialize in providing
data solutions involving ETL, data base management, semantic model design and building.
We support our operations in the Azure cloud and we use Azure Synapse to handle ETL processes.
We use ADLS Gen2 for data storage and management.

App Context Responsibilities:
This MCP server has token generation limitations, so it doesnt need to provide templates or very complicated explanations unless specifically asked to do so.
However, when creating work items, it MUST provide COMPREHENSIVE and DETAILED task descriptions that include proper structure with Objective, Technical Requirements, Implementation Steps, and Acceptance Criteria sections.
The App provides comprehensive task descriptions with clear guidance while avoiding overly complex explanations in general responses.
App should avoid to alter any work items when not in a 'To do' state. 

Final User Responsibilities:
The final user of this tasks will update the tasks and change the sate to 'Doing' while actively working on task.
The final user will write comments on the tasks. 
The final user will generate all content files attached or related after.
The final user will change the state to 'Done' when the task is completed.

"""

import os
import json
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
import base64
from enum import Enum

# Load environment variables
load_dotenv()

# Initialize FastMCP
mcp = FastMCP("Azure DevOps Work Item Manager")

# MCP Prompts
@mcp.prompt()
def epic_management_guide():
    """Guide for creating Epics with child Tasks and adding Tasks to existing Epics"""
    return {
        "name": "epic_management_guide",
        "description": "Learn how to create Epics with child Tasks and add Tasks to existing Epics",
        "arguments": [
            {
                "name": "action_type",
                "description": "Choose: 'create_epic_with_tasks' to create a new Epic with multiple Tasks, or 'add_task_to_epic' to add a single Task to an existing Epic",
                "required": True
            },
            {
                "name": "epic_title",
                "description": "For new Epics: Title of the Epic to create. For existing Epics: leave empty and provide epic_id instead",
                "required": False
            },
            {
                "name": "epic_id", 
                "description": "For adding to existing Epic: ID of the Epic to add Task to. For new Epics: leave empty",
                "required": False
            },
            {
                "name": "task_titles",
                "description": "Comma-separated list of Task titles to create under the Epic",
                "required": True
            },
            {
                "name": "assignee_email",
                "description": "Email address to assign the Epic and/or Tasks to (optional)",
                "required": False
            }
        ]
    }

# MCP Resources
@mcp.resource("ado://guide/user-friendly")
def user_guide():
    """Comprehensive user guide for the Azure DevOps MCP Server"""
    current_project, current_org_url, _ = get_current_config()
    return {
        "uri": "ado://guide/user-friendly",
        "name": "Azure DevOps MCP Server - User Guide",
        "description": "Complete guide for using the Azure DevOps MCP Server effectively",
        "mimeType": "text/markdown",
        "text": f"""# 🚀 Azure DevOps MCP Server - User Guide

Welcome to your Azure DevOps MCP Server! This guide will help you manage work items like a pro.

**Current Project:** {current_project}
**Organization:** {current_org_url}

## 🎯 Quick Start

### What Can You Do?
- ✅ Create Tasks and Epics (individual or batch)
- ✅ Create Epic with multiple Tasks in one command (with auto-linking and URL summary)
- ✅ Update existing work items
- ✅ Delete work items
- ✅ Link Tasks to Epics (parent-child relationships)
- ✅ Switch between projects
- ✅ Get detailed work item information

**⚠️ IMPORTANT**: Always create COMPREHENSIVE and DETAILED task descriptions with proper structure including Objective, Technical Requirements, Implementation Steps, and Acceptance Criteria sections.

## 📋 Work Item Types

### 🏆 **Epics**
Think of Epics as big features or initiatives. They're like containers for related work.

**Best Practices:**
- Use clear, descriptive titles: "Epic: User Authentication System"
- Include business value in the description (use Markdown formatting)
- Break down into smaller Tasks
- Set appropriate priority (1=highest, 4=lowest)

### ✅ **Tasks** 
Tasks are specific, actionable work items that make up an Epic.

**Best Practices:**
- Keep titles action-oriented: "Task: Create login API endpoint"
- Make them small enough to complete in 1-3 days
- Include clear acceptance criteria (use Markdown lists and checkboxes)
- Link to parent Epic when applicable

**📋 Task Description Requirements:**
Task descriptions should be **COMPREHENSIVE and DETAILED**, not short or brief. Include:
- **Objective section**: Clear statement of what needs to be accomplished
- **Technical Requirements**: Specific technical details, constraints, and dependencies
- **Implementation Steps**: Detailed breakdown of work to be done
- **Acceptance Criteria**: Specific, testable conditions using Markdown checkboxes
- **Business Context**: Why this task matters and how it fits the larger goal
- Use proper Markdown formatting with headers (##), lists, and checkboxes
- Minimum 3-4 sentences per section for adequate detail and context

## 🔧 Common Workflows

### ⚡ RECOMMENDED: Creating an Epic with Multiple Tasks (Streamlined)

**Use this for:** New features with multiple tasks (fastest method)

```
Tool: create_epic_with_tasks
- epic_title: "Epic: User Profile Management"
- epic_description: "## Overview\nAllow users to manage their profile information\n\n## Features\n- [ ] Avatar upload\n- [ ] Personal details editing\n- [ ] Privacy preferences\n- [ ] Account settings"
- task_titles: "Design profile UI, Implement avatar upload, Create user preferences, Add validation logic"
- task_descriptions: "## Objective\nDesign comprehensive UI mockups and implement responsive profile interface\n\n## Tasks\n1. Create wireframes for profile layout\n2. Design UI components with accessibility standards\n3. Implement responsive CSS framework\n\n## Acceptance Criteria\n- [ ] Mobile-responsive design\n- [ ] WCAG 2.1 accessibility compliance\n- [ ] Cross-browser compatibility, ## Objective\nBuild secure file upload system for user avatars\n\n## Technical Requirements\n- Support JPG, PNG, WebP formats\n- Maximum file size 5MB\n- Image compression and resizing\n- Virus scanning integration\n\n## Acceptance Criteria\n- [ ] Upload progress indicator\n- [ ] Image preview before saving\n- [ ] Error handling for invalid files, ## Objective\nImplement comprehensive user preferences and settings management\n\n## Features\n- Notification preferences\n- Privacy settings\n- Theme customization\n- Language selection\n\n## Acceptance Criteria\n- [ ] Real-time settings sync\n- [ ] Export/import preferences\n- [ ] Settings validation, ## Objective\nImplement comprehensive form validation across all profile forms\n\n## Validation Rules\n- Email format and uniqueness\n- Password complexity requirements\n- Required field validation\n- Custom business rules\n\n## Acceptance Criteria\n- [ ] Client-side validation with immediate feedback\n- [ ] Server-side validation for security\n- [ ] Localized error messages"
- assigned_to: "teamlead@company.com"
- priority: 2
- tags: "feature; user-management"
```

**Result:** Automatic Epic + Tasks creation, linking, and URL summary table!

### 1️⃣ Creating an Epic with Multiple Tasks (Manual Method)

**Use this for:** Complex scenarios requiring individual task customization

**Step 1:** Create the Epic
```
Tool: create_work_item
- work_item_type: "Epic"
- title: "Epic: User Profile Management"
- description: "## Overview\nAllow users to manage their profile information including avatar, personal details, and preferences\n\n## Features\n- [ ] Avatar upload and management\n- [ ] Personal details editing\n- [ ] Privacy preferences\n- [ ] Account settings\n\n## Success Criteria\n- Users can update all profile fields\n- Changes are saved automatically\n- Profile validation works correctly"
- assigned_to: "teamlead@company.com"
- priority: 2
- tags: "feature; user-management"
```

**Step 2:** Create Tasks under the Epic
```
Tool: create_work_item (repeat for each task)
- work_item_type: "Task"
- title: "Task: Design profile edit UI"
- description: "## Objective\nCreate mockups and implement profile editing interface\n\n## Tasks\n1. Create wireframes for profile page\n2. Design UI components\n3. Implement responsive layout\n4. Add form validation\n\n## Acceptance Criteria\n- [ ] Mobile-responsive design\n- [ ] Accessible UI components\n- [ ] Form validation with error messages"
- assigned_to: "designer@company.com"
- priority: 2
- tags: "frontend; ui"
```

**Step 3:** Link Tasks to Epic
```
Tool: link_task_to_epic
- epic_id: [Epic ID from step 1]
- task_id: [Task ID from step 2]
```

### 2️⃣ Adding a Task to an Existing Epic

**Step 1:** Find your Epic ID
```
Tool: get_work_item
- item_id: [Your Epic ID]
```

**Step 2:** Create the new Task
```
Tool: create_work_item
- work_item_type: "Task"
- title: "Task: Add password reset functionality"
- description: "## Objective\nImplement forgot password feature with email verification\n\n## Implementation Steps\n1. Create password reset API endpoint\n2. Design email template\n3. Implement token generation and validation\n4. Add reset form UI\n5. Test email delivery\n\n## Technical Requirements\n- Secure token generation (JWT)\n- Email service integration\n- Token expiration (24 hours)\n- Rate limiting for reset requests\n\n## Acceptance Criteria\n- [ ] User receives reset email within 2 minutes\n- [ ] Reset link expires after 24 hours\n- [ ] Password complexity validation\n- [ ] Audit logging for security"
- assigned_to: "developer@company.com"
- priority: 1
- tags: "backend; security"
```

**Step 3:** Link the Task to the Epic
```
Tool: link_task_to_epic
- epic_id: [Existing Epic ID]
- task_id: [New Task ID from step 2]
```

## 🏷️ Tagging Best Practices

Use semicolon-separated tags to categorize work:

**By Type:**
- `feature` - New functionality
- `bug` - Bug fixes
- `enhancement` - Improvements to existing features
- `documentation` - Documentation updates

**By Component:**
- `frontend` - UI/UX work
- `backend` - Server-side work
- `database` - Data layer changes
- `api` - API development

**By Status:**
- `blocked` - Cannot proceed
- `ready` - Ready to start
- `in-review` - Under review
- `testing` - Being tested

## 🎚️ Priority Guidelines

**Priority 1 (Critical):**
- Production bugs affecting users
- Security vulnerabilities
- Blocking issues for other work

**Priority 2 (High):**
- Important new features
- Non-blocking bugs
- Performance improvements

**Priority 3 (Medium):**
- Standard feature development
- Minor enhancements
- Technical debt

**Priority 4 (Low):**
- Nice-to-have features
- Future considerations
- Research tasks

## 🔄 Project Management

### Switching Projects
```
Tool: set_project
- new_project_name: "MyOtherProject"
```

### Checking Current Project
```
Tool: get_current_project
```

## 💡 Pro Tips

### 📝 **Markdown Formatting in Descriptions:**
Azure DevOps renders work item descriptions as Markdown files. Use proper formatting with explicit \\n for human readability:

**CRITICAL: Always use \\n for line breaks!**

**Headers (with \\n):**
```
# Main Objective\\n## Technical Requirements\\n### Implementation Details
```

**Lists and Checkboxes (with \\n):**
```
- Bullet point\\n- Another point\\n\\n1. Numbered list\\n2. Second item\\n\\n- [ ] Unchecked task\\n- [x] Completed task
```

**Code and Links (with \\n):**
```
`inline code`\\n\\n```python\\ncode block\\n```\\n\\n[Documentation Link](https://docs.microsoft.com)
```

**Emphasis (with \\n):**
```
**Bold text** for important items\\n*Italic text* for emphasis\\n\\nNew paragraph here
```

**Example well-formatted description:**
```
## Overview\\nThis task involves...\\n\\n## Tasks\\n- [ ] Step 1\\n- [ ] Step 2\\n\\n## Notes\\nImportant information here
```

### 🎯 **For Better Organization:**
1. **Use consistent naming**: Start Epics with "Epic:" and Tasks with "Task:"
2. **Keep descriptions clear**: Include acceptance criteria and context (use Markdown formatting)
3. **Tag everything**: Makes searching and filtering much easier
4. **Set realistic priorities**: Don't make everything Priority 1!

### ⚡ **For Faster Workflows:**
1. **Use create_epic_with_tasks**: Create Epic + multiple Tasks + linking in one command (fastest!)
2. **Batch create Tasks**: For manual approach, create all Tasks for an Epic, then link them
3. **Use templates**: Copy descriptions from similar work items
4. **Update regularly**: Keep work item status current
5. **Link related work**: Use the linking feature to show dependencies

### 🛠️ **For Team Collaboration:**
1. **Assign clearly**: Make sure everyone knows their responsibilities
2. **Use @mentions**: Tag team members in descriptions for notifications
3. **Update status**: Keep teammates informed of progress
4. **Document decisions**: Use work item comments for important discussions

## 🚨 Troubleshooting

### Common Issues:

**"Failed to create work item"**
- Check your Azure DevOps PAT token is valid
- Verify you have permissions to create work items
- Ensure the project name is correct

**"Failed to link work items"**
- Verify both Epic and Task IDs exist
- Check that the Epic is actually an Epic type
- Ensure the Task is actually a Task type

**"Work item not found"**
- Double-check the work item ID
- Verify you're in the correct project
- Make sure the work item wasn't deleted

## 📞 Need Help?

1. **Check work item details**: Use `get_work_item` to see current status
2. **Verify project**: Use `get_current_project` to confirm you're in the right place
3. **Review this guide**: Most common workflows are covered here
4. **Check Azure DevOps directly**: Sometimes the web interface provides additional context

---

Happy work item management! 🎉

*Remember: Good work item management leads to better project visibility and team collaboration.*
"""
    }

@mcp.resource("ado://guide/epic-workflow")
def epic_workflow_guide():
    """Detailed guide specifically for Epic and Task workflow"""
    return {
        "uri": "ado://guide/epic-workflow", 
        "name": "Epic & Task Workflow Guide",
        "description": "Step-by-step guide for Epic creation and Task management",
        "mimeType": "text/markdown",
        "text": """# 🏆 Epic & Task Workflow Guide

## 🎯 Epic Creation Strategy

### Planning Your Epic

**Before you create an Epic, ask yourself:**
1. What business value does this provide?
2. How will we know when it's complete?
3. What are the major components/tasks needed?
4. Who should be involved?
5. What's the priority relative to other work?

### Epic Structure Template

**Important:** Use Markdown formatting in descriptions as Azure DevOps renders them as .md files

```
Title: Epic: [Feature Area] - [Brief Description]

Description: 
## Business Value
[Why this matters to users/business]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2  
- [ ] Criterion 3

## Scope
### Included
- [What's included]
- [Feature 1]
- [Feature 2]

### Excluded
- [What's excluded]
- [Out of scope items]

## Dependencies
- [Other work this depends on]
- [Blocking items]

## Technical Notes
```python
# Code examples if relevant
```

**Links:** [Related Documentation](url)
  
Tags: feature; [component]; [team]
Priority: [1-4 based on business impact]
```

## 🔄 Three Main Workflows

### Workflow 1A: Create Epic + Tasks (Streamlined - RECOMMENDED)

**When to use:** Starting a new feature from scratch with multiple tasks

**Tool:** `create_epic_with_tasks`

**Benefits:** 
- Single command creates Epic + all Tasks + links them automatically
- Returns summary table with all URLs
- Faster and less error-prone

**Steps:**
1. **Plan your Epic and Tasks**
   - Epic title and description (use Markdown)
   - List of task titles (comma-separated)
   - **IMPORTANT**: Task descriptions should be COMPREHENSIVE and DETAILED, not short or brief. Each description must include: Objective section, Technical Requirements, Implementation Steps, and Acceptance Criteria with proper Markdown formatting

2. **Execute the command**
   - All work items created and linked automatically
   - Receive formatted summary with URLs
   - Review and refine as needed

### Workflow 1B: Create Epic + Tasks (Manual Method)

**When to use:** Complex scenarios requiring individual task customization

1. **Create the Epic first**
   - Use descriptive title with "Epic:" prefix
   - Include comprehensive description with Markdown formatting (headers, lists, checkboxes)
   - Set appropriate priority and tags
   - Assign to Epic owner/lead

2. **Plan the breakdown**
   - List all major tasks needed
   - Ensure tasks are small enough (1-3 days each)
   - Consider dependencies between tasks

3. **Create Tasks one by one**
   - Use "Task:" prefix in titles
   - Make titles action-oriented
   - Include clear acceptance criteria using Markdown checkboxes
   - Assign to appropriate team members

4. **Link Tasks to Epic**
   - Use `link_task_to_epic` for each Task
   - This creates the parent-child relationship
   - Helps with reporting and tracking

### Workflow 2: Add Task to Existing Epic

**When to use:** Adding scope to existing work or splitting large tasks

1. **Review the existing Epic**
   - Use `get_work_item` to see current Epic details
   - Understand the current scope and progress
   - Check existing linked Tasks

2. **Identify the gap**
   - What new work is needed?
   - How does it fit with existing Tasks?
   - Are there dependencies to consider?

3. **Create the new Task**
   - Follow same Task creation best practices
   - Consider how it relates to existing work
   - Assign appropriately

4. **Link to the Epic**
   - Use `link_task_to_epic` to establish relationship
   - Update Epic description if scope changed significantly

## 📊 Epic Management Best Practices

### 🎯 **Epic Sizing**
- **Good Epic:** 2-4 weeks of work for a team
- **Too Small:** Could be just a Task
- **Too Large:** Should be broken into multiple Epics

### 🏷️ **Epic Tagging Strategy**
```
Epic tags should include:
- Type: feature, enhancement, technical-debt
- Component: frontend, backend, infrastructure
- Team: team-alpha, team-beta
- Initiative: q1-goals, user-experience
```

### 📝 **Task Breakdown Guidelines**

**Good Task Examples:**
- "Task: Create user registration API endpoint"
- "Task: Design profile page wireframes"
- "Task: Implement password validation"
- "Task: Write unit tests for auth service"

**Avoid These:**
- "Task: Do everything" (too vague)
- "Task: Build entire login system" (too large)
- "Login stuff" (not descriptive)

### 🔗 **Linking Strategy**

**Always link when:**
- Tasks contribute to an Epic's completion
- Work items have dependencies
- Tasks share common acceptance criteria

**Linking Benefits:**
- Progress tracking at Epic level
- Better reporting and visibility
- Clearer team communication
- Easier sprint planning

## 🚀 Advanced Tips

### 📈 **Epic Progress Tracking**
- Link all related Tasks to see completion percentage
- Use consistent tagging for easy filtering
- Update Epic description as scope evolves
- Close Epic only when ALL linked Tasks are complete

### 🎛️ **Priority Management**
- Epic priority should reflect business value
- Task priorities can vary within an Epic
- Critical bugs might have higher priority than Epic
- Adjust priorities as business needs change

### 👥 **Team Collaboration**
- Assign Epic to the lead/owner
- Distribute Tasks among team members
- Use @mentions in comments for communication
- Regular updates help team stay aligned

### 📅 **Sprint Planning Integration**
- Epics span multiple sprints usually
- Tasks should fit within single sprint
- Plan Task dependencies across sprints
- Use Epic progress to guide sprint goals

---

**Remember:** Good Epic and Task management is the foundation of successful project delivery! 🎯
"""
    }

@mcp.resource("ado://template/description")
def description_template():
    """Template for creating comprehensive work item descriptions"""
    return {
        "uri": "ado://template/description",
        "name": "Work Item Description Template",
        "description": "Comprehensive template for creating detailed Epic and Task descriptions",
        "mimeType": "text/markdown",
        "text": """# 📝 Work Item Description Template

## 🏆 Epic Description Template

Use this template for creating comprehensive Epic descriptions:

```
[Brief summary of the Epic in one sentence explaining the main goal.]

**Objective:** [Clear statement of what needs to be accomplished and why it matters to the business]

**Key Requirements:**
- [Specific requirement 1 with clear details]
- [Specific requirement 2 with technical constraints]
- [Specific requirement 3 with business rules]
- [Additional requirements as needed]

**Success Criteria:**
- [Measurable outcome 1 that defines completion]
- [Measurable outcome 2 that ensures quality]
- [Measurable outcome 3 that validates business value]
- [Additional criteria for comprehensive validation]
```

### 📋 Epic Example

```
Develop a comprehensive semantic model following TOML architecture for automation data processing.

**Objective:** Create a robust semantic model that imports and processes data from the existing SQL serverless database, following TOML (Tables, Objects, Measures, Labels) architecture principles.

**Key Requirements:**
- Import all data from SQL serverless database
- Follow TOML architecture standards
- Ensure scalable and maintainable design
- Prepare foundation for future automation enhancements

**Success Criteria:**
- Semantic model successfully created and validated
- All data imported without loss or corruption
- TOML architecture properly implemented
- Documentation completed for future reference
```

## ✅ Task Description Template

Use this template for creating detailed Task descriptions:

```
## Objective
[Clear statement of what this specific task accomplishes and how it contributes to the parent Epic]

## Technical Requirements
- [Specific technical constraint or requirement]
- [Technology stack or tools to be used]
- [Performance or quality standards to meet]
- [Integration points with other systems]

## Implementation Steps
1. [Detailed step 1 with specific actions]
2. [Detailed step 2 with technical details]
3. [Detailed step 3 with validation approach]
4. [Additional steps as needed for completion]

## Acceptance Criteria
- [ ] [Specific, testable condition 1]
- [ ] [Specific, testable condition 2]
- [ ] [Specific, testable condition 3]
- [ ] [Additional criteria for thorough validation]

## Business Context
[Explanation of why this task matters and how it fits into the larger business goal]
```

### 📋 Task Example

```
## Objective
Analyze the existing SQL serverless database schema to understand data structure, relationships, and prepare for semantic model implementation following TOML architecture principles.

## Technical Requirements
- Access to SQL serverless database with read permissions
- Database documentation and schema analysis tools
- Understanding of TOML architecture components
- Data profiling and quality assessment capabilities

## Implementation Steps
1. Connect to SQL serverless database and document connection parameters
2. Generate complete schema documentation including tables, views, and relationships
3. Analyze data types, constraints, and business rules for each entity
4. Map existing structure to TOML architecture components (Tables, Objects, Measures, Labels)
5. Identify data quality issues and document remediation requirements
6. Create preliminary data flow diagrams for semantic model design

## Acceptance Criteria
- [ ] Complete database schema documentation generated and reviewed
- [ ] All table relationships and dependencies mapped and validated
- [ ] Data quality assessment completed with issues documented
- [ ] TOML mapping strategy defined and approved by technical lead
- [ ] Preliminary design documents created for next implementation phase

## Business Context
This foundational analysis ensures the semantic model will accurately represent business data and support future automation initiatives while maintaining data integrity and following enterprise architecture standards.
```

## 🎯 Usage Guidelines

### When Creating Descriptions:
1. **Start with the template** - Copy the appropriate template structure
2. **Fill in all sections** - Don't skip any section, ensure comprehensive coverage
3. **Be specific** - Use concrete details rather than vague statements
4. **Make it testable** - Acceptance criteria should be measurable and verifiable
5. **Consider the audience** - Write for both technical and business stakeholders

### Format Requirements:
- Use Markdown formatting with proper headers (##)
- Include bullet points (-) and checkboxes (- [ ]) for lists
- Use \\n for line breaks in the description field
- Ensure minimum 3-4 sentences per section for adequate detail

### Quality Checklist:
- [ ] Objective clearly states the goal and business value
- [ ] Technical requirements are specific and actionable
- [ ] Implementation steps provide a clear roadmap
- [ ] Acceptance criteria are measurable and testable
- [ ] Business context explains the "why" behind the work
"""
    }

# Define allowed work item types
class WorkItemType(Enum):
    TASK = "Task"
    EPIC = "Epic"

# Helper Functions
def get_current_config():
    """
    Retrieves current Azure DevOps configuration from environment variables.
    
    Returns:
        tuple: (project, organization_url, personal_access_token)
    """
    current_project = os.getenv("AZURE_DEVOPS_PROJECT")
    current_org_url = os.getenv("AZURE_DEVOPS_ORGANIZATION_URL")
    current_pat = os.getenv("AZURE_DEVOPS_PAT")
    return current_project, current_org_url, current_pat

def process_description_text(description: str) -> str:
    """
    Process description text to ensure proper formatting for Azure DevOps.
    Converts \\n escape sequences to proper HTML paragraph formatting.
    
    Based on Azure DevOps documentation and testing:
    - Description field has Data type=HTML (confirmed from Microsoft docs)
    - Work item ID 75 confirmed that HTML paragraph formatting works perfectly
    - Use <p> tags for paragraphs and proper HTML structure for optimal rendering
    
    Args:
        description: Raw description text with \\n characters
        
    Returns:
        Processed description with HTML paragraph formatting for proper Azure DevOps rendering
    """
    if not description:
        return description
    
    # Convert \\n escape sequences to actual newlines first
    processed = description.replace('\\n', '\n')
    
    # Split into sections by double newlines first
    sections = processed.split('\n\n')
    html_sections = []
    
    for section in sections:
        if not section.strip():
            continue
            
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        if not lines:
            continue
            
        section_html = []
        in_list = False
        list_type = None
        
        for line in lines:
            if line.startswith('**') and line.endswith('**'):
                # Close any open list first
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                # Convert markdown bold headers to HTML paragraph with strong
                content = line[2:-2]  # Remove ** from both ends
                section_html.append(f'<p><strong>{content}</strong></p>')
            elif line.startswith('- ') or line.startswith('• '):
                # Handle unordered list items
                if not in_list or list_type != 'ul':
                    if in_list:
                        section_html.append(f'</{list_type}>')
                    section_html.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                item_content = line[2:].strip()  # Remove "- " or "• "
                section_html.append(f'<li>{item_content}</li>')
            elif len(line) > 2 and line[:2].replace('.', '').isdigit() and line[2:3] == '.':
                # Handle numbered list items (1. 2. etc.)
                if not in_list or list_type != 'ol':
                    if in_list:
                        section_html.append(f'</{list_type}>')
                    section_html.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                item_content = line[3:].strip() if len(line) > 3 else ""  # Remove "1. " etc.
                section_html.append(f'<li>{item_content}</li>')
            elif line.startswith('✓ '):
                # Handle checkmark items - keep them as paragraph with breaks
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                content = line[2:].strip()  # Remove "✓ "
                section_html.append(f'✓ {content}<br>')
            elif line.startswith('##'):
                # Keep markdown headers as-is for mixed compatibility
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                section_html.append(line)
            else:
                # Regular paragraph content
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                section_html.append(f'<p>{line}</p>')
        
        # Close any remaining open list
        if in_list:
            section_html.append(f'</{list_type}>')
        
        # Handle checkmark section completion
        if section_html and any('✓' in line and '<br>' in line for line in section_html):
            # Find checkmark lines and wrap them properly
            checkmark_lines = []
            other_lines = []
            for line in section_html:
                if '✓' in line and '<br>' in line:
                    checkmark_lines.append(line)
                else:
                    other_lines.append(line)
            
            if checkmark_lines:
                # Combine checkmark lines into a single paragraph
                checkmark_content = '\n'.join(checkmark_lines).rstrip('<br>')
                other_lines.append(f'<p>{checkmark_content}</p>')
                section_html = other_lines
        
        html_sections.append('\n'.join(section_html))
    
    return '\n\n'.join(html_sections)

def get_auth_headers(pat=None):
    """
    Creates authorization headers for Azure DevOps API requests.
    
    Args:
        pat (str, optional): Personal Access Token. If None, gets from environment.
    
    Returns:
        dict: Headers dictionary with authorization
    """
    if pat is None:
        _, _, pat = get_current_config()
    
    return {
        "Authorization": f"Basic {base64.b64encode(f':{pat}'.encode()).decode()}"
    }

def get_json_patch_headers(pat=None):
    """
    Creates headers for JSON Patch requests to Azure DevOps API.
    
    Args:
        pat (str, optional): Personal Access Token. If None, gets from environment.
    
    Returns:
        dict: Headers dictionary with content-type and authorization
    """
    headers = get_auth_headers(pat)
    headers["Content-Type"] = "application/json-patch+json"
    return headers

def build_workitem_url(item_id=None, work_item_type=None):
    """
    Builds Azure DevOps work item API URL.
    
    Args:
        item_id (int, optional): Work item ID for specific item operations
        work_item_type (str, optional): Work item type for creation operations
    
    Returns:
        str: Complete API URL
    """
    current_project, current_org_url, _ = get_current_config()
    
    if work_item_type:
        return f"{current_org_url}/{current_project}/_apis/wit/workitems/${work_item_type}?api-version=7.0"
    elif item_id:
        return f"{current_org_url}/{current_project}/_apis/wit/workitems/{item_id}?api-version=7.0"
    else:
        return f"{current_org_url}/{current_project}/_apis/wit/workitems?api-version=7.0"

# Helper Functions for Internal Use
def _create_work_item_internal(
    work_item_type: str, 
    title: str, 
    description: str = "", 
    assigned_to: str = "", 
    priority: Optional[int] = None, 
    tags: str = ""
) -> str:
    """
    Internal helper function to create work items.
    Avoids "FunctionTool object not callable" errors when MCP tools call other MCP tools.
    
    Used by:
    - create_work_item() - Main MCP tool for individual work item creation
    - create_epic_with_tasks() - Streamlined Epic+Tasks creation workflow
    
    Args:
        work_item_type: The type of work item to create ("Task" or "Epic")
        title: The title of the work item
        description: Description with Markdown formatting (\\n converts to paragraph breaks)
        assigned_to: Email address of the person to assign
        priority: Priority level (1-4, where 1 is highest)
        tags: Semicolon-separated tags
    
    Returns:
        Success message with ID and URL if successful, error message otherwise
    """
    try:
        # Validate work item type
        if work_item_type not in ["Task", "Epic"]:
            return f"Error: Invalid work item type '{work_item_type}'. Must be 'Task' or 'Epic'"
        
        # URL to create a work item
        url = build_workitem_url(work_item_type=work_item_type)

        # Define the payload for the work item - always include title
        payload = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
        ]
        
        # Only add optional fields if they're provided
        if description:
            processed_description = process_description_text(description)
            payload.append({"op": "add", "path": "/fields/System.Description", "value": processed_description})
        
        if assigned_to:
            payload.append({"op": "add", "path": "/fields/System.AssignedTo", "value": assigned_to})
        
        if priority is not None:
            payload.append({"op": "add", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority})
        
        if tags:
            payload.append({"op": "add", "path": "/fields/System.Tags", "value": tags})

        # Get headers
        headers = get_json_patch_headers()

        # Make the POST request
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code in [200, 201]:
            item_data = response.json()
            item_url = item_data.get('_links', {}).get('html', {}).get('href', '')
            item_id = item_data.get('id', 'Unknown')
            return f"{work_item_type} created successfully! ID: {item_id}, URL: {item_url}"
        else:
            return f"Failed to create {work_item_type.lower()}: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {e}"

def _link_task_to_epic_internal(epic_id: int, task_id: int) -> str:
    """
    Internal helper function to link tasks to epics.
    Avoids "FunctionTool object not callable" errors when MCP tools call other MCP tools.
    
    Used by:
    - link_task_to_epic() - Main MCP tool for linking individual tasks to epics
    - create_epic_with_tasks() - Streamlined Epic+Tasks creation workflow (links all tasks automatically)
    
    Args:
        epic_id: The ID of the Epic work item (parent)
        task_id: The ID of the Task work item (child)
    
    Returns:
        Success message if link was created, error message otherwise
    """
    try:
        # Get current configuration
        current_project, current_org_url, current_pat = get_current_config()
        
        # First, verify that the epic_id is actually an Epic and task_id is actually a Task
        def get_item_type(item_id: int):
            url = build_workitem_url(item_id=item_id)
            headers = get_auth_headers()
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None

        epic_data = get_item_type(epic_id)
        task_data = get_item_type(task_id)
        
        if not epic_data or not task_data:
            return "Failed to retrieve work item information for validation"
        
        epic_type = epic_data.get('fields', {}).get('System.WorkItemType', '')
        task_type = task_data.get('fields', {}).get('System.WorkItemType', '')
        
        if epic_type != 'Epic':
            return f"Error: Work item {epic_id} is not an Epic (it's a {epic_type})"
        
        if task_type != 'Task':
            return f"Error: Work item {task_id} is not a Task (it's a {task_type})"
        
        # URL to update the task work item to add the parent relationship
        url = f"{current_org_url}/{current_project}/_apis/wit/workitems/{task_id}?api-version=7.0"
        
        # Define the payload to add the parent-child relationship
        payload = [
            {
                "op": "add",
                "path": "/relations/-",
                "value": {
                    "rel": "System.LinkTypes.Hierarchy-Reverse",  # This means "parent"
                    "url": f"{current_org_url}/{current_project}/_apis/wit/workitems/{epic_id}"
                }
            }
        ]
        
        # Get headers
        headers = get_json_patch_headers()
        
        # Make the PATCH request
        response = requests.patch(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            epic_title = epic_data.get('fields', {}).get('System.Title', 'Unknown Epic')
            task_title = task_data.get('fields', {}).get('System.Title', 'Unknown Task')
            return f"Successfully linked Task '{task_title}' (ID: {task_id}) to Epic '{epic_title}' (ID: {epic_id})"
        else:
            return f"Failed to link work items: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"An error occurred while linking work items: {e}"

# MCP Tools
@mcp.tool()
def create_work_item(
    work_item_type: str, 
    title: str, 
    description: str = "", 
    assigned_to: str = "", 
    priority: Optional[int] = None, 
    tags: str = ""
) -> str:
    """
    Creates a new work item in Azure DevOps.
    
    Uses helper function:
    - _create_work_item_internal() - Handles the actual work item creation logic
    
    Args:
        work_item_type: The type of work item to create ("Task" or "Epic")
        title: The title of the work item
        description: Description of the work item (supports Markdown formatting - MUST use \\n for line breaks which converts to paragraph breaks)
        assigned_to: Email address of the person to assign
        priority: Priority level (1-4, where 1 is highest)
        tags: Semicolon-separated tags
    
    Returns:
        URL of the created work item if successful, error message otherwise
    """
    return _create_work_item_internal(work_item_type, title, description, assigned_to, priority, tags)

@mcp.tool()
def update_work_item(
    item_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None, 
    assigned_to: Optional[str] = None, 
    priority: Optional[int] = None, 
    tags: Optional[str] = None
) -> str:
    """
    Updates an existing work item in Azure DevOps.
    
    Uses helper functions:
    - process_description_text() - Converts \\n escape sequences to proper HTML paragraph formatting for perfect Azure DevOps rendering
    - build_workitem_url() - Constructs the Azure DevOps API URL for the work item
    - get_json_patch_headers() - Creates proper headers for JSON Patch requests
    
    Args:
        item_id: The ID of the work item to update
        title: New title for the work item
        description: New description (supports HTML formatting - MUST use \\n for line breaks which converts to HTML paragraphs)
        assigned_to: Email address to assign or "" to unassign
        priority: New priority level (1-4)
        tags: New tags or "" to remove all tags
    
    Returns:
        Success message with URL if successful, error message otherwise
    """
    try:
        # Check if at least one field is provided for update
        if all(param is None for param in [title, description, assigned_to, priority, tags]):
            return "Error: At least one field must be provided for update (title, description, assigned_to, priority, or tags)"
        
        # URL to update a work item
        url = build_workitem_url(item_id=item_id)

        # Define the payload for the work item update
        payload = []
        
        # Only add fields that are provided (not None)
        if title is not None:
            payload.append({"op": "replace", "path": "/fields/System.Title", "value": title})
        
        if description is not None:
            processed_description = process_description_text(description)
            payload.append({"op": "replace", "path": "/fields/System.Description", "value": processed_description})
        
        if assigned_to is not None:
            if assigned_to == "":  # Empty string means unassign
                payload.append({"op": "remove", "path": "/fields/System.AssignedTo"})
            else:
                payload.append({"op": "replace", "path": "/fields/System.AssignedTo", "value": assigned_to})
        
        if priority is not None:
            payload.append({"op": "replace", "path": "/fields/Microsoft.VSTS.Common.Priority", "value": priority})
        
        if tags is not None:
            if tags == "":  # Empty string means remove all tags
                payload.append({"op": "remove", "path": "/fields/System.Tags"})
            else:
                payload.append({"op": "replace", "path": "/fields/System.Tags", "value": tags})

        # Get headers
        headers = get_json_patch_headers()

        # Make the PATCH request
        response = requests.patch(url, json=payload, headers=headers)

        if response.status_code == 200:
            item_data = response.json()
            item_url = item_data.get('_links', {}).get('html', {}).get('href', '')
            item_id = item_data.get('id', 'Unknown')
            return f"Work item updated successfully! ID: {item_id}, URL: {item_url}"
        else:
            return f"Failed to update work item: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {e}"

@mcp.tool()
def delete_work_item(item_id: int) -> str:
    """
    Deletes a work item from Azure DevOps.
    
    Uses helper functions:
    - build_workitem_url() - Constructs the Azure DevOps API URL for the work item
    - get_auth_headers() - Creates proper authorization headers for the request
    
    Args:
        item_id: The ID of the work item to delete
    
    Returns:
        Success message if deletion was successful, error message otherwise
    """
    try:
        # URL to delete a work item
        url = build_workitem_url(item_id=item_id)

        # Get headers
        headers = get_auth_headers()

        # Make the DELETE request
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            item_data = response.json()
            item_id = item_data.get('id', 'Unknown')
            item_type = item_data.get('fields', {}).get('System.WorkItemType', 'Work item')
            return f"{item_type} deleted successfully! Deleted {item_type} ID: {item_id}"
        else:
            return f"Failed to delete work item: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {e}"

@mcp.tool()
def get_work_item(item_id: int) -> str:
    """
    Retrieves detailed information about a work item from Azure DevOps.
    For Epics, automatically shows a comprehensive table of all linked child work items with their URLs.
    
    This function is particularly useful when you need to see the complete breakdown of an Epic
    with all its associated Tasks, including direct URLs for quick access to each work item.
    
    Uses helper functions:
    - build_workitem_url() - Constructs the Azure DevOps API URL for the work item with relations expansion
    - get_auth_headers() - Creates proper authorization headers for the request
    
    Args:
        item_id: The ID of the work item to retrieve
    
    Returns:
        Formatted work item details if successful, error message otherwise.
        For Epics: Includes a complete breakdown table showing all child Tasks with IDs, titles, 
        states, assignees, and direct Azure DevOps URLs for immediate access.
    """
    try:
        # URL to get a work item with relations
        base_url = build_workitem_url(item_id=item_id)
        url = f"{base_url}&$expand=relations"

        # Get headers
        headers = get_auth_headers()

        # Make the GET request
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            item_data = response.json()
            
            # Extract key information
            item_id = item_data.get('id', 'Unknown')
            fields = item_data.get('fields', {})
            item_type = fields.get('System.WorkItemType', 'Unknown')
            title = fields.get('System.Title', 'No title')
            description = fields.get('System.Description', 'No description')
            state = fields.get('System.State', 'Unknown')
            assigned_to = fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned')
            priority = fields.get('Microsoft.VSTS.Common.Priority', 'No priority')
            tags = fields.get('System.Tags', 'No tags')
            created_date = fields.get('System.CreatedDate', 'Unknown')
            item_url = item_data.get('_links', {}).get('html', {}).get('href', '')
            
            # Format the basic information
            details = f"""
=== {item_type} Details ===
ID: {item_id}
Title: {title}
State: {state}
Assigned To: {assigned_to}
Priority: {priority}
Tags: {tags}
Created: {created_date}
Description: {description}
URL: {item_url}
==============================="""
            
            # Check for child work items (for Epics)
            relations = item_data.get('relations', [])
            child_items = []
            
            # Look for child relationships
            for relation in relations:
                rel_type = relation.get('rel', '')
                if rel_type in ['System.LinkTypes.Hierarchy-Forward', 'Microsoft.VSTS.Common.Hierarchy-Forward']:
                    # This is a child relationship
                    child_url = relation.get('url', '')
                    # Extract child ID from URL (handle both /workitems/ and /workItems/)
                    if '/workitems/' in child_url or '/workItems/' in child_url:
                        child_id = child_url.split('/')[-1]
                        try:
                            # Get child work item details
                            child_response = requests.get(build_workitem_url(item_id=int(child_id)), headers=headers)
                            
                            if child_response.status_code == 200:
                                child_data = child_response.json()
                                child_fields = child_data.get('fields', {})
                                child_items.append({
                                    'id': child_data.get('id'),
                                    'type': child_fields.get('System.WorkItemType', 'Unknown'),
                                    'title': child_fields.get('System.Title', 'No title'),
                                    'state': child_fields.get('System.State', 'Unknown'),
                                    'assigned_to': child_fields.get('System.AssignedTo', {}).get('displayName', 'Unassigned'),
                                    'url': child_data.get('_links', {}).get('html', {}).get('href', '')
                                })
                        except Exception:
                            # If we can't get child details, add basic info
                            child_items.append({
                                'id': child_id,
                                'type': 'Unknown',
                                'title': 'Error retrieving details',
                                'state': 'Unknown',
                                'assigned_to': 'Unknown',
                                'url': 'N/A'
                            })
            
            # Add child items table if any exist
            if child_items:
                details += f"\n\n🔗 **Child Work Items ({len(child_items)} total):**\n"
                details += f"| ID | Type | Title | State | Assigned To | URL |\n"
                details += f"|----|------|-------|-------|-------------|-----|\n"
                
                for child in child_items:
                    # Truncate title if too long for better table formatting
                    title_display = child['title'][:40] + "..." if len(child['title']) > 43 else child['title']
                    details += f"| {child['id']} | {child['type']} | {title_display} | {child['state']} | {child['assigned_to']} | {child['url']} |\n"
                
                details += f"\n💡 **Tip:** Use get_work_item with individual child IDs for detailed information."
            
            return details
        else:
            return f"Failed to retrieve work item: {response.status_code} - {response.text}"

    except Exception as e:
        return f"An error occurred: {e}"

@mcp.tool()
def link_task_to_epic(epic_id: int, task_id: int) -> str:
    """
    Establishes a parent-child hierarchical relationship between an Epic and a Task.
    
    Uses helper function:
    - _link_task_to_epic_internal() - Handles the actual linking logic with validation
    
    Args:
        epic_id: The ID of the Epic work item (parent)
        task_id: The ID of the Task work item (child)
    
    Returns:
        Success message if link was created, error message otherwise
    """
    return _link_task_to_epic_internal(epic_id, task_id)

@mcp.tool()
def get_current_project() -> str:
    """
    Retrieves the currently configured Azure DevOps project name.
    
    Uses helper function:
    - get_current_config() - Gets configuration from environment variables
    
    Returns:
        The current project name from environment variables
    """
    current_project, _, _ = get_current_config()
    return f"Current project: {current_project}"

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
        # Update the environment variable for current session
        old_project = os.getenv("AZURE_DEVOPS_PROJECT", "")
        os.environ["AZURE_DEVOPS_PROJECT"] = new_project_name
        
        return f"Project updated from '{old_project}' to '{new_project_name}' for current session"
    except Exception as e:
        return f"Error updating project: {e}"

@mcp.tool()
def create_epic_with_tasks(
    epic_title: str,
    epic_description: str = "",
    task_titles: str = "",
    task_descriptions: str = "",
    assigned_to: str = "",
    priority: Optional[int] = None,
    tags: str = ""
) -> str:
    """
    Creates an Epic with multiple Tasks and links them together, then provides a comprehensive summary with URLs.
    
    This is the RECOMMENDED workflow for creating Epics with multiple tasks in a single operation.
    The function automatically creates all work items, establishes parent-child relationships, and provides
    a detailed breakdown table with URLs for immediate access to all created items.
    
    Uses helper functions:
    - _create_work_item_internal() - Creates both the Epic and all Tasks
    - _link_task_to_epic_internal() - Links each Task to the Epic automatically
    
    Args:
        epic_title: The title of the Epic to create
        epic_description: Description of the Epic (supports HTML formatting - MUST use \\n for line breaks which converts to HTML paragraphs)
        task_titles: Comma-separated list of Task titles (e.g., "Task 1, Task 2, Task 3")
        task_descriptions: Comma-separated list of DETAILED Task descriptions. Each description should be comprehensive and include: Objective section, Technical Requirements, Implementation Steps, and Acceptance Criteria. Use proper formatting with headers (##), lists, and checkboxes. Minimum 3-4 sentences per section for adequate detail. (optional, must match task_titles count if provided - MUST use \\n for line breaks which converts to HTML paragraphs)
        assigned_to: Email address to assign the Epic and Tasks to (optional)
        priority: Priority level (1-4, where 1 is highest)
        tags: Semicolon-separated tags to apply to all work items
    
    Returns:
        Comprehensive summary table with Epic and Task URLs, linking status, and next steps.
        This breakdown provides immediate access to all created work items with their direct Azure DevOps URLs.
    """
    try:
        # Create the Epic first
        epic_result = _create_work_item_internal(
            work_item_type="Epic",
            title=epic_title,
            description=epic_description,
            assigned_to=assigned_to,
            priority=priority,
            tags=tags
        )
        
        # Extract Epic ID and URL from result
        if "created successfully!" not in epic_result:
            return f"Failed to create Epic: {epic_result}"
        
        # Parse Epic ID from result string
        epic_id_start = epic_result.find("ID: ") + 4
        epic_id_end = epic_result.find(",", epic_id_start)
        epic_id = int(epic_result[epic_id_start:epic_id_end])
        
        # Parse Epic URL from result string
        epic_url_start = epic_result.find("URL: ") + 5
        epic_url = epic_result[epic_url_start:].strip()
        
        # Process task titles
        if not task_titles.strip():
            return f"Epic created successfully!\n\n📋 **Epic Summary**\n| Work Item | ID | URL |\n|-----------|----|----- |\n| {epic_title} | {epic_id} | {epic_url} |\n\nNo tasks were created. Use task_titles parameter to create tasks."
        
        task_list = [title.strip() for title in task_titles.split(",") if title.strip()]
        
        # Process task descriptions (optional)
        desc_list = []
        if task_descriptions.strip():
            desc_list = [desc.strip() for desc in task_descriptions.split(",")]
            # Ensure descriptions list matches tasks list length
            while len(desc_list) < len(task_list):
                desc_list.append("")
        else:
            desc_list = [""] * len(task_list)
        
        # Create tasks and collect results
        created_tasks = []
        for i, task_title in enumerate(task_list):
            task_description = desc_list[i] if i < len(desc_list) else ""
            
            task_result = _create_work_item_internal(
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
                link_result = _link_task_to_epic_internal(epic_id, task_id)
                
                created_tasks.append({
                    "title": task_title,
                    "id": task_id,
                    "url": task_url,
                    "linked": "✅" if "Successfully linked" in link_result else "❌"
                })
            else:
                created_tasks.append({
                    "title": task_title,
                    "id": "Failed",
                    "url": "N/A",
                    "linked": "❌"
                })
        
        # Build summary table
        summary = f"Epic with Tasks created successfully!\n\n"
        summary += f"📋 **Work Items Summary**\n"
        summary += f"| Work Item | Type | ID | Linked | URL |\n"
        summary += f"|-----------|------|----|---------|----- |\n"
        summary += f"| {epic_title} | Epic | {epic_id} | - | {epic_url} |\n"
        
        for task in created_tasks:
            summary += f"| {task['title']} | Task | {task['id']} | {task['linked']} | {task['url']} |\n"
        
        summary += f"\n🎯 **Next Steps:**\n"
        summary += f"- Review and update work item descriptions with detailed acceptance criteria\n"
        summary += f"- Assign specific team members to individual tasks if needed\n"
        summary += f"- Set up any additional dependencies or blockers\n"
        summary += f"- Update Epic progress as tasks are completed\n"
        
        return summary
        
    except Exception as e:
        return f"An error occurred while creating Epic with Tasks: {e}"

if __name__ == "__main__":
    # Check if required environment variables are loaded
    current_project, current_org_url, current_pat = get_current_config()
    
    if not current_pat:
        print("❌ AZURE_DEVOPS_PAT not found in environment variables. Please check your .env file.")
        exit(1)
    if not current_org_url:
        print("❌ AZURE_DEVOPS_ORGANIZATION_URL not found in environment variables. Please check your .env file.")
        exit(1)
    if not current_project:
        print("❌ AZURE_DEVOPS_PROJECT not found in environment variables. Please check your .env file.")
        exit(1)
    
    # Get port from environment variable or use default
    port = int(os.getenv("MCP_SERVER_PORT", "8000"))
    
    print("✅ Azure DevOps MCP Server starting with HTTP transport...")
    print(f"📋 Project: {current_project}")
    print(f"🔗 Organization: {current_org_url}")
    print(f"🌐 Server will run on: http://localhost:{port}")
    print("🛠️  Available tools: create_work_item, update_work_item, delete_work_item, get_work_item, link_task_to_epic, get_current_project, set_project, create_epic_with_tasks")
    
    # Start the MCP server with HTTP transport
    mcp.run(transport="streamable-http", host="localhost", port=port)
