"""
Configuration for the context generation script.
Contains all packaging jobs and default settings.
"""

from typing import List, Dict, Any

# Default ignore patterns applied to all jobs
DEFAULT_IGNORE_PATTERNS = {
    # Version control
    ".git", ".svn", ".hg",
    
    # Python
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.so", "*.egg", "*.egg-info",
    ".pytest_cache", ".coverage", "htmlcov", ".tox", ".mypy_cache",
    
    # Virtual environments
    ".venv", "venv", "env", ".env", "ENV",
    
    # IDEs and editors
    ".vscode", ".idea", "*.swp", "*.swo", "*~", ".vs",
    
    # Build and distribution
    "dist", "build", "*.egg-info", "*.whl", "node_modules",
    
    # OS and temp files
    ".DS_Store", "Thumbs.db", "*.tmp", "*.temp", "*.bak", "*.backup",
    
    # Logs and databases
    "*.log", "*.sqlite", "*.db", "*.sqlite3",
    
    # Media files (usually not needed for context)
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.ico", "*.svg",
    "*.mp4", "*.avi", "*.mov", "*.wav", "*.mp3", "*.pdf",
    
    # Archives
    "*.zip", "*.tar", "*.gz", "*.rar", "*.7z",
    
    # Large data files
    "*.csv", "*.parquet", "*.h5",
    
    # Optimized files (from this script)
    "*.optimized.*",
    
    "**/*.jsonl",
    "**/*.TEST_ONLY",
    
    "**/*lock*",
    "**/package.json",
    "**/tsconfig.json", 
    "**/jest.config.cjs",
    "**/pyproject.toml",
    "**/.python-version",
    "**/Dockerfile",
    "**/.npmrc"
}

# All packaging jobs configuration
PACKAGING_JOBS: List[Dict[str, Any]] = [
    # TEXTUAL: I. Core Application Structure & Lifecycle
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_core_app_structure_context.md",
        "include": [
            "examples/app/simple02.py",
            "examples/guide/dom2.py",
            "examples/app/event01.py",
            "examples/app/question01.py",
            "examples/app/suspend.py",
            "blog/posts/anatomy-of-a-textual-user-interface.md"
        ]
    },
    # II. Styling with CSS (TCSS)
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_styling_css_context.md",
        "include": [
            "examples/app/question02.py",
            "examples/app/question02.tcss",
            "examples/app/question03.py",
            "examples/guide/css/nesting02.py",
            "examples/guide/css/nesting02.tcss",
            "examples/styles/border_all.py",
            "examples/styles/text_style_all.py",
            "examples/styles/background_transparency.py",
            "examples/themes/todo_app.py",
            "css_types/_template.md"
        ]
    },
    # III. Layout Management
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_layout_management_context.md",
        "include": [
            "examples/guide/layout/vertical_layout.py",
            "examples/guide/layout/horizontal_layout.py",
            "examples/guide/layout/grid_layout1.py",
            "examples/guide/layout/combining_layouts.py",
            "examples/guide/layout/dock_layout1_sidebar.py",
            "examples/guide/layout/layers.py",
            "how-to/center-things.md",
            "how-to/work-with-containers.md",
            "how-to/design-a-layout.md"
        ]
    },
    # IV. Event Handling & Reactivity
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_event_handling_reactivity_context.md",
        "include": [
            "examples/events/custom01.py",
            "examples/events/on_decorator02.py",
            "examples/events/prevent.py",
            "examples/guide/reactivity/refresh01.py",
            "examples/guide/reactivity/refresh02.py",
            "examples/guide/reactivity/validate01.py",
            "examples/guide/reactivity/watch01.py",
            "examples/guide/reactivity/computed01.py",
            "examples/guide/reactivity/world_clock02.py",
            "examples/events/dictionary.py"
        ]
    },
    # V. Input & Interaction
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_input_interaction_context.md",
        "include": [
            "examples/guide/input/key01.py",
            "examples/guide/input/mouse01.py",
            "examples/guide/input/binding01.py",
            "examples/widgets/input_validation.py",
            "examples/widgets/masked_input.py"
        ]
    },
    # VI. Widget-Specific Examples
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_widget_examples_context.md",
        "include": [
            "examples/widgets/button.py",
            "examples/widgets/checkbox.py",
            "examples/widgets/collapsible.py",
            "examples/widgets/data_table.py",
            "examples/widgets/data_table_sort.py",
            "examples/widgets/digits.py",
            "examples/widgets/directory_tree.py",
            "examples/widgets/input.py",
            "examples/widgets/list_view.py",
            "examples/widgets/loading_indicator.py",
            "examples/widgets/log.py",
            "examples/widgets/markdown_viewer.py",
            "examples/widgets/markdown.py",
            "examples/widgets/option_list_options.py",
            "examples/widgets/placeholder.py",
            "examples/widgets/pretty.py",
            "examples/widgets/progress_bar.py",
            "examples/widgets/radiobutton.py",
            "examples/widgets/radioset.py",
            "examples/widgets/rich_log.py",
            "examples/widgets/rule.py",
            "examples/widgets/select_widget.py",
            "examples/widgets/selection_list_selections.py",
            "examples/widgets/sparkline.py",
            "examples/widgets/switch.py",
            "examples/widgets/tabs.py",
            "examples/widgets/tabbed_content.py",
            "examples/widgets/text_area_example.py",
            "examples/widgets/text_area_custom_language.py",
            "examples/widgets/tree.py",
            "examples/widgets/toast.py",
            "examples/widgets/link.py"
        ]
    },
    # VII. Advanced Topics & Utilities
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_advanced_topics_context.md",
        "include": [
            "examples/guide/workers/weather03.py",
            "examples/guide/workers/weather05.py",
            "examples/guide/command_palette/command02.py",
            "examples/guide/widgets/checker04.py",
            "examples/guide/compound/byte03.py",
            "examples/guide/testing/test_rgb.py",
            "how-to/package-with-hatch.md",
            "how-to/style-inline-apps.md",
            "how-to/render-and-compose.md",
            "blog/posts/steal-this-code.md",
            "blog/posts/rich-inspect.md",
            "blog/posts/toolong-retrospective.md",
            "blog/posts/textual-web.md",
            "blog/posts/textual-serve-files.md"
        ]
    },
    # VIII. Comprehensive Tutorials & Demos
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_tutorials_demos_context.md",
        "include": [
            "tutorial.md"
        ]
    },
    # MCP: Part 1 - Project Overview & Philosophy (SAFE)
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": ".",
        "output_filename": "mcp_overview_philosophy_context.md",
        "include": [
            "README.md",
            "docs/introduction.mdx",
            "docs/faqs.mdx",
            "docs/development/roadmap.mdx",
            "docs/community/governance.mdx",
            "docs/community/sep-guidelines.mdx"
        ]
    },
    # MCP: Part 2 - Core Concepts (CURATED)
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": ".",
        "output_filename": "mcp_core_concepts_context.md",
        "include": [
            "docs/docs/concepts/roots.mdx",
            "docs/docs/concepts/sampling.mdx"
        ]
    },
    # MCP: Part 3 - Formal Specification (ESSENTIAL)
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": ".",
        "output_filename": "mcp_formal_specification_context.md",
        "include": [
            "docs/specification/versioning.mdx",
            "docs/specification/draft/index.mdx",
            "docs/specification/draft/changelog.mdx",
            "docs/specification/draft/schema.mdx",
            "docs/specification/draft/architecture/index.mdx",
            "docs/specification/draft/basic/index.mdx",
            "docs/specification/draft/basic/lifecycle.mdx",
            "docs/specification/draft/basic/transports.mdx",
            "docs/specification/draft/basic/authorization.mdx",
            "docs/specification/draft/basic/security_best_practices.mdx",
            "docs/specification/draft/client/elicitation.mdx",
            "docs/specification/draft/client/roots.mdx",
            "docs/specification/draft/client/sampling.mdx",
            "docs/specification/draft/server/index.mdx",
            "docs/specification/draft/server/prompts.mdx",
            "docs/specification/draft/server/resources.mdx",
            "docs/specification/draft/server/tools.mdx"
        ]
    },
    # MCP: Part 4 - Practical Guides & Examples (SAFE)
    {
        "repo_name": "modelcontextprotocol",
        "sub_path": ".",
        "output_filename": "mcp_guides_examples_context.md",
        "include": [
            "docs/quickstart/user.mdx",
            "docs/tutorials/building-mcp-with-llms.mdx",
            "docs/docs/tools/inspector.mdx",
            "docs/docs/tools/debugging.mdx"
        ]
    },
    # FAST-AGENT: Core Examples and Tests
    {
        "repo_name": "fast-agent",
        "sub_path": ".",
        "output_filename": "fast_agent_core_context.md",
        "include": [
            "examples/**",
            "tests/e2e/**",
            "tests/integration/**",
            "scripts/event_replay.py",
            "scripts/event_summary.py",
            "scripts/test_package_install.sh"
        ]
    },
    # MCP SERVERS: Core Documentation
    {
        "repo_name": "servers",
        "sub_path": ".",
        "output_filename": "mcp_servers_context.md",
        "include": [
            "README.md"
        ]
    }
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