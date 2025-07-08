# Git Server Summary
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
