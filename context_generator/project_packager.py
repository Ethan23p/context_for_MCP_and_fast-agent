"""
Project packaging functionality.
Contains the Project class and related utilities for generating context files.
"""

import os
import fnmatch
from pathlib import Path
from typing import List, Set, TextIO, Optional
from config_context import get_default_ignore_patterns

# Optional token counting
try:
    import tiktoken
    TOKEN_COUNTING_AVAILABLE = True
except ImportError:
    TOKEN_COUNTING_AVAILABLE = False


class Project:
    """Represents a project to be packaged into a context file."""
    
    def __init__(self, source_path: Path, output_path: Path, ignore_patterns: List[str] = None):
        self.source_path = source_path
        self.output_path = output_path
        self.ignore_patterns = ignore_patterns or []
        self.default_ignores = get_default_ignore_patterns()
        self.all_ignores = self.default_ignores.union(set(self.ignore_patterns))
        self.total_tokens = 0
        self.total_files = 0
        
    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored based on ignore patterns."""
        try:
            relative_path = str(path.relative_to(self.source_path)).replace(os.path.sep, '/')
            for pattern in self.all_ignores:
                if fnmatch.fnmatch(relative_path, pattern):
                    return True
        except ValueError:
            return True
        return False
    
    def get_sorted_items(self, path: Path) -> List[Path]:
        """Get sorted list of items in a directory, filtered by ignore patterns."""
        try:
            items = sorted([p for p in path.iterdir()], key=lambda p: (p.is_file(), p.name.lower()))
            return [item for item in items if not self.should_ignore(item)]
        except FileNotFoundError:
            return []
    
    def build_tree(self, current_path: Path, prefix: str = "") -> str:
        """Build a tree representation of the directory structure."""
        tree_lines = []
        valid_items = self.get_sorted_items(current_path)
        
        for i, item in enumerate(valid_items):
            is_last = (i == len(valid_items) - 1)
            connector = "└── " if is_last else "├── "
            icon = "📄" if item.is_file() else "📁"
            tree_lines.append(f"{prefix}{connector}{icon} {item.name}")
            
            if item.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                tree_lines.extend(self.build_tree(item, new_prefix).splitlines())
                
        return "\n".join(tree_lines)
    
    def write_file_contents(self, output_f: TextIO, current_path: Path):
        """Write file contents to the output file."""
        valid_items = self.get_sorted_items(current_path)
        
        for item in valid_items:
            if item.is_file():
                relative_path_str = str(item.relative_to(self.source_path)).replace(os.path.sep, '/')
                output_f.write(f"--- START OF FILE {relative_path_str} ---\n")
                try:
                    content = item.read_text(encoding='utf-8', errors='replace')
                    output_f.write(f"{content}\n")
                    
                    # Count tokens for this file
                    file_tokens = self.count_tokens(content)
                    self.total_tokens += file_tokens
                    self.total_files += 1
                    
                except Exception as e:
                    output_f.write(f"[Error reading file: {e}]\n")
                output_f.write(f"--- END OF FILE {relative_path_str} ---\n\n\n")
            elif item.is_dir():
                self.write_file_contents(output_f, item)
    
    def write_header(self, output_f: TextIO):
        """Write the header section of the output file."""
        output_f.write(f"# Project: {self.source_path.name}\n\n")
        output_f.write("## Directory Structure\n\n```\n")
        tree_str = f"📁 {self.source_path.name}\n" + self.build_tree(self.source_path)
        output_f.write(tree_str)
        output_f.write("\n```\n\n------------------------------------------------------------\n\n## File Contents\n\n")
    
    def write_footer(self, output_f: TextIO):
        """Write the footer section of the output file."""
        output_f.write("\n--- PROJECT PACKAGING COMPLETE ---")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken if available, otherwise word count."""
        if TOKEN_COUNTING_AVAILABLE:
            try:
                encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
                return len(encoding.encode(text))
            except Exception:
                # Fallback to word count if tiktoken fails
                return len(text.split())
        else:
            # Fallback to word count
            return len(text.split())
    
    def get_token_stats(self) -> dict:
        """Get token statistics for the project."""
        return {
            "total_tokens": self.total_tokens,
            "total_files": self.total_files,
            "avg_tokens_per_file": self.total_tokens / max(self.total_files, 1),
            "token_counting_available": TOKEN_COUNTING_AVAILABLE
        }
    
    def package(self) -> bool:
        """Package the project into a context file."""
        print(f"📦 Packaging '{self.source_path}' into '{self.output_path}'...")
        
        try:
            with self.output_path.open("w", encoding="utf-8") as f:
                self.write_header(f)
                self.write_file_contents(f, self.source_path)
                self.write_footer(f)
            
            print(f"✅ Successfully packaged '{self.output_path}'.")
            return True
            
        except Exception as e:
            print(f"❌ Error packaging '{self.source_path}': {e}")
            return False


def create_project(source_path: Path, output_path: Path, ignore_patterns: List[str] = None) -> Project:
    """Factory function to create a Project instance."""
    return Project(source_path, output_path, ignore_patterns) 