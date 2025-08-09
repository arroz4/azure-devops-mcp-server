"""User guides and documentation for Azure DevOps MCP Server."""


def get_epic_management_guide():
    """
    Get the Epic management guide.

    Returns:
        str: Complete Epic management guide
    """
    return """
# Epic Management Comprehensive Guide

## Epic Organization Strategy

### Primary Workflow Approach
1. **Use create_epic_with_tasks**: Create Epic + multiple Tasks + linking in one command (fastest!)
2. **Alternative**: Create Epic first, then add Tasks individually with link_task_to_epic

### Epic Structure Best Practices
- **Epic Purpose**: High-level business objective or feature
- **Task Breakdown**: 3-8 Tasks per Epic (optimal project management)
- **Task Scope**: Each Task should be completable in 1-3 days
- **Linking**: Always link Tasks to Epics for proper hierarchy

## Epic Creation Methods

### Method 1: Complete Epic with Tasks (Recommended)
**Tool:** `create_epic_with_tasks`

**Usage:**
```
epic_title: "Feature Development Epic"
task_titles: "Backend API, Frontend UI, Testing, Documentation"
task_descriptions: "Backend desc ||| Frontend desc ||| Testing desc ||| Docs desc"
```

**Benefits:**
- Creates everything in one operation
- Automatic linking of all Tasks to Epic
- Immediate URL summary table
- Consistent tagging and assignment

### Method 2: Incremental Approach
**Tools:** `create_work_item` + `link_task_to_epic`

**Steps:**
1. Create Epic with `create_work_item`
2. Create each Task individually
3. Link each Task to Epic with `link_task_to_epic`

**Benefits:**
- More control over individual items
- Can add Tasks later as scope changes
- Flexible for evolving requirements

## Task Description Guidelines

### Quality Standards (Reference: Work Item ID 89)
Each Task description MUST include these 5 sections:

1. **## Objective** - What will be accomplished (4-5 sentences)
2. **## Technical Requirements** - Specific tools and constraints
3. **## Implementation Steps** - 8-10 numbered action items
4. **## Acceptance Criteria** - 6-8 testable checkboxes
5. **## Business Context** - Enterprise value explanation

### Description Delimiter System
- **Multiple Tasks**: Use `|||` to separate descriptions
- **Example**: `"Task 1 desc ||| Task 2 desc ||| Task 3 desc"`
- **Legacy Support**: Comma separation (only when count matches exactly)
- **Single Description**: Assigns to first Task only

## Epic Management Lifecycle

### 1. Planning Phase
- Define Epic objective and scope
- Break down into logical Tasks
- Assign priority levels
- Set up proper tags for filtering

### 2. Execution Phase
- Monitor Task progress through states
- Update Task assignments as needed
- Track Epic completion percentage
- Manage dependencies and blockers

### 3. Completion Phase
- Validate all acceptance criteria
- Update Epic status to completed
- Document lessons learned
- Archive or reference for future work

## URL Management and Access

### Immediate Access Features
- **Epic URLs**: Direct links provided in creation summary
- **Task URLs**: Individual links for each Task
- **Breakdown Tables**: Complete URL overview for Epics
- **Quick Navigation**: Click any URL for immediate Azure DevOps access

### URL Structure Understanding
- Format: `https://dev.azure.com/{org}/{project}/_workitems/edit/{id}`
- Direct editing access
- Shareable with team members
- Bookmark-friendly for frequent access

## Advanced Epic Strategies

### Epic Types by Size
- **Small Epic**: 3-4 Tasks, 1-2 week completion
- **Medium Epic**: 5-6 Tasks, 2-4 week completion
- **Large Epic**: 7-8 Tasks, 4-6 week completion

### Tagging Strategy
- **Project Tags**: Use consistent project identifiers
- **Technology Tags**: Specific tools and platforms
- **Priority Tags**: Business importance indicators
- **Phase Tags**: Development stage markers

### Assignment Patterns
- **Epic Owner**: Project lead or senior developer
- **Task Assignments**: Specific team members by expertise
- **Shared Tasks**: Use for collaborative work items
- **Unassigned**: For future allocation or backlog items

This guide ensures optimal Epic and Task management for successful project delivery.
"""


def get_user_guide():
    """
    Get the general user guide.

    Returns:
        str: Complete user guide
    """
    return """
# Azure DevOps MCP Server User Guide

## Available Tools Overview

### Core Work Item Management
1. **create_work_item** - Create individual Tasks or Epics
2. **create_epic_with_tasks** - Create Epic with multiple Tasks (recommended)
3. **update_work_item** - Modify existing work items
4. **delete_work_item** - Remove work items
5. **get_work_item** - Retrieve detailed work item information
6. **link_task_to_epic** - Establish parent-child relationships

### Project Management
7. **get_current_project** - View current project configuration
8. **set_project** - Switch between projects

## Quick Start Guide

### 1. Create Your First Epic with Tasks
```
Tool: create_epic_with_tasks
- epic_title: "Your Epic Name"
- task_titles: "Task 1, Task 2, Task 3"
- task_descriptions: "Desc 1 ||| Desc 2 ||| Desc 3"
- assigned_to: "your.email@company.com"
- priority: 1 (1=highest, 4=lowest)
- tags: "project;feature;sprint1"
```

### 2. View Your Epic
```
Tool: get_work_item
- item_id: [Epic ID from creation response]
```
This shows the Epic details plus a table of all linked Tasks with URLs.

### 3. Update Work Items
```
Tool: update_work_item
- item_id: [Work Item ID]
- description: "Updated description"
- assigned_to: "new.person@company.com"
```

## Best Practices

### Work Item Creation
- **Always use comprehensive descriptions** following the 5-section format
- **Include specific technical requirements** and acceptance criteria
- **Set appropriate priority levels** (1=critical, 2=high, 3=medium, 4=low)
- **Use consistent tagging** for project organization

### Epic Management
- **Create Epics with 3-8 Tasks** for optimal management
- **Use the ||| delimiter** for multiple task descriptions
- **Assign clear owners** to both Epics and Tasks
- **Track progress** through work item states

### URL Management
- **Bookmark Epic URLs** for quick project access
- **Share Task URLs** with specific team members
- **Use the URL breakdown tables** for team meetings
- **Access Azure DevOps directly** through provided links

## Description Quality Standards

### Required Sections (5 total)
1. **## Objective** - Clear accomplishment statement (4-5 sentences)
2. **## Technical Requirements** - Specific tools and constraints
3. **## Implementation Steps** - 8-10 numbered action items
4. **## Acceptance Criteria** - 6-8 testable checkboxes
5. **## Business Context** - Enterprise value explanation

### Example Quality Description
```
## Objective
Implement user authentication system for the web application...

## Technical Requirements
- Azure Active Directory integration
- JWT token management
- Role-based access control

## Implementation Steps
1. Configure Azure AD application registration
2. Implement authentication middleware
3. Create user role management system
...

## Acceptance Criteria
- [ ] Users can log in with corporate credentials
- [ ] Role-based permissions enforced
- [ ] Session management functional
...

## Business Context
This authentication system ensures secure access to company data...
```

## Troubleshooting

### Common Issues
- **Missing descriptions**: Use the ||| delimiter for multiple tasks
- **Linking failures**: Verify Epic and Task IDs are correct
- **Permission errors**: Check Azure DevOps project access
- **URL access issues**: Ensure you're logged into Azure DevOps

### Getting Help
- Reference Work Item ID 89 for quality standards
- Use get_work_item to verify created items
- Check work item URLs for direct Azure DevOps access
- Contact admin for project access issues

This guide provides everything needed for effective Azure DevOps work item management.
"""


def get_workflow_guide():
    """
    Get the workflow guide.

    Returns:
        str: Complete workflow guide
    """
    return """
# Epic Creation Workflow Guide

## Streamlined Epic Creation Process

### Step 1: Plan Your Epic
**Preparation Checklist:**
- [ ] Define Epic objective and business value
- [ ] Break down work into 3-8 logical Tasks
- [ ] Identify team members for assignment
- [ ] Determine priority level (1-4)
- [ ] Choose relevant tags for organization

### Step 2: Prepare Task Information
**Task Titles:** Create comma-separated list
```
Example: "Database Setup, API Development, Frontend Implementation, Testing"
```

**Task Descriptions:** Use ||| delimiter (new system)
```
Example: "Complete DB description ||| Complete API description ||| Complete UI description ||| Complete test description"
```

### Step 3: Execute Epic Creation
**Use create_epic_with_tasks tool:**
```
epic_title: "Your Epic Name"
epic_description: "Epic-level description with business context"
task_titles: "Task 1, Task 2, Task 3, Task 4"
task_descriptions: "Desc 1 ||| Desc 2 ||| Desc 3 ||| Desc 4"
assigned_to: "team.member@company.com"
priority: 2
tags: "project;feature;quarter1"
```

### Step 4: Review Creation Results
**What You Get:**
- Epic created with unique ID and URL
- All Tasks created and linked to Epic
- Summary table with all work item URLs
- Immediate access to Azure DevOps items

**Verification Steps:**
1. Click Epic URL to verify in Azure DevOps
2. Check each Task URL for proper descriptions
3. Verify linking in Epic's related work items
4. Confirm assignments and priorities

## Quality Assurance Process

### Description Quality Check
**Each Task Must Have 5 Sections:**
1. **## Objective** - Clear goal statement
2. **## Technical Requirements** - Specific tools needed
3. **## Implementation Steps** - 8-10 numbered actions
4. **## Acceptance Criteria** - 6-8 testable checkboxes
5. **## Business Context** - Enterprise value explanation

**Reference Standard:** Work Item ID 89 demonstrates perfect quality

### Post-Creation Tasks
**Immediate Actions:**
- Review all generated work items
- Update descriptions if needed using update_work_item
- Assign specific team members to individual Tasks
- Set up any additional dependencies or blockers

**Ongoing Management:**
- Track Task progress through states (To Do → Doing → Done)
- Update Epic progress as Tasks complete
- Add comments and attachments as work progresses
- Monitor for scope changes requiring new Tasks

## Advanced Workflow Techniques

### Epic Sizing Guidelines
**Small Epic (1-2 weeks):**
- 3-4 Tasks maximum
- Single feature or component
- 1-2 developers involved

**Medium Epic (2-4 weeks):**
- 5-6 Tasks optimal
- Multiple components or integrations
- Small team collaboration

**Large Epic (4-6 weeks):**
- 7-8 Tasks maximum
- Complex feature with multiple dependencies
- Full team involvement

### Parallel Task Management
**Dependency Planning:**
- Identify Tasks that can run in parallel
- Mark Tasks with prerequisites
- Set up proper sequencing for dependent work
- Use Task linking for complex dependencies

### Team Collaboration Patterns
**Assignment Strategies:**
- **Epic Owner**: Senior developer or team lead
- **Core Tasks**: Primary feature developers
- **Supporting Tasks**: QA, documentation, DevOps team
- **Review Tasks**: Stakeholders and product owners

This workflow ensures consistent, high-quality Epic and Task creation for successful project delivery.
"""
