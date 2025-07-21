> Last updated: January 2025
# Context for MCP and fast-agent

This repository contains context files for building AI agents using the Model Context Protocol (MCP) and the `fast-agent` framework.

> **Note:** These files are generated from source repositories and are time-sensitive. They are primarily for my own use, but feel free to explore the generation scripts.

## Quick Start

```bash
# Generate context files from your cloned repos
python generate_context.py --root-dir "path/to/your/repos"

# Output to the 'generated_context' folder in this project (regardless of config)
python generate_context.py --root-dir "path/to/your/repos" --output-here
# or using the short form
python generate_context.py --root-dir "path/to/your/repos" -oh

# With custom max file size (5MB)
python generate_context.py --root-dir "path/to/your/repos" -oh --max-file-size 5242880

# Optimize the generated files (optional)
python optimize_context.py
```

## Scripts

- **`generate_context.py`** - Creates context files from source repositories
- **`optimize_context.py`** - Optimizes context files for token efficiency
- **`download_docs_llms.py`** - Downloads documentation for LLM processing

## Features

- **Modular design** with configuration in `config_context.py`
- **Token counting** (optional: `pip install tiktoken` for accurate counting)
- **Progress tracking** and detailed statistics
- **Graceful fallbacks** for missing dependencies
- **Smart file filtering** with comprehensive ignore patterns
- **Configurable max file size** to avoid processing large files
- **Flexible output location**: use `--output-here`/`-oh` to always output to this repo's `generated_context` folder

## Directory Structure

- **`generated_context/`** - Full context files from source code
- **`optimized_context/`** - Token-efficient versions for LLM use
- **`context_generator/`** - Modular packaging logic
- **`config_context.py`** - Configuration for packaging jobs

## Configuration

Packaging jobs (what gets included in each context file) are defined in `config_context.py`. By default, no jobs are hardcoded for 'fast-agent' or 'servers'—edit the config to suit your needs.

## Example Execution Log

<details>
<summary>Click to see the console output from a successful run</summary>

```text
🚀 Starting context generation...
   Root directory: /path/to/repos
   Output directory: generated_context
   Jobs to process: 12+
   🧮 Token counting: Available (tiktoken)

📋 Processing job 1/12+: my-repo/examples
📦 Packaging 'my-repo/examples' into 'generated_context/my_repo_examples_context.md'...
✅ Successfully packaged 'generated_context/my_repo_examples_context.md'.
   📊 25 files, 12,847 tokens
   📈 Average: 514 tokens/file
--------------------------------------------------

📊 Generation Summary:
   ✅ Successful: 12+
   ❌ Failed: 0
   📁 Total: 12+
   📄 Files processed: 1,000+
   🧮 Total tokens: 200,000+
   📈 Average tokens/file: ~200

🎉 All jobs completed successfully!
```
</details>
```