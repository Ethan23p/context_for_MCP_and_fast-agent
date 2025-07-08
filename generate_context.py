import os
import fnmatch
import argparse
from pathlib import Path
from typing import List, Set

# --- CONFIGURATION ---
OUTPUT_DIR = "generated_context"

# --- Helper Functions ---

def should_ignore(path: Path, root_path: Path, ignore_patterns: Set[str]) -> bool:
    try:
        relative_path = str(path.relative_to(root_path)).replace(os.path.sep, '/')
        for pattern in ignore_patterns:
            if fnmatch.fnmatch(relative_path, pattern):
                return True
    except ValueError:
        return True
    return False

def build_tree(current_path: Path, root_path: Path, ignore_patterns: Set[str], prefix: str = "") -> str:
    tree_lines = []
    try:
        items = sorted([p for p in current_path.iterdir()], key=lambda p: (p.is_file(), p.name.lower()))
    except FileNotFoundError:
        return ""
    
    valid_items = [item for item in items if not should_ignore(item, root_path, ignore_patterns)]

    for i, item in enumerate(valid_items):
        is_last = (i == len(valid_items) - 1)
        connector = "└── " if is_last else "├── "
        icon = "📄" if item.is_file() else "📁"
        tree_lines.append(f"{prefix}{connector}{icon} {item.name}")
        
        if item.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_lines.extend(build_tree(item, root_path, ignore_patterns, new_prefix).splitlines())
            
    return "\n".join(tree_lines)

def write_file_contents(output_f, current_path: Path, root_path: Path, ignore_patterns: Set[str]):
    try:
        items = sorted([p for p in current_path.iterdir()], key=lambda p: (p.is_file(), p.name.lower()))
    except FileNotFoundError:
        return

    for item in items:
        if should_ignore(item, root_path, ignore_patterns):
            continue
            
        if item.is_file():
            relative_path_str = str(item.relative_to(root_path)).replace(os.path.sep, '/')
            output_f.write(f"--- START OF FILE {relative_path_str} ---\n")
            try:
                content = item.read_text(encoding='utf-8', errors='replace')
                output_f.write(f"{content}\n")
            except Exception as e:
                output_f.write(f"[Error reading file: {e}]\n")
            output_f.write(f"--- END OF FILE {relative_path_str} ---\n\n\n")
        elif item.is_dir():
            write_file_contents(output_f, item, root_path, ignore_patterns)

def package_project(source_path: Path, output_path: Path, ignore_patterns: List[str]):
    print(f"📦 Packaging '{source_path}' into '{output_path}'...")
    
    default_ignores = {".git", ".venv", "__pycache__", ".vscode", "*.pyc", "*.bak", "*.optimized.*", "dist", "node_modules", ".DS_Store"}
    all_ignores = default_ignores.union(set(ignore_patterns))

    with output_path.open("w", encoding="utf-8") as f:
        f.write(f"# Project: {source_path.name}\n\n")
        f.write("## Directory Structure\n\n```\n")
        tree_str = f"📁 {source_path.name}\n" + build_tree(source_path, source_path, all_ignores)
        f.write(tree_str)
        f.write("\n```\n\n------------------------------------------------------------\n\n## File Contents\n\n")
        write_file_contents(f, source_path, source_path, all_ignores)
        f.write("\n--- PROJECT PACKAGING COMPLETE ---")
    
    print(f"✅ Successfully packaged '{output_path}'.")

# --- Main Execution ---

def main():
    parser = argparse.ArgumentParser(description="Regenerate full context files from source repositories.")
    parser.add_argument("--root-dir", required=True, help="The root directory containing the cloned repositories.")
    args = parser.parse_args()
    
    root_dir = Path(args.root_dir)
    if not root_dir.is_dir():
        print(f"❌ Error: Root directory not found at '{root_dir}'")
        return

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    print(f"✅ Created output directory: '{output_dir}'\n")

    packaging_jobs = [
        {"repo_name": "fast-agent", "sub_path": "examples", "output_filename": "fast_agent_examples_context.md", "ignore": ["*.png", "*.jpg", "*.jpeg", "*.ico"]},
        {"repo_name": "fast-agent", "sub_path": "tests", "output_filename": "fast_agent_tests_context.md", "ignore": ["*.png", "*.jpg"]},
        {"repo_name": "servers", "sub_path": "src/everything", "output_filename": "mcp_server_everything_context.md", "ignore": []},
        {"repo_name": "servers", "sub_path": "src/fetch", "output_filename": "mcp_server_fetch_context.md", "ignore": []},
        {"repo_name": "servers", "sub_path": "src/filesystem", "output_filename": "mcp_server_filesystem_context.md", "ignore": []},
        {"repo_name": "servers", "sub_path": "src/git", "output_filename": "mcp_server_git_context.md", "ignore": []},
        {"repo_name": "servers", "sub_path": "src/time", "output_filename": "mcp_server_time_context.md", "ignore": []},
        {"repo_name": "modelcontextprotocol", "sub_path": "docs/specification", "output_filename": "mcp_spec_full_version_history_context.md", "ignore": []},
        {"repo_name": "servers", "sub_path": ".", "output_filename": "mcp_servers_full_directory_context.md", "ignore": ["src"]},
        {"repo_name": "modelcontextprotocol", "sub_path": "docs/specification/draft", "output_filename": "mcp_spec_schema_context.md", "ignore": []},
        {"repo_name": "modelcontextprotocol", "sub_path": "docs/links/sdks", "output_filename": "mcp_spec_sdk_links_context.md", "ignore": []},
        {"repo_name": "fast-agent", "sub_path": "scripts", "output_filename": "fast_agent_dev_scripts_context.md", "ignore": []},
        {"repo_name": "modelcontextprotocol", "sub_path": ".", "output_filename": "mcp_spec_concepts_context.md", "ignore": ["docs", ".github", "schema", "LICENSE", ".gitignore", "CONTRIBUTING.md"]},
        {"repo_name": "fast-agent", "sub_path": ".", "output_filename": "fast_agent_core_context.md", "ignore": ["src", "examples", "tests", "scripts", ".git", ".github", ".vscode", "dist"]},
    ]

    print(f"--- Starting context regeneration from source repos in '{root_dir}' into '{output_dir}' ---\n")

    for job in packaging_jobs:
        repo_path = root_dir / job["repo_name"]
        source_path = repo_path / job["sub_path"]
        
        if not source_path.exists():
            print(f"⚠️ Warning: Source path not found, skipping job. Path: '{source_path}'")
            continue
            
        output_path = output_dir / job["output_filename"]
        package_project(source_path, output_path, job["ignore"])
        print("-" * 20)

    print("✅ All regeneration tasks complete.")

if __name__ == "__main__":
    main()