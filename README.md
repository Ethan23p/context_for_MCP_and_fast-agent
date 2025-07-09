> Last updated: July 8th 2025
# Context for MCP and fast-agent

This repository contains my latest context files for building AI agents using the Model Context Protocol (MCP) and the `fast-agent` framework.

> **Note:** These files are generated from specific commits of their source repositories and are highly time-sensitive. They are primarily for my own use, but feel free to explore the generation and optimization scripts.

## Workflow

This repository contains two primary Python scripts to create and manage the context files.

### 1. Generate Full Context

First, run the `regenerate_context.py` script to create the full, un-optimized context files from the source repositories. This script requires you to have the `fast-agent`, `servers`, and `modelcontextprotocol` repositories cloned locally.

```bash
# Point this to the directory containing the source repos
python regenerate_context.py --root-dir "path/to/your/repos"
```

This will create the `generated_context/` directory with the complete, unabridged files.

### 2. Optimize Context

Next, run the `optimize_docs.py` script. It reads the files from `generated_context/` and applies a series of optimizations (e.g., summarizing code, trimming data) to create smaller, more token-efficient versions.

```bash
python optimize_docs.py
```

This will create the `optimized_context/` directory, containing the final files ready for use in an LLM.

## Directory Structure

-   **`generated_context/`**: Contains the full, unabridged context files generated directly from the source code.
-   **`optimized_context/`**: Contains the smaller, token-efficient versions of the context files, ready for use.
-   **`regenerate_context.py`**: The script used to generate the files in `generated_context/`.
-   **`optimize_docs.py`**: The script used to process the files in `generated_context/` and create the final files in `optimized_context/`.

## Example Execution Log

<details>
<summary>Click to see the console output from a successful run</summary>

```text
PS E:\Hume General\Programming\Repos\script clone> python regenerate_context.py --root-dir "E:/Hume General/AI Resources"
✅ Created output directory: 'generated_context'

--- Starting context regeneration from source repos in 'E:\Hume General\AI Resources' into 'generated_context' ---

📦 Packaging 'E:\Hume General\AI Resources\fast-agent\examples' into 'generated_context\fast_agent_examples_context.md'...
✅ Successfully packaged 'generated_context\fast_agent_examples_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\fast-agent\tests' into 'generated_context\fast_agent_tests_context.md'...
✅ Successfully packaged 'generated_context\fast_agent_tests_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers\src\everything' into 'generated_context\mcp_server_everything_context.md'...
✅ Successfully packaged 'generated_context\mcp_server_everything_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers\src\fetch' into 'generated_context\mcp_server_fetch_context.md'...
✅ Successfully packaged 'generated_context\mcp_server_fetch_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers\src\filesystem' into 'generated_context\mcp_server_filesystem_context.md'...
✅ Successfully packaged 'generated_context\mcp_server_filesystem_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers\src\git' into 'generated_context\mcp_server_git_context.md'...
✅ Successfully packaged 'generated_context\mcp_server_git_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers\src\time' into 'generated_context\mcp_server_time_context.md'...
✅ Successfully packaged 'generated_context\mcp_server_time_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\modelcontextprotocol\docs\specification' into 'generated_context\mcp_spec_full_version_history_context.md'...
✅ Successfully packaged 'generated_context\mcp_spec_full_version_history_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\servers' into 'generated_context\mcp_servers_full_directory_context.md'...
✅ Successfully packaged 'generated_context\mcp_servers_full_directory_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\modelcontextprotocol\docs\specification\draft' into 'generated_context\mcp_spec_schema_context.md'...
✅ Successfully packaged 'generated_context\mcp_spec_schema_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\modelcontextprotocol\docs\links\sdks' into 'generated_context\mcp_spec_sdk_links_context.md'...
✅ Successfully packaged 'generated_context\mcp_spec_sdk_links_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\fast-agent\scripts' into 'generated_context\fast_agent_dev_scripts_context.md'...
✅ Successfully packaged 'generated_context\fast_agent_dev_scripts_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\modelcontextprotocol' into 'generated_context\mcp_spec_concepts_context.md'...
✅ Successfully packaged 'generated_context\mcp_spec_concepts_context.md'.
--------------------
📦 Packaging 'E:\Hume General\AI Resources\fast-agent' into 'generated_context\fast_agent_core_context.md'...
✅ Successfully packaged 'generated_context\fast_agent_core_context.md'.
--------------------
✅ All regeneration tasks complete.
PS E:\Hume General\Programming\Repos\script clone> python optimize_docs.py
✅ Created output directory: 'optimized_context'

--- (1/5) Summarizing Server Implementation Files ---
✅ Optimized "mcp_server_filesystem_context.md"
  - Original Size: 107,145 bytes
  - New Size:      982 bytes
  - Reduction:     106,163 bytes (99.08%)

✅ Optimized "mcp_server_fetch_context.md"
  - Original Size: 124,349 bytes
  - New Size:      250 bytes
  - Reduction:     124,099 bytes (99.8%)

✅ Optimized "mcp_server_git_context.md"
  - Original Size: 85,361 bytes
  - New Size:      1,005 bytes
  - Reduction:     84,356 bytes (98.82%)

✅ Optimized "mcp_server_time_context.md"
  - Original Size: 95,534 bytes
  - New Size:      275 bytes
  - Reduction:     95,259 bytes (99.71%)

✅ Optimized "mcp_server_everything_context.md"
  - Original Size: 53,263 bytes
  - New Size:      1,012 bytes
  - Reduction:     52,251 bytes (98.1%)

--- (2/5) Condensing: mcp_servers_full_directory_context.md ---
✅ Optimized "mcp_servers_full_directory_context.md"
  - Original Size: 492,780 bytes
  - New Size:      299,906 bytes
  - Reduction:     192,874 bytes (39.14%)

--- (3/5) Processing: fast_agent_examples_context.md ---
✅ Optimized "fast_agent_examples_context.md"
  - Original Size: 342,206 bytes
  - New Size:      115,809 bytes
  - Reduction:     226,397 bytes (66.16%)

--- (4/5) Processing: fast_agent_tests_context.md ---
✅ Optimized "fast_agent_tests_context.md"
  - Original Size: 2,464,475 bytes
  - New Size:      9,476 bytes
  - Reduction:     2,454,999 bytes (99.62%)

--- (5/5) Processing: mcp_spec_full_version_history_context.md ---
✅ Optimized "mcp_spec_full_version_history_context.md"
  - Original Size: 609,445 bytes
  - New Size:      4,687 bytes
  - Reduction:     604,758 bytes (99.23%)

---
✅ All optimizations complete! Optimized files are in the 'optimized_context' directory.
```
</details>
```
