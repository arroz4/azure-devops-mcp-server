"""Utility functions for the Azure DevOps MCP Server."""

import logging
from typing import Any, Dict, List


def setup_logging(level=logging.INFO):
    """
    Set up logging configuration.

    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def validate_required_fields(data: Dict[str, Any],
                           required_fields: List[str]) -> List[str]:
    """
    Validate that required fields are present in data.

    Args:
        data: Dictionary to validate
        required_fields: List of required field names

    Returns:
        List of missing field names
    """
    missing_fields = []
    for field in required_fields:
        if field not in data or data[field] is None or data[field] == "":
            missing_fields.append(field)
    return missing_fields


def sanitize_input(text: str) -> str:
    """
    Sanitize input text for Azure DevOps.

    Args:
        text: Text to sanitize

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove potentially harmful characters
    sanitized = text.replace("'", "'").replace('"', '"')

    # Limit length to prevent excessive data
    max_length = 10000  # Reasonable limit for descriptions
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "... (truncated)"

    return sanitized


def extract_id_from_url(url: str) -> int:
    """
    Extract work item ID from Azure DevOps URL.

    Args:
        url: Azure DevOps work item URL

    Returns:
        Work item ID

    Raises:
        ValueError: If ID cannot be extracted from URL
    """
    if not url:
        raise ValueError("URL cannot be empty")

    try:
        # Extract ID from URL pattern like:
        # https://dev.azure.com/org/project/_workitems/edit/123
        parts = url.split('/')
        id_str = parts[-1]
        return int(id_str)
    except (IndexError, ValueError) as e:
        raise ValueError(f"Cannot extract ID from URL: {url}") from e


def format_error_message(operation: str, error: Exception) -> str:
    """
    Format a consistent error message.

    Args:
        operation: Name of the operation that failed
        error: The exception that occurred

    Returns:
        Formatted error message
    """
    return f"Error during {operation}: {str(error)}"


def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Split a list into chunks of specified size.

    Args:
        items: List to chunk
        chunk_size: Size of each chunk

    Returns:
        List of chunks
    """
    chunks = []
    for i in range(0, len(items), chunk_size):
        chunks.append(items[i:i + chunk_size])
    return chunks


def safe_get(dictionary: Dict[str, Any], key: str,
             default: Any = None) -> Any:
    """
    Safely get a value from a dictionary.

    Args:
        dictionary: Dictionary to get value from
        key: Key to look up
        default: Default value if key not found

    Returns:
        Value from dictionary or default
    """
    return dictionary.get(key, default)


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge multiple dictionaries into one.

    Args:
        *dicts: Dictionaries to merge

    Returns:
        Merged dictionary
    """
    result = {}
    for d in dicts:
        if d:  # Only merge non-None dictionaries
            result.update(d)
    return result


def is_valid_email(email: str) -> bool:
    """
    Basic email validation.

    Args:
        email: Email address to validate

    Returns:
        True if email appears valid
    """
    if not email:
        return False

    # Basic validation - contains @ and .
    return "@" in email and "." in email and len(email) > 5


def format_table_row(columns: List[str], widths: List[int]) -> str:
    """
    Format a table row with proper column widths.

    Args:
        columns: Column values
        widths: Column widths

    Returns:
        Formatted table row
    """
    if len(columns) != len(widths):
        raise ValueError("Number of columns must match number of widths")

    formatted_cols = []
    for col, width in zip(columns, widths):
        if len(col) > width:
            col = col[:width-3] + "..."
        formatted_cols.append(col.ljust(width))

    return "| " + " | ".join(formatted_cols) + " |"


def create_table_separator(widths: List[int]) -> str:
    """
    Create a table separator line.

    Args:
        widths: Column widths

    Returns:
        Table separator line
    """
    separators = ["-" * width for width in widths]
    return "| " + " | ".join(separators) + " |"
