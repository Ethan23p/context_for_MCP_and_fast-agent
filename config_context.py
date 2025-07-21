"""
Configuration for the project packaging script.
Contains all packaging jobs and default settings.
"""

# Default ignore patterns applied to all jobs
# These patterns are used to exclude common temporary files, logs, and environment folders.
DEFAULT_IGNORE_PATTERNS = {
    # Version control & IDEs
    ".git", ".svn", ".hg", ".vscode", ".idea", ".vs",
    
    # Python artifacts
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.so", "*.egg", "*.egg-info",
    ".pytest_cache", ".coverage", "htmlcov", ".tox", ".mypy_cache",
    
    # Virtual environments
    ".venv", "venv", "env", ".env", "ENV",
    
    # Build and distribution artifacts
    "dist", "build", "node_modules",
    
    # OS-specific and temporary files
    ".DS_Store", "Thumbs.db", "*.tmp", "*.temp", "*.bak", "*.swp",
    
    # Common logs and databases
    "*.log", "*.sqlite", "*.db", "*.sqlite3",
    
    # Large media and data files (usually not useful for code context)
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.mp4", "*.mp3", "*.pdf",
    "*.zip", "*.tar.gz", "*.rar", "*.csv", "*.parquet",
    
    # Specific project config files you might want to ignore globally
    "**/*lock*", "**/package.json", "**/pyproject.toml"
}

# The directory where the final context files will be saved.
OUTPUT_DIR = "generated_context"

# A list of all packaging jobs to be performed.
# Each job is a dictionary specifying the repository, the files to include,
# and the name of the output file.
PACKAGING_JOBS = [
    # To package an entire repository, create a job without an "include" key.
    # For example:
    # {
    #     "repo_name": "fast-agent",
    #     "sub_path": ".",
    #     "output_filename": "fast_agent_complete_context.md",
    # },

    # TEXTUAL: Core Application & Lifecycle
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_core_app_structure_context.md",
        "include": [
            "docs/examples/app/simple02.py",
            "docs/examples/guide/dom2.py",
            "docs/examples/app/event01.py",
            "docs/examples/app/question01.py",
            "docs/examples/app/suspend.py",
            "docs/blog/posts/anatomy-of-a-textual-user-interface.md"
        ]
    },
    # II. Styling with CSS (TCSS)
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_styling_css_context.md",
        "include": [
            "examples/calculator.py",
            "examples/code_browser.py",
            "examples/dictionary.py",
            "examples/five_by_five.py",
            "examples/calculator.tcss",
            "examples/code_browser.tcss",
            "examples/dictionary.tcss",
            "examples/five_by_five.tcss",
            "docs/examples/app/question02.py",
            "docs/examples/app/question02.tcss",
            "docs/examples/app/question03.py",
            "docs/examples/guide/css/nesting02.py",
            "docs/examples/guide/css/nesting02.tcss",
            "docs/examples/styles/border_all.py",
            "docs/examples/styles/text_style_all.py",
            "docs/examples/styles/background_transparency.py",
            "docs/examples/themes/todo_app.py",
            "docs/css_types/_template.md"
        ]
    },
    # III. Layout Management
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_layout_management_context.md",
        "include": [
            "docs/examples/guide/layout/vertical_layout.py",
            "docs/examples/guide/layout/horizontal_layout.py",
            "docs/examples/guide/layout/grid_layout1.py",
            "docs/examples/guide/layout/combining_layouts.py",
            "docs/examples/guide/layout/dock_layout1_sidebar.py",
            "docs/examples/guide/layout/layers.py",
            "docs/how-to/center-things.md",
            "docs/how-to/work-with-containers.md",
            "docs/how-to/design-a-layout.md"
        ]
    },
    # IV. Event Handling & Reactivity
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_event_handling_reactivity_context.md",
        "include": [
            "docs/examples/events/custom01.py",
            "docs/examples/events/on_decorator02.py",
            "docs/examples/events/prevent.py",
            "docs/examples/guide/reactivity/refresh01.py",
            "docs/examples/guide/reactivity/refresh02.py",
            "docs/examples/guide/reactivity/validate01.py",
            "docs/examples/guide/reactivity/watch01.py",
            "docs/examples/guide/reactivity/computed01.py",
            "docs/examples/guide/reactivity/world_clock02.py",
            "docs/examples/events/dictionary.py"
        ]
    },
    # V. Input & Interaction
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_input_interaction_context.md",
        "include": [
            "docs/examples/guide/input/key01.py",
            "docs/examples/guide/input/mouse01.py",
            "docs/examples/guide/input/binding01.py",
            "docs/examples/widgets/input_validation.py",
            "docs/examples/widgets/masked_input.py"
        ]
    },
    # VI. Widget-Specific Examples
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_widget_examples_context.md",
        "include": [
            "docs/examples/widgets/button.py",
            "docs/examples/widgets/checkbox.py",
            "docs/examples/widgets/collapsible.py",
            "docs/examples/widgets/data_table.py",
            "docs/examples/widgets/data_table_sort.py",
            "docs/examples/widgets/digits.py",
            "docs/examples/widgets/directory_tree.py",
            "docs/examples/widgets/input.py",
            "docs/examples/widgets/list_view.py",
            "docs/examples/widgets/loading_indicator.py",
            "docs/examples/widgets/log.py",
            "docs/examples/widgets/markdown_viewer.py",
            "docs/examples/widgets/markdown.py",
            "docs/examples/widgets/option_list_options.py",
            "docs/examples/widgets/placeholder.py",
            "docs/examples/widgets/pretty.py",
            "docs/examples/widgets/progress_bar.py",
            "docs/examples/widgets/radiobutton.py",
            "docs/examples/widgets/radioset.py",
            "docs/examples/widgets/rich_log.py",
            "docs/examples/widgets/rule.py",
            "docs/examples/widgets/select_widget.py",
            "docs/examples/widgets/selection_list_selections.py",
            "docs/examples/widgets/sparkline.py",
            "docs/examples/widgets/switch.py",
            "docs/examples/widgets/tabs.py",
            "docs/examples/widgets/tabbed_content.py",
            "docs/examples/widgets/text_area_example.py",
            "docs/examples/widgets/text_area_custom_language.py",
            "docs/examples/widgets/tree.py",
            "docs/examples/widgets/toast.py",
            "docs/examples/widgets/link.py"
        ]
    },
    # VII. Advanced Topics & Utilities
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_advanced_topics_context.md",
        "include": [
            "docs/examples/guide/workers/weather03.py",
            "docs/examples/guide/workers/weather05.py",
            "docs/examples/guide/command_palette/command02.py",
            "docs/examples/guide/widgets/checker04.py",
            "docs/examples/guide/compound/byte03.py",
            "docs/examples/guide/testing/test_rgb.py",
            "docs/how-to/package-with-hatch.md",
            "docs/how-to/style-inline-apps.md",
            "docs/how-to/render-and-compose.md",
            "docs/blog/posts/steal-this-code.md",
            "docs/blog/posts/rich-inspect.md",
            "docs/blog/posts/toolong-retrospective.md",
            "docs/blog/posts/textual-web.md",
            "docs/blog/posts/textual-serve-files.md"
        ]
    },
    # VIII. Comprehensive Tutorials & Demos
    {
        "repo_name": "textual",
        "sub_path": ".",
        "output_filename": "textual_tutorials_demos_context.md",
        "include": [
            "docs/tutorial.md"
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
    # FAST-AGENT: Examples
    {
        "repo_name": "fast-agent",
        "sub_path": ".",
        "output_filename": "fast_agent_examples_context.md",
        "include": [
            "examples/**"
        ]
    },
    # FAST-AGENT: Tests
    {
        "repo_name": "fast-agent",
        "sub_path": ".",
        "output_filename": "fast_agent_tests_context.md",
        "include": [
            "tests/e2e/**",
            "tests/integration/**"
        ]
    },
    # FAST-AGENT: Scripts
    {
        "repo_name": "fast-agent",
        "sub_path": ".",
        "output_filename": "fast_agent_scripts_context.md",
        "include": [
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