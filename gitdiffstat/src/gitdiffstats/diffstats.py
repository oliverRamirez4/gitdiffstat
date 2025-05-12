import re
from typing import Dict

def parse_git_diff(diff_text: str) -> Dict:
    """
    Parse a given git diff string to extract overall statistics and per-file statistics.
    
    Args:
        diff_text (str): A string containing the git diff.
    
    Returns:
        Dict: A dictionary with total stats and per-file stats.
    """
   #convert diff_text to string if it is None
    if diff_text is None:
        diff_text = ""

    lines = diff_text.strip().splitlines()

    total_added = 0
    total_removed = 0
    files_stats = {}

    current_file = None
    change_type = "modified"

    # Patterns
    diff_git_pattern = re.compile(r'^diff --git a/(.*?) b/(.*)$')
    new_file_pattern = re.compile(r'^new file mode')
    deleted_file_pattern = re.compile(r'^deleted file mode')
    plus_file_pattern = re.compile(r'^\+\+\+ b/(.*)$')
    minus_file_pattern = re.compile(r'^--- (.*)$')

    for line in lines:
        # Start of a new file diff
        if line.startswith("diff --git"):
            match = diff_git_pattern.match(line)
            if match:
                a_path, b_path = match.groups()
                current_file = b_path.strip()  # we use the destination path
                change_type = "modified"  # default assumption
                files_stats[current_file] = {'added': 0, 'removed': 0, 'change_type': change_type}
            continue

        # Detect added or deleted files
        if new_file_pattern.match(line):
            change_type = "added"
            if current_file:
                files_stats[current_file]['change_type'] = change_type
            continue

        if deleted_file_pattern.match(line):
            change_type = "deleted"
            if current_file:
                files_stats[current_file]['change_type'] = change_type
            continue

        # Handle snippets with only ---/+++ headers
        if plus_file_pattern.match(line):
            plus_match = plus_file_pattern.match(line)
            current_file = plus_match.group(1).strip()
            if current_file not in files_stats:
                files_stats[current_file] = {'added': 0, 'removed': 0, 'change_type': change_type}
            continue

        if minus_file_pattern.match(line):
            minus_match = minus_file_pattern.match(line)
            if minus_match.group(1) == '/dev/null':
                change_type = "added"
                if current_file:
                    files_stats[current_file]['change_type'] = change_type
            continue

        # Hunk header (skip)
        if line.startswith("@@"):
            continue

        # Count added lines
        if line.startswith("+") and not line.startswith("+++"):
            total_added += 1
            if current_file:
                files_stats[current_file]['added'] += 1

        # Count removed lines
        elif line.startswith("-") and not line.startswith("---"):
            total_removed += 1
            if current_file:
                files_stats[current_file]['removed'] += 1

    return {
        'total_files_changed': len(files_stats),
        'total_lines_added': total_added,
        'total_lines_removed': total_removed,
        'files': files_stats
    }