# GitDiffStat

A Python package for parsing Git diff output and extracting meaningful statistics from it.

## Installation

You can install the package via pip:

```bash
pip install gitdiffstats_oliverRamirez
```

Or install directly from the repository:

```bash
pip install git+https://github.com/oliverRamirez4/gitdiffstat.git
```

## Usage

```python
from gitdiffstats.diffstats import parse_git_diff

# Example git diff output
diff_text = """
diff --git a/example.py b/example.py
--- a/example.py
+++ b/example.py
@@ -1,3 +1,4 @@
 def hello():
-    print("Hello")
+    print("Hello World")
+    return True
 """

# Parse the diff and get statistics
result = parse_git_diff(diff_text)

print(f"Files changed: {result['total_files_changed']}")
print(f"Lines added: {result['total_lines_added']}")
print(f"Lines removed: {result['total_lines_removed']}")

# Access file-specific data
for filename, stats in result['files'].items():
    print(f"\nFile: {filename}")
    print(f"  Change type: {stats['change_type']}")
    print(f"  Lines added: {stats['added']}")
    print(f"  Lines removed: {stats['removed']}")
```

## Features

- Parse Git diff output into structured data
- Extract per-file statistics:
  - Number of lines added
  - Number of lines removed
  - Type of change (added, deleted, modified)
- Calculate overall statistics:
  - Total files changed
  - Total lines added
  - Total lines removed
- Handles various Git diff formats:
  - Added files
  - Deleted files
  - Modified files
  - Files with special characters or whitespace in names

## API Reference

### parse_git_diff(diff_text: str) -> Dict

Parses a Git diff string and returns a dictionary with statistics.

**Parameters:**
- `diff_text` (str): A string containing the Git diff output.

**Returns:**
- A dictionary with:
  - `total_files_changed`: Total number of files modified in the diff
  - `total_lines_added`: Total number of lines added across all files
  - `total_lines_removed`: Total number of lines removed across all files
  - `files`: Dictionary with per-file statistics:
    - Key: File path
    - Value: Dictionary with:
      - `added`: Number of lines added
      - `removed`: Number of lines removed
      - `change_type`: Type of change ('added', 'deleted', or 'modified')

## Development

### Setup

```bash
git clone https://github.com/oliverRamirez4/gitdiffstat.git
cd gitdiffstat
pip install -e .
```

### Running Tests

```bash
python -m unittest discover -s test
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.