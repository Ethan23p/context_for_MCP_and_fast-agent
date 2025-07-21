#!/usr/bin/env python3
"""
A script to package repository contents into a single context file based on a configuration.
"""
import os
import fnmatch
import argparse
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

# Attempt to import tiktoken for accurate token counting, but fall back gracefully.
try:
    import tiktoken
    TOKEN_COUNTING_AVAILABLE = True
except ImportError:
    TOKEN_COUNTING_AVAILABLE = False

# --- Configuration Import ---
from config_context import PACKAGING_JOBS, DEFAULT_IGNORE_PATTERNS, OUTPUT_DIR


class Project:
    """
    Represents a project to be packaged, handling file discovery, filtering, and writing.
    """
    def __init__(self, source_path: Path, output_path: Path, include_patterns: Optional[List[str]] = None, max_tokens: int = 16000):
        self.source_path = source_path
        self.output_path = output_path
        self.include_patterns = include_patterns
        self.ignore_patterns = DEFAULT_IGNORE_PATTERNS
        # NEW: Maximum token limit for individual files.
        self.max_tokens = max_tokens
        self.stats = {"tokens": 0, "files": 0, "skipped_large": 0}

    def _count_tokens(self, text: str) -> int:
        """Counts tokens using tiktoken if available, otherwise falls back to word count."""
        if not text: return 0
        if TOKEN_COUNTING_AVAILABLE:
            try:
                encoding = tiktoken.get_encoding("cl100k_base")
                return len(encoding.encode(text, disallowed_special=()))
            except Exception:
                return len(text.split())
        return len(text.split())

    def _is_path_match(self, path: Path) -> bool:
        """Determines if a file's path matches the include/ignore patterns."""
        relative_path_str = path.relative_to(self.source_path).as_posix()

        if any(fnmatch.fnmatch(relative_path_str, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in self.ignore_patterns):
            return False

        if not self.include_patterns:
            return True

        return any(fnmatch.fnmatch(relative_path_str, pattern) for pattern in self.include_patterns)

    def _build_directory_tree(self, files: List[Path]) -> str:
        """Builds a string representation of the directory structure for the included files."""
        tree = {}
        for file in files:
            parts = file.relative_to(self.source_path).parts
            node = tree
            for part in parts:
                node = node.setdefault(part, {})
        
        def generate_tree_lines(d, prefix=""):
            lines = []
            items = sorted(d.keys(), key=lambda k: (not bool(d[k]), k))
            for i, name in enumerate(items):
                connector = "└── " if i == len(items) - 1 else "├── "
                lines.append(f"{prefix}{connector}{name}")
                if d[name]:
                    extension = "    " if i == len(items) - 1 else "│   "
                    lines.extend(generate_tree_lines(d[name], prefix + extension))
            return lines

        return "\n".join(generate_tree_lines(tree))

    def package(self) -> bool:
        """Main method to generate the context file. Returns True on success."""
        candidate_files = [path for path in self.source_path.rglob('*') if path.is_file() and self._is_path_match(path)]
        
        included_files = []
        for file_path in candidate_files:
            # The "include override" logic is here.
            # Check if the file is explicitly listed (no wildcards) to bypass token check.
            relative_path_str = file_path.relative_to(self.source_path).as_posix()
            is_explicitly_included = self.include_patterns and relative_path_str in self.include_patterns

            if not is_explicitly_included:
                try:
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    token_count = self._count_tokens(content)
                    if token_count > self.max_tokens:
                        print(f"  -> ⚠️  Skipping large file: {relative_path_str} ({token_count:,} tokens)")
                        self.stats["skipped_large"] += 1
                        continue
                except Exception:
                    # Skip files that can't be read
                    continue
            
            included_files.append(file_path)

        if not included_files:
            print("  -> ℹ️ No files matched the criteria for this job. Skipping.")
            return False

        self.output_path.parent.mkdir(exist_ok=True)
        with self.output_path.open("w", encoding="utf-8", errors="replace") as f:
            f.write(f"# Context for: {self.source_path.name}\n\n")
            f.write("## Directory Structure\n\n```")
            f.write(f"{self.source_path.name}/\n")
            f.write(self._build_directory_tree(included_files))
            f.write("\n```\n---\n\n## File Contents\n\n")

            for file_path in included_files:
                relative_path = file_path.relative_to(self.source_path).as_posix()
                f.write(f"--- START OF FILE {relative_path} ---\n")
                try:
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    f.write(content.strip() + "\n")
                    self.stats["tokens"] += self._count_tokens(content)
                    self.stats["files"] += 1
                except Exception as e:
                    f.write(f"[Error reading file: {e}]\n")
                f.write(f"--- END OF FILE {relative_path} ---\n\n\n")
        return True

    def get_stats(self) -> Dict[str, int]:
        return self.stats

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate context files from source repositories based on `config_context.py`.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--root-dir", required=True, help="The root directory where all your cloned repositories are located.")
    parser.add_argument("--output-dir", default=OUTPUT_DIR, help=f"Directory to save the generated files (default: '{OUTPUT_DIR}')")
    parser.add_argument("--output-here", "-oh", action="store_true", help="If set, output to 'generated_context' in the script's directory.")
    # NEW: Command-line argument for max tokens
    parser.add_argument("--max-tokens", type=int, default=16000, help="Maximum tokens for a single file to be included (default: 16000).")
    args = parser.parse_args()

    root_dir = Path(args.root_dir)
    output_dir = Path(args.output_dir)
    if args.output_here:
        output_dir = Path(__file__).parent / "generated_context"

    if not root_dir.is_dir():
        print(f"❌ Error: Root directory not found at '{root_dir}'")
        sys.exit(1)

    print("🚀 Starting context generation...")
    if not TOKEN_COUNTING_AVAILABLE:
        print("   (Note: `tiktoken` not found. Using word count for token stats.)")
    print("-" * 40)

    total_stats = {"tokens": 0, "files": 0, "skipped_large": 0}
    successful_jobs, skipped_jobs = 0, 0

    for i, job in enumerate(PACKAGING_JOBS, 1):
        print(f"▶️ Processing job {i}/{len(PACKAGING_JOBS)}: {job['output_filename']}")
        source_path = root_dir / job["repo_name"] / job.get("sub_path", ".")
        
        if not source_path.exists():
            print(f"  -> ⏭️ Skipping: Source path not found at '{source_path}'")
            skipped_jobs += 1
            continue

        output_path = output_dir / job["output_filename"]
        
        project = Project(
            source_path=source_path,
            output_path=output_path,
            include_patterns=job.get("include"),
            # Pass the max_tokens value to the Project
            max_tokens=args.max_tokens
        )
        
        if project.package():
            stats = project.get_stats()
            token_type = "tokens" if TOKEN_COUNTING_AVAILABLE else "words"
            skipped_info = f", {stats['skipped_large']} large files skipped" if stats['skipped_large'] > 0 else ""
            print(f"  -> ✅ Success! Packaged {stats['files']} files ({stats['tokens']:,} {token_type}{skipped_info}).")
            for key in total_stats:
                total_stats[key] += stats[key]
            successful_jobs += 1
        else:
            skipped_jobs += 1
        
    print("-" * 40)
    print("\n🎉 All jobs complete!")
    print(f"  Summary: {successful_jobs} jobs successful, {skipped_jobs} jobs skipped.")
    if total_stats["files"] > 0:
        token_type = "tokens" if TOKEN_COUNTING_AVAILABLE else "words"
        print(f"  📊 Total output: {total_stats['files']:,} files and {total_stats['tokens']:,} {token_type}.")
    if total_stats["skipped_large"] > 0:
        print(f"  ⏭️  Total large files skipped: {total_stats['skipped_large']:,}")

if __name__ == "__main__":
    main()