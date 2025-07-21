import os
import re
import shutil
from pathlib import Path

# --- SCRIPT CONFIGURATION ---
SOURCE_DIR = "generated_context"
OUTPUT_DIR = "optimized_context"

SERVER_SUMMARIES = {
    "mcp_server_filesystem_context.md": """# Filesystem Server Summary
Provides tools for filesystem operations within allowed directories.
## Tools
- **read_file(path, [tail], [head])**: Reads a file's content, optionally the first or last N lines.
- **read_multiple_files(paths)**: Reads several files at once.
- **write_file(path, content)**: Creates or overwrites a file.
- **edit_file(path, edits, [dryRun])**: Applies line-based edits to a file.
- **create_directory(path)**: Creates a directory.
- **list_directory(path)**: Lists contents of a directory.
- **list_directory_with_sizes(path, [sortBy])**: Lists directory contents with file sizes.
- **directory_tree(path)**: Returns a JSON tree of a directory.
- **move_file(source, destination)**: Moves or renames a file.
- **search_files(path, pattern, [excludePatterns])**: Recursively searches for files.
- **get_file_info(path)**: Retrieves metadata for a file or directory.
- **list_allowed_directories()**: Lists all accessible root directories.
""",
    "mcp_server_fetch_context.md": """# Fetch Server Summary
Provides tools to fetch web content and convert it to Markdown.
## Tools
- **fetch(url, [max_length], [start_index], [raw])**: Fetches a URL and extracts its content.
## Prompts
- **fetch(url)**: A prompt to fetch a URL.
""",
    "mcp_server_git_context.md": """# Git Server Summary
Provides tools to interact with Git repositories.
## Tools
- **git_status(repo_path)**: Shows working tree status.
- **git_diff_unstaged(repo_path, [context_lines])**: Shows unstaged changes.
- **git_diff_staged(repo_path, [context_lines])**: Shows staged changes.
- **git_diff(repo_path, target, [context_lines])**: Shows differences between branches/commits.
- **git_commit(repo_path, message)**: Records changes to the repository.
- **git_add(repo_path, files)**: Adds files to the staging area.
- **git_reset(repo_path)**: Unstages all changes.
- **git_log(repo_path, [max_count])**: Shows commit logs.
- **git_create_branch(repo_path, branch_name, [base_branch])**: Creates a new branch.
- **git_checkout(repo_path, branch_name)**: Switches branches.
- **git_show(repo_path, revision)**: Shows the contents of a commit.
- **git_init(repo_path)**: Initializes a Git repository.
- **git_branch(repo_path, branch_type, [contains], [not_contains])**: Lists branches.
""",
    "mcp_server_time_context.md": """# Time Server Summary
Provides tools for time and timezone conversions.
## Tools
- **get_current_time(timezone)**: Gets the current time in a specific IANA timezone.
- **convert_time(source_timezone, time, target_timezone)**: Converts a time between two IANA timezones.
""",
    "mcp_server_everything_context.md": """# Everything Server Summary
A comprehensive test server demonstrating all MCP features.
## Tools
- **echo(message)**: Echoes back the input.
- **add(a, b)**: Adds two numbers.
- **longRunningOperation(duration, steps)**: Simulates a long task with progress updates.
- **printEnv()**: Prints all environment variables.
- **sampleLLM(prompt, maxTokens)**: Requests a completion from the client's LLM.
- **getTinyImage()**: Returns a small test image.
- **annotatedMessage(messageType, includeImage)**: Demonstrates content annotations.
- **getResourceReference(resourceId)**: Returns an embedded resource.
- **getResourceLinks(count)**: Returns multiple resource links.
## Resources
- Provides 100 paginated test resources (even IDs are text, odd IDs are binary). URI: `test://static/resource/{id}`
## Prompts
- **simple_prompt**: A prompt with no arguments.
- **complex_prompt(temperature, [style])**: A prompt with arguments.
- **resource_prompt(resourceId)**: A prompt that embeds a resource.
"""
}

# --- HELPER FUNCTIONS ---

def report_progress(file_name, original_size, new_size):
    reduction = original_size - new_size
    reduction_percent = round((reduction / original_size) * 100, 2) if original_size > 0 else 0
    print(f"✅ Optimized \"{file_name}\"")
    print(f"  - Original Size: {original_size:,} bytes")
    print(f"  - New Size:      {new_size:,} bytes")
    print(f"  - Reduction:     {reduction:,} bytes ({reduction_percent}%)")
    print("")

# --- OPTIMIZATION FUNCTIONS ---

def summarize_server_files(source_dir, output_dir):
    print(f"--- (1/5) Summarizing Server Implementation Files ---")
    for filename, summary in SERVER_SUMMARIES.items():
        source_path = source_dir / filename
        if source_path.exists():
            new_name = source_path.name.replace('_context', '_optimized')
            dest_path = output_dir / new_name
            original_size = source_path.stat().st_size
            dest_path.write_text(summary, encoding='utf-8')
            new_size = dest_path.stat().st_size
            report_progress(filename, original_size, new_size)
        else:
            print(f"⚠️ Source file not found, skipping: {source_path}")

def condense_server_directory(source_dir, output_dir):
    filename = "mcp_servers_full_directory_context.md"
    print(f"--- (2/5) Condensing: {filename} ---")
    source_path = source_dir / filename
    if not source_path.exists():
        print(f"⚠️ Source file not found, skipping: {source_path}")
        return

    new_name = source_path.name.replace('_context', '_optimized')
    dest_path = output_dir / new_name
    original_content = source_path.read_text(encoding='utf-8')
    original_size = len(original_content.encode('utf-8'))
    
    table_regex = re.compile(r"(?ms)(## 🤝 Third-Party Servers.*?)(?=\n## 📚 Frameworks)")
    table_match = table_regex.search(original_content)

    if not table_match:
        print(f"⚠️ Could not find server table in {filename}. Copying original file.")
        shutil.copy2(source_path, dest_path)
        return

    table_content = table_match.group(1)
    new_table_lines = ["## 🤝 Third-Party Servers"]
    row_regex = re.compile(r"(?m)^\|\s*<img.*?\[(.*?)\]\(.*?\)\*\*.*?\|\s*(.*?)\s*\|$")

    for line in table_content.splitlines():
        if line.startswith("###"):
            new_table_lines.append(f"\n{line}\n")
        elif line.startswith("| <img"):
            row_match = row_regex.search(line)
            if row_match:
                new_table_lines.append(f"- **{row_match.group(1).strip()}**: {row_match.group(2).strip()}")

    new_table_section = "\n".join(new_table_lines)
    new_content = table_regex.sub(new_table_section, original_content, count=1)
    
    dest_path.write_text(new_content, encoding='utf-8')
    new_size = len(new_content.encode('utf-8'))
    report_progress(filename, original_size, new_size)

def trim_csv_data(source_dir, output_dir):
    filename = "fast_agent_examples_context.md"
    print(f"--- (3/5) Processing: {filename} ---")
    source_path = source_dir / filename
    if not source_path.exists():
        print(f"⚠️ Source file not found, skipping: {source_path}")
        return

    new_name = source_path.name.replace('_context', '_optimized')
    dest_path = output_dir / new_name
    content = source_path.read_text(encoding='utf-8')
    original_size = len(content.encode('utf-8'))

    csv_filename = "WA_Fn-UseC_-HR-Employee-Attrition.csv"
    start_marker = re.escape(f"--- START OF FILE") + r".*?" + re.escape(csv_filename) + re.escape(" ---")
    end_marker = re.escape(f"--- END OF FILE") + r".*?" + re.escape(csv_filename) + re.escape(" ---")
    placeholder = "[Contents of a 1470-row CSV file about employee attrition are included here for the data-analysis example.]"
    
    regex = re.compile(f"({start_marker}\\r?\\n)(.*?)(\\r?\\n{end_marker})", re.DOTALL)
    new_content, count = regex.subn(f"\\1\n{placeholder}\n\\3", content)
    
    if count == 0:
        print(f"⚠️ Could not find CSV block in {filename}. Copying original file.")
        shutil.copy2(source_path, dest_path)
        return

    dest_path.write_text(new_content, encoding='utf-8')
    new_size = len(new_content.encode('utf-8'))
    report_progress(filename, original_size, new_size)

def curate_test_suite(source_dir, output_dir):
    filename = "fast_agent_tests_context.md"
    print(f"--- (4/5) Processing: {filename} ---")
    source_path = source_dir / filename
    if not source_path.exists():
        print(f"⚠️ Source file not found, skipping: {source_path}")
        return

    new_name = source_path.name.replace('_context', '_optimized')
    dest_path = output_dir / new_name
    original_content = source_path.read_text(encoding='utf-8')
    original_size = len(original_content.encode('utf-8'))

    files_to_keep = [
        "tests/e2e/workflow/test_chain.py", "tests/e2e/workflow/test_router_agent_e2e.py",
        "tests/e2e/workflow/test_evaluator_optimizer.py", "tests/e2e/smoke/base/test_e2e_smoke.py",
        "tests/e2e/multimodal/test_multimodal_images.py", "tests/e2e/structured/test_structured_outputs.py"
    ]

    all_blocks = re.split(r'(--- START OF FILE .*? ---)', original_content)
    new_content_blocks = [all_blocks[0]] if all_blocks else []

    for i in range(1, len(all_blocks), 2):
        header, body_and_rest = all_blocks[i], all_blocks[i+1]
        if any(file_to_keep in header for file_to_keep in files_to_keep):
            end_marker_match = re.search(r'--- END OF FILE .*? ---', body_and_rest)
            if end_marker_match:
                new_content_blocks.append(header + body_and_rest[:end_marker_match.end()])

    new_content = "\n".join(new_content_blocks)
    dest_path.write_text(new_content, encoding='utf-8')
    new_size = len(new_content.encode('utf-8'))
    report_progress(filename, original_size, new_size)

def trim_spec_history(source_dir, output_dir):
    filename = "mcp_spec_full_version_history_context.md"
    print(f"--- (5/5) Processing: {filename} ---")
    source_path = source_dir / filename
    if not source_path.exists():
        print(f"⚠️ Source file not found, skipping: {source_path}")
        return

    new_name = source_path.name.replace('_context', '_optimized')
    dest_path = output_dir / new_name
    original_content = source_path.read_text(encoding='utf-8')
    original_size = len(original_content.encode('utf-8'))

    versions_to_trim = ["2024-11-05", "2025-03-26"]
    versions_to_keep = ["2025-06-18", "draft"]
    new_content_blocks = []

    header_end_index = original_content.find("--- START OF FILE")
    if header_end_index != -1:
        new_content_blocks.append(original_content[:header_end_index])

    all_file_blocks = re.split(r'(--- START OF FILE .*? ---)', original_content)[1:]

    for i in range(0, len(all_file_blocks), 2):
        header, body_and_rest = all_file_blocks[i], all_file_blocks[i+1]
        end_marker_match = re.search(r'--- END OF FILE .*? ---', body_and_rest)
        if not end_marker_match: continue
        
        body = body_and_rest[:end_marker_match.end()]
        
        if any(f"specification/{v}/" in header for v in versions_to_keep) or \
           any(f"specification/{v}/changelog.mdx" in header for v in versions_to_trim):
            new_content_blocks.append(header + body)

    new_content = "\n\n".join(new_content_blocks)
    dest_path.write_text(new_content, encoding='utf-8')
    new_size = len(new_content.encode('utf-8'))
    report_progress(filename, original_size, new_size)

def main():
    """Main function to run all optimization steps."""
    source_dir = Path(SOURCE_DIR)
    output_dir = Path(OUTPUT_DIR)

    if not source_dir.is_dir():
        print(f"❌ Error: Source directory '{source_dir}' not found. Please run the regeneration script first.")
        return

    output_dir.mkdir(exist_ok=True)
    print(f"✅ Created output directory: '{output_dir}'\n")
    
    try:
        summarize_server_files(source_dir, output_dir)
        condense_server_directory(source_dir, output_dir)
        trim_csv_data(source_dir, output_dir)
        curate_test_suite(source_dir, output_dir)
        trim_spec_history(source_dir, output_dir)
        print("---")
        print(f"✅ All optimizations complete! Optimized files are in the '{OUTPUT_DIR}' directory.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()