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
    
    def __init__(self, source_path: Path, output_path: Path, include_patterns: List[str] = None, max_file_size: int = 10 * 1024 * 1024, max_tokens_per_file: int = 16000):
        self.source_path = source_path
        self.output_path = output_path
        self.include_patterns = include_patterns or []
        self.max_file_size = max_file_size
        self.max_tokens_per_file = max_tokens_per_file
        self.default_ignores = get_default_ignore_patterns()
        self.total_tokens = 0
        self.total_files = 0
        self.skipped_files = 0
        self.skipped_files_size = 0
        self.skipped_files_tokens = 0
        
    def should_include(self, path: Path) -> bool:
        """Check if a path should be included based on include patterns, ignore patterns, file size, and token count."""
        try:
            relative_path = str(path.relative_to(self.source_path)).replace(os.path.sep, '/')

            # Always apply default ignore patterns
            for pattern in self.default_ignores:
                if fnmatch.fnmatch(relative_path, pattern):
                    return False

            # If include patterns are specified, only include matching files
            if self.include_patterns:
                if path.is_file():
                    for pattern in self.include_patterns:
                        if fnmatch.fnmatch(relative_path, pattern):
                            # Include pattern overrides size and token limits
                            break
                    else:
                        return False
                else:
                    # For directories, include if any child files would be included
                    return self._has_includable_files(path)

            # If no include patterns specified, include everything (except default ignores)
            if path.is_file():
                try:
                    file_size = path.stat().st_size
                    if file_size > self.max_file_size:
                        self.skipped_files += 1
                        self.skipped_files_size += 1
                        return False

                    # Check token count by reading file content
                    try:
                        content = path.read_text(encoding='utf-8', errors='replace')
                        file_tokens = self.count_tokens(content)
                        if file_tokens > self.max_tokens_per_file:
                            self.skipped_files += 1
                            self.skipped_files_tokens += 1
                            return False
                    except Exception:
                        # If we can't read the file, skip it
                        self.skipped_files += 1
                        return False
                except (OSError, IOError):
                    return False
            return True
        except ValueError:
            return False
    
    def _has_includable_files(self, dir_path: Path) -> bool:
        """Check if a directory contains any files that would be included."""
        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    relative_path = str(item.relative_to(self.source_path)).replace(os.path.sep, '/')
                    for pattern in self.include_patterns:
                        if fnmatch.fnmatch(relative_path, pattern):
                            return True
                elif item.is_dir():
                    if self._has_includable_files(item):
                        return True
        except (OSError, IOError):
            pass
        return False
    
    def get_sorted_items(self, path: Path) -> List[Path]:
        """Get sorted list of items in a directory, filtered by include patterns."""
        try:
            items = sorted([p for p in path.iterdir()], key=lambda p: (p.is_file(), p.name.lower()))
            return [item for item in items if self.should_include(item)]
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
        
        # Add include pattern info if specified
        if self.include_patterns:
            output_f.write(f"## Included Files\n\n")
            output_f.write("This context includes only files matching these patterns:\n\n")
            for pattern in self.include_patterns:
                output_f.write(f"- `{pattern}`\n")
            output_f.write("\n")
        
        # Add token statistics if we have them
        if self.total_files > 0:
            token_type = "tokens" if TOKEN_COUNTING_AVAILABLE else "words"
            avg_tokens = self.total_tokens / self.total_files
            output_f.write(f"## Statistics\n\n")
            output_f.write(f"- **Files processed**: {self.total_files}\n")
            if self.skipped_files > 0:
                skip_reasons = []
                if self.skipped_files_size > 0:
                    skip_reasons.append(f"size > {self.max_file_size / (1024*1024):.1f}MB: {self.skipped_files_size}")
                if self.skipped_files_tokens > 0:
                    skip_reasons.append(f"tokens > {self.max_tokens_per_file:,}: {self.skipped_files_tokens}")
                if skip_reasons:
                    output_f.write(f"- **Files skipped** ({', '.join(skip_reasons)}): {self.skipped_files}\n")
            output_f.write(f"- **Total {token_type}**: {self.total_tokens:,}\n")
            output_f.write(f"- **Average {token_type}/file**: {avg_tokens:.0f}\n\n")
        
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
            "skipped_files": self.skipped_files,
            "skipped_files_size": self.skipped_files_size,
            "skipped_files_tokens": self.skipped_files_tokens,
            "avg_tokens_per_file": self.total_tokens / max(self.total_files, 1),
            "token_counting_available": TOKEN_COUNTING_AVAILABLE
        }
    
    def package(self) -> bool:
        """Package the project into a context file."""
        try:
            with self.output_path.open("w", encoding="utf-8") as f:
                self.write_header(f)
                self.write_file_contents(f, self.source_path)
                self.write_footer(f)
            return True
        except Exception as e:
            print(f"❌ Error packaging '{self.source_path}': {e}")
            return False


def create_project(source_path: Path, output_path: Path, include_patterns: List[str] = None, max_file_size: int = 10 * 1024 * 1024, max_tokens_per_file: int = 16000) -> Project:
    """Factory function to create a Project instance."""
    return Project(source_path, output_path, include_patterns, max_file_size, max_tokens_per_file) 