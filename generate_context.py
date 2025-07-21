#!/usr/bin/env python3
"""
Context generation script for MCP and Fast-Agent repositories.
Automatically loads configuration and packages projects into context files.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any
import os

# Import our modular components
from config_context import get_packaging_jobs, get_output_dir
from context_generator.project_packager import create_project


class ContextGenerator:
    """Main class for generating context files from repositories."""
    
    def __init__(self, root_dir: Path, output_dir: Path, max_file_size: int = 10 * 1024 * 1024, max_tokens_per_file: int = 16000):
        self.root_dir = root_dir
        self.output_dir = output_dir
        self.max_file_size = max_file_size
        self.max_tokens_per_file = max_tokens_per_file
        self.packaging_jobs = get_packaging_jobs()
        
    def setup_output_directory(self) -> bool:
        """Create the output directory if it doesn't exist."""
        try:
            self.output_dir.mkdir(exist_ok=True)
            print(f"✅ Output directory ready: '{self.output_dir}'")
            return True
        except Exception as e:
            print(f"❌ Error creating output directory: {e}")
            return False
    
    def validate_source_path(self, source_path: Path, job_info: Dict[str, Any]) -> bool:
        """Validate that a source path exists and is accessible."""
        if not source_path.exists():
            # Skip silently for missing repos - this is expected behavior
            return False
        return True
    
    def process_job(self, job: Dict[str, Any]) -> bool:
        """Process a single packaging job."""
        repo_path = self.root_dir / job["repo_name"]
        source_path = repo_path / job["sub_path"]
        output_path = self.output_dir / job["output_filename"]
        
        if not self.validate_source_path(source_path, job):
            return False
        
        project = create_project(
            source_path=source_path,
            output_path=output_path,
            include_patterns=job.get("include", []),
            max_file_size=self.max_file_size,
            max_tokens_per_file=self.max_tokens_per_file
        )
        
        success = project.package()
        
        # Show token statistics
        if success:
            stats = project.get_token_stats()
            token_type = "tokens" if stats["token_counting_available"] else "words"
            print(f"   📊 {stats['total_files']} files, {stats['total_tokens']:,} {token_type}")
            if stats['skipped_files'] > 0:
                print(f"   ⏭️  Skipped {stats['skipped_files']} files (too large)")
            if stats['total_files'] > 0:
                print(f"   📈 Average: {stats['avg_tokens_per_file']:.0f} {token_type}/file")
        
        return success
    
    def run(self) -> bool:
        """Run the complete context generation process."""
        print(f"🚀 Starting context generation...")
        print(f"   Root directory: {self.root_dir}")
        print(f"   Output directory: {self.output_dir}")
        print(f"   Max file size: {self.max_file_size / (1024*1024):.1f}MB")
        print(f"   Max tokens per file: {self.max_tokens_per_file:,}")
        
        # Check which repos are available
        available_repos = set()
        for job in self.packaging_jobs:
            repo_path = self.root_dir / job["repo_name"]
            if repo_path.exists():
                available_repos.add(job["repo_name"])

        # Find all files in root_dir not covered by config jobs (recursively)
        config_job_paths = set()
        for job in self.packaging_jobs:
            config_job_paths.add((job["repo_name"], job["sub_path"]))
        unmatched_files = []
        # --- Begin fix for generic case ---
        has_files_at_root = any(x.is_file() for x in self.root_dir.iterdir())
        if has_files_at_root:
            # root_dir is a leaf directory, not a parent of repos
            for root, dirs, files in os.walk(self.root_dir):
                for filename in files:
                    abs_file = os.path.join(root, filename)
                    rel_file = os.path.relpath(abs_file, self.root_dir).replace("\\", "/")
                    unmatched_files.append(rel_file)
        else:
            # original logic for parent-of-repos
            for repo_dir in self.root_dir.iterdir():
                if not repo_dir.is_dir():
                    continue
                repo_name = repo_dir.name
                for root, dirs, files in os.walk(repo_dir):
                    for filename in files:
                        abs_file = os.path.join(root, filename)
                        rel_file = os.path.relpath(abs_file, repo_dir).replace("\\", "/")
                        # Check if this file is covered by any config job
                        covered = False
                        for job in self.packaging_jobs:
                            if job["repo_name"] == repo_name:
                                if job["sub_path"] == "." or rel_file.startswith(job["sub_path"]):
                                    if not job["include"] or rel_file in job["include"]:
                                        covered = True
                                        break
                        if not covered:
                            unmatched_files.append(f"{repo_name}/{rel_file}")
        if unmatched_files:
            self.packaging_jobs.append({
                "repo_name": "",  # Use empty string to indicate root_dir itself
                "sub_path": ".",
                "output_filename": f"{self.root_dir.name}_misc_context.md",
                "include": unmatched_files
            })
        # --- End fix for generic case ---

        print()
        
        # Check token counting availability
        from context_generator.project_packager import TOKEN_COUNTING_AVAILABLE
        if TOKEN_COUNTING_AVAILABLE:
            print(f"   🧮 Token counting: Available (tiktoken)")
        else:
            print(f"   ⚠️  Token counting: Word count only (install tiktoken for accurate counting)")
        print()
        
        if not self.setup_output_directory():
            return False
        
        successful_jobs = 0
        failed_jobs = 0
        skipped_jobs = 0
        total_tokens = 0
        total_files = 0
        
        for i, job in enumerate(self.packaging_jobs, 1):
            # --- Begin fix for generic case job path resolution ---
            if job["repo_name"]:
                repo_path = self.root_dir / job["repo_name"]
            else:
                repo_path = self.root_dir
            source_path = repo_path / job["sub_path"]
            # --- End fix for generic case job path resolution ---
            if not source_path.exists():
                skipped_jobs += 1
                continue
            job_label = f"[{i}/{len(self.packaging_jobs)}] {job['output_filename']}"
            from context_generator.project_packager import create_project
            output_path = self.output_dir / job["output_filename"]
            project = create_project(source_path, output_path, job.get("include", []), self.max_file_size, self.max_tokens_per_file)
            success = project.package()
            stats = project.get_token_stats()
            if success:
                successful_jobs += 1
                total_tokens += stats["total_tokens"]
                total_files += stats["total_files"]
                skipped_str = f", {stats['skipped_files']} skipped" if stats['skipped_files'] > 0 else ""
                print(f"{job_label} ({stats['total_files']} files, {stats['total_tokens']} tokens{skipped_str})")
            else:
                failed_jobs += 1
                print(f"{job_label} (FAILED)")
        # Concise summary
        print(f"\nSummary: {successful_jobs} successful, {failed_jobs} failed, {skipped_jobs} skipped, {len(self.packaging_jobs)} total jobs")
        
        if total_files > 0:
            from context_generator.project_packager import TOKEN_COUNTING_AVAILABLE
            token_type = "tokens" if TOKEN_COUNTING_AVAILABLE else "words"
            print(f"   📄 Files processed: {total_files:,}")
            print(f"   🧮 Total {token_type}: {total_tokens:,}")
            print(f"   📈 Average {token_type}/file: {total_tokens / total_files:.0f}")
        
        if failed_jobs == 0:
            print(f"\n🎉 All jobs completed successfully!")
            return True
        else:
            print(f"\n⚠️  {failed_jobs} job(s) failed. Check the output above for details.")
            return False


def validate_root_directory(root_dir: Path) -> bool:
    """Validate that the root directory exists and is accessible."""
    if not root_dir.exists():
        print(f"❌ Error: Root directory not found at '{root_dir}'")
        return False
    
    if not root_dir.is_dir():
        print(f"❌ Error: '{root_dir}' is not a directory")
        return False
    
    return True


def main():
    """Main entry point for the context generation script."""
    parser = argparse.ArgumentParser(
        description="Generate context files from source repositories.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_context.py --root-dir /path/to/repos
  python generate_context.py --root-dir ./repositories --max-file-size 5242880
  python generate_context.py --root-dir ./repositories --max-tokens-per-file 50000
        """
    )
    parser.add_argument(
        "--root-dir", 
        required=True, 
        help="Root directory containing the cloned repositories"
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=10 * 1024 * 1024,  # 10MB default
        help="Maximum file size in bytes to include (default: 10MB)"
    )
    parser.add_argument(
        "--max-tokens-per-file",
        type=int,
        default=16000,  # 16K tokens default
        help="Maximum tokens per file to include (default: 16000)"
    )
    parser.add_argument(
        "--output-here", "-oh",
        action="store_true",
        help="If set, output context files to the 'generated_context' folder in the directory of this script. Otherwise, use the default output directory from config_context.py."
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    root_dir = Path(args.root_dir)
    if not validate_root_directory(root_dir):
        sys.exit(1)
    
    if args.output_here:
        output_dir = Path(__file__).parent / "generated_context"
    else:
        output_dir = Path(get_output_dir())
    
    # Create and run the generator
    generator = ContextGenerator(root_dir, output_dir, args.max_file_size, args.max_tokens_per_file)
    success = generator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()