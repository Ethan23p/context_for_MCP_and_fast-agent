# Filesystem Server Summary
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
