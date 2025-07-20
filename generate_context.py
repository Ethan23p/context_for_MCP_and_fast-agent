#!/usr/bin/env python3
"""
Context generation script for MCP and Fast-Agent repositories.
Automatically loads configuration and packages projects into context files.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Any

# Import our modular components
from config_context import get_packaging_jobs, get_output_dir
from context_generator.project_packager import create_project


class ContextGenerator:
    """Main class for generating context files from repositories."""
    
    def __init__(self, root_dir: Path, output_dir: Path):
        self.root_dir = root_dir
        self.output_dir = output_dir
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
            print(f"⚠️  Warning: Source path not found, skipping job.")
            print(f"   Path: '{source_path}'")
            print(f"   Job: {job_info['repo_name']}/{job_info['sub_path']}")
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
            ignore_patterns=job["ignore"]
        )
        
        success = project.package()
        
        # Show token statistics
        if success:
            stats = project.get_token_stats()
            token_type = "tokens" if stats["token_counting_available"] else "words"
            print(f"   📊 {stats['total_files']} files, {stats['total_tokens']:,} {token_type}")
            if stats['total_files'] > 0:
                print(f"   📈 Average: {stats['avg_tokens_per_file']:.0f} {token_type}/file")
        
        return success
    
    def run(self) -> bool:
        """Run the complete context generation process."""
        print(f"🚀 Starting context generation...")
        print(f"   Root directory: {self.root_dir}")
        print(f"   Output directory: {self.output_dir}")
        print(f"   Jobs to process: {len(self.packaging_jobs)}")
        
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
        total_tokens = 0
        total_files = 0
        
        for i, job in enumerate(self.packaging_jobs, 1):
            print(f"📋 Processing job {i}/{len(self.packaging_jobs)}: {job['repo_name']}/{job['sub_path']}")
            
            if self.process_job(job):
                successful_jobs += 1
                # Get stats from the last processed project
                from context_generator.project_packager import create_project
                repo_path = self.root_dir / job["repo_name"]
                source_path = repo_path / job["sub_path"]
                output_path = self.output_dir / job["output_filename"]
                project = create_project(source_path, output_path, job["ignore"])
                stats = project.get_token_stats()
                total_tokens += stats["total_tokens"]
                total_files += stats["total_files"]
            else:
                failed_jobs += 1
            
            print("-" * 50)
        
        # Summary
        print(f"\n📊 Generation Summary:")
        print(f"   ✅ Successful: {successful_jobs}")
        print(f"   ❌ Failed: {failed_jobs}")
        print(f"   📁 Total: {len(self.packaging_jobs)}")
        
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
  python generate_context.py --root-dir ./repositories
        """
    )
    parser.add_argument(
        "--root-dir", 
        required=True, 
        help="Root directory containing the cloned repositories"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    root_dir = Path(args.root_dir)
    if not validate_root_directory(root_dir):
        sys.exit(1)
    
    output_dir = Path(get_output_dir())
    
    # Create and run the generator
    generator = ContextGenerator(root_dir, output_dir)
    success = generator.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()