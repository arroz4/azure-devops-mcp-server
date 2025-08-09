"""Text formatting utilities for Azure DevOps work items."""


def process_description_text(description: str) -> str:
    """
    Process description text to ensure proper formatting for Azure DevOps.
    Converts \\n escape sequences to proper HTML paragraph formatting.

    Based on Azure DevOps documentation and testing:
    - Description field has Data type=HTML (confirmed from Microsoft docs)
    - Work item ID 75 confirmed that HTML paragraph formatting works perfectly
    - Use <p> tags for paragraphs and proper HTML structure for optimal
      rendering

    Args:
        description: Raw description text with \\n characters

    Returns:
        Processed description with HTML paragraph formatting for proper
        Azure DevOps rendering
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
                # Bold headers
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                header_text = line[2:-2]
                section_html.append(f'<p><strong>{header_text}</strong></p>')
            elif line.startswith('## '):
                # Section headers
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                header_text = line[3:]
                section_html.append(f'<p><strong>{header_text}</strong></p>')
            elif line.startswith('- '):
                # Unordered list items
                if not in_list or list_type != 'ul':
                    if in_list:
                        section_html.append(f'</{list_type}>')
                    section_html.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                item_text = line[2:]
                section_html.append(f'<li>{item_text}</li>')
            elif line.startswith('* '):
                # Alternative unordered list items
                if not in_list or list_type != 'ul':
                    if in_list:
                        section_html.append(f'</{list_type}>')
                    section_html.append('<ul>')
                    in_list = True
                    list_type = 'ul'
                item_text = line[2:]
                section_html.append(f'<li>{item_text}</li>')
            elif line.lstrip().startswith(('1.', '2.', '3.', '4.', '5.',
                                          '6.', '7.', '8.', '9.')):
                # Numbered list items
                if not in_list or list_type != 'ol':
                    if in_list:
                        section_html.append(f'</{list_type}>')
                    section_html.append('<ol>')
                    in_list = True
                    list_type = 'ol'
                # Extract text after number and period
                item_text = line.lstrip()
                dot_index = item_text.find('.')
                if dot_index != -1:
                    item_text = item_text[dot_index + 1:].strip()
                section_html.append(f'<li>{item_text}</li>')
            else:
                # Regular paragraph
                if in_list:
                    section_html.append(f'</{list_type}>')
                    in_list = False
                section_html.append(f'<p>{line}</p>')

        # Close any open list
        if in_list:
            section_html.append(f'</{list_type}>')

        html_sections.extend(section_html)

    return '\n'.join(html_sections)


def split_task_descriptions(task_descriptions: str, task_count: int) -> list:
    """
    Split task descriptions using the enhanced delimiter system.

    Args:
        task_descriptions: Raw descriptions string
        task_count: Number of tasks expected

    Returns:
        List of individual task descriptions
    """
    desc_list = []

    if task_descriptions.strip():
        # Check if using new ||| delimiter or old comma delimiter
        if "|||" in task_descriptions:
            # Split by ||| delimiter
            parts = task_descriptions.split("|||")
            desc_list = [part.strip() for part in parts]
        else:
            # Legacy comma support - but only if number of commas+1
            # equals number of tasks
            comma_split = [
                desc.strip() for desc in task_descriptions.split(",")
            ]
            if len(comma_split) == task_count:
                desc_list = comma_split
            else:
                # Single description provided - use it for first task,
                # empty for others
                desc_list = [task_descriptions.strip()] + \
                          [""] * (task_count - 1)

        # Ensure descriptions list matches tasks list length
        while len(desc_list) < task_count:
            desc_list.append("")
    else:
        desc_list = [""] * task_count

    return desc_list
