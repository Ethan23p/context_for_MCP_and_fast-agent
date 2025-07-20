> Last updated: January 2025
# Context for MCP and fast-agent

This repository contains context files for building AI agents using the Model Context Protocol (MCP) and the `fast-agent` framework.

> **Note:** These files are generated from source repositories and are time-sensitive. They are primarily for my own use, but feel free to explore the generation scripts.

## Quick Start

```bash
# Generate context files from your cloned repos
python generate_context.py --root-dir "path/to/your/repos"

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

## Directory Structure

- **`generated_context/`** - Full context files from source code
- **`optimized_context/`** - Token-efficient versions for LLM use
- **`context_generator/`** - Modular packaging logic
- **`config_context.py`** - Configuration for packaging jobs

## Example Execution Log

<details>
<summary>Click to see the console output from a successful run</summary>

```text
🚀 Starting context generation...
   Root directory: /path/to/repos
   Output directory: generated_context
   Jobs to process: 14
   🧮 Token counting: Available (tiktoken)

📋 Processing job 1/14: fast-agent/examples
📦 Packaging 'fast-agent/examples' into 'generated_context/fast_agent_examples_context.md'...
✅ Successfully packaged 'generated_context/fast_agent_examples_context.md'.
   📊 25 files, 12,847 tokens
   📈 Average: 514 tokens/file
--------------------------------------------------

📊 Generation Summary:
   ✅ Successful: 14
   ❌ Failed: 0
   📁 Total: 14
   📄 Files processed: 342
   🧮 Total tokens: 156,234
   📈 Average tokens/file: 457

🎉 All jobs completed successfully!
```
</details>
```
