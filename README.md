> Last updated: July 2025
# Context for MCP and fast-agent

This repository contains context files for building AI agents using the Model Context Protocol (MCP) and the `fast-agent` framework.

> **Note:** These files are generated from source repositories and are time-sensitive. They are primarily for my own use, but feel free to explore the generation scripts.

## Quick Start

```sh
python generate_context.py --root-dir /path/to/your/repos --output-here
```
- Use `--output-here` (or `-oh`) to always output to a `generated_context` folder in this directory.
- You can set a max token limit per file with `--max-tokens` (default: 16000).

## Output

- Each job in `config_context.py` creates a markdown file in `generated_context/`.
- For fast-agent, you'll get:
  - `fast_agent_examples_context.md`
  - `fast_agent_tests_context.md`
  - `fast_agent_scripts_context.md`
- Other repos are split by topic or area as needed.

## Notes

- The script skips files that are too large (over the token limit), unless they're explicitly included.
- You can adjust which files are included by editing `config_context.py`.
- Token counting uses `tiktoken` if available, otherwise falls back to word count.

That's it. If you want to add or change what gets packaged, just update the config and rerun the script.