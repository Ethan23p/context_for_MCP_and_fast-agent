"""
Configuration for the context generation script.
Contains all packaging jobs and default settings.
"""

from typing import List, Dict, Any

# Default ignore patterns applied to all jobs
DEFAULT_IGNORE_PATTERNS = {
    ".git", ".venv", "__pycache__", ".vscode", "*.pyc", "*.bak", 
    "*.optimized.*", "dist", "node_modules", ".DS_Store"
}

# All packaging jobs configuration
PACKAGING_JOBS: List[Dict[str, Any]] = [
    {
        "repo_name": "fast-agent",
        "sub_path": "examples", 
        "output_filename": "fast_agent_examples_context.md",
        "ignore": ["*.png", "*.jpg", "*.jpeg", "*.ico"]
    },
    {
        "repo_name": "fast-agent",
        "sub_path": "tests", 
        "output_filename": "fast_agent_tests_context.md",
        "ignore": ["*.png", "*.jpg"]
    },
    {
        "repo_name": "servers",
        "sub_path": "src/everything", 
        "output_filename": "mcp_server_everything_context.md",
        "ignore": []
    },
    {
        "repo_name": "servers",
        "sub_path": "src/fetch", 
        "output_filename": "mcp_server_fetch_context.md",
        "ignore": []
    },
    {
        "repo_name": "servers",
        "sub_path": "src/filesystem", 
        "output_filename": "mcp_server_filesystem_context.md",
        "ignore": []
    },
    {
        "repo_name": "servers",
        "sub_path": "src/git", 
        "output_filename": "mcp_server_git_context.md",
        "ignore": []
    },
    {
        "repo_name": "servers",
        "sub_path": "src/time", 
        "output_filename": "mcp_server_time_context.md",
        "ignore": []
    },
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": "docs/specification", 
        "output_filename": "mcp_spec_full_version_history_context.md",
        "ignore": []
    },
    {
        "repo_name": "servers",
        "sub_path": ".", 
        "output_filename": "mcp_servers_full_directory_context.md",
        "ignore": ["src"]
    },
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": "docs/specification/draft", 
        "output_filename": "mcp_spec_schema_context.md",
        "ignore": []
    },
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": "docs/links/sdks", 
        "output_filename": "mcp_spec_sdk_links_context.md",
        "ignore": []
    },
    {
        "repo_name": "fast-agent",
        "sub_path": "scripts", 
        "output_filename": "fast_agent_dev_scripts_context.md",
        "ignore": []
    },
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": ".", 
        "output_filename": "mcp_spec_concepts_context.md",
        "ignore": ["docs", ".github", "schema", "LICENSE", ".gitignore", "CONTRIBUTING.md"]
    },
    {
        "repo_name": "fast-agent",
        "sub_path": ".", 
        "output_filename": "fast_agent_core_context.md",
        "ignore": ["src", "examples", "tests", "scripts", ".git", ".github", ".vscode", "dist"]
    },
]

# Output directory configuration
OUTPUT_DIR = "generated_context"

def get_packaging_jobs() -> List[Dict[str, Any]]:
    """Get the list of packaging jobs."""
    return PACKAGING_JOBS

def get_default_ignore_patterns() -> set:
    """Get the default ignore patterns."""
    return DEFAULT_IGNORE_PATTERNS.copy()

def get_output_dir() -> str:
    """Get the output directory name."""
    return OUTPUT_DIR 