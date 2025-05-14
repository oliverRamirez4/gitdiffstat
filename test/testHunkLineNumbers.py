import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest

class TestHunkLineNumbers(unittest.TestCase):
    def test_single_hunk_line_numbers(self):
        """Test that line numbers are correctly tracked in a single hunk"""
        diff = (
            "diff --git a/example.py b/example.py\n"
            "--- a/example.py\n"
            "+++ b/example.py\n"
            "@@ -10,7 +10,8 @@ def function_a():\n"
            "     print('Hello')\n"
            "-    return None\n"
            "+    # Added a comment\n"
            "+    return True\n"
            "     \n"
        )
        
        result = parse_git_diff(diff)
        
        # Basic assertions
        self.assertEqual(result['total_files_changed'], 1)
        self.assertEqual(result['total_lines_added'], 2)
        self.assertEqual(result['total_lines_removed'], 1)
        
        # File-level assertions
        file_stats = result['files']['example.py']
        self.assertEqual(file_stats['change_type'], 'modified')
        self.assertEqual(file_stats['added'], 2)
        self.assertEqual(file_stats['removed'], 1)
        
        # Hunk-level assertions
        self.assertEqual(len(file_stats['hunks']), 1)
        hunk = file_stats['hunks'][0]
        
        # Check hunk header information
        self.assertEqual(hunk['old_start'], 10)
        self.assertEqual(hunk['old_count'], 7)
        self.assertEqual(hunk['new_start'], 10)
        self.assertEqual(hunk['new_count'], 8)
        
        # Find added/removed lines and verify their line numbers
        added_lines = [change for change in hunk['changes'] if change['type'] == 'add']
        removed_lines = [change for change in hunk['changes'] if change['type'] == 'remove']
        
        self.assertEqual(len(added_lines), 2)
        self.assertEqual(len(removed_lines), 1)
        
        # Check specific line numbers and content
        self.assertEqual(removed_lines[0]['line_number'], 11)
        self.assertEqual(removed_lines[0]['content'], '    return None')
        
        self.assertEqual(added_lines[0]['line_number'], 11)
        self.assertEqual(added_lines[0]['content'], '    # Added a comment')
        
        self.assertEqual(added_lines[1]['line_number'], 12)
        self.assertEqual(added_lines[1]['content'], '    return True')
        
    def test_multiple_hunks_line_numbers(self):
        """Test that line numbers are correctly tracked across multiple hunks"""
        diff = (
            "diff --git a/multi_hunk.py b/multi_hunk.py\n"
            "--- a/multi_hunk.py\n"
            "+++ b/multi_hunk.py\n"
            "@@ -5,6 +5,7 @@ def first_function():\n"
            "     print('First')\n"
            "     x = 1\n"
            "     y = 2\n"
            "+    z = 3\n"
            "     return x + y\n"
            " \n"
            " \n"
            "@@ -27,7 +28,8 @@ def second_function():\n"
            "     a = 10\n"
            "     b = 20\n"
            "-    return a - b\n"
            "+    c = 30\n"
            "+    return a + b + c\n"
            " \n"
            " def third_function():\n"
            "     pass\n"
        )
        
        result = parse_git_diff(diff)
        
        # Basic assertions
        self.assertEqual(result['total_files_changed'], 1)
        self.assertEqual(result['total_lines_added'], 3)
        self.assertEqual(result['total_lines_removed'], 1)
        
        # Verify hunks count
        file_stats = result['files']['multi_hunk.py']
        self.assertEqual(len(file_stats['hunks']), 2)
        
        # Check first hunk
        first_hunk = file_stats['hunks'][0]
        self.assertEqual(first_hunk['old_start'], 5)
        self.assertEqual(first_hunk['old_count'], 6)
        self.assertEqual(first_hunk['new_start'], 5)
        self.assertEqual(first_hunk['new_count'], 7)
        
        # Check first hunk changes
        first_hunk_added = [change for change in first_hunk['changes'] if change['type'] == 'add']
        self.assertEqual(len(first_hunk_added), 1)
        self.assertEqual(first_hunk_added[0]['line_number'], 8)
        self.assertEqual(first_hunk_added[0]['content'], '    z = 3')
        
        # Check second hunk
        second_hunk = file_stats['hunks'][1]
        self.assertEqual(second_hunk['old_start'], 27)
        self.assertEqual(second_hunk['old_count'], 7)
        self.assertEqual(second_hunk['new_start'], 28)
        self.assertEqual(second_hunk['new_count'], 8)
        
        # Check second hunk changes
        second_hunk_added = [change for change in second_hunk['changes'] if change['type'] == 'add']
        second_hunk_removed = [change for change in second_hunk['changes'] if change['type'] == 'remove']
        
        self.assertEqual(len(second_hunk_added), 2)
        self.assertEqual(len(second_hunk_removed), 1)
        
        self.assertEqual(second_hunk_removed[0]['line_number'], 29)
        self.assertEqual(second_hunk_removed[0]['content'], '    return a - b')
        
        self.assertEqual(second_hunk_added[0]['line_number'], 30)
        self.assertEqual(second_hunk_added[0]['content'], '    c = 30')
        
        self.assertEqual(second_hunk_added[1]['line_number'], 31)
        self.assertEqual(second_hunk_added[1]['content'], '    return a + b + c')
        
    def test_added_file_line_numbers(self):
        """Test line numbers in a newly added file"""
        diff = (
            "diff --git a/new_file.py b/new_file.py\n"
            "new file mode 100644\n"
            "--- /dev/null\n"
            "+++ b/new_file.py\n"
            "@@ -0,0 +1,4 @@\n"
            "+def new_function():\n"
            "+    print('This is a new file')\n"
            "+    x = 42\n"
            "+    return x\n"
        )
        
        result = parse_git_diff(diff)
        
        # Check file type
        file_stats = result['files']['new_file.py']
        self.assertEqual(file_stats['change_type'], 'added')
        
        # Check hunk
        hunk = file_stats['hunks'][0]
        self.assertEqual(hunk['old_start'], 0)
        self.assertEqual(hunk['old_count'], 0)
        self.assertEqual(hunk['new_start'], 1)
        self.assertEqual(hunk['new_count'], 4)
        
        # Check added lines
        added_lines = [change for change in hunk['changes'] if change['type'] == 'add']
        self.assertEqual(len(added_lines), 4)
        
        # Check line numbers start at 1 and increase sequentially
        for i, change in enumerate(added_lines):
            self.assertEqual(change['line_number'], i + 1)
        
        # Check content of specific lines
        self.assertEqual(added_lines[0]['content'], 'def new_function():')
        self.assertEqual(added_lines[3]['content'], '    return x')
        
    def test_deleted_file_line_numbers(self):
        """Test line numbers in a deleted file"""
        diff = (
            "diff --git a/deleted_file.py b/deleted_file.py\n"
            "deleted file mode 100644\n"
            "--- a/deleted_file.py\n"
            "+++ /dev/null\n"
            "@@ -1,3 +0,0 @@\n"
            "-def to_be_deleted():\n"
            "-    print('This function will be deleted')\n"
            "-    return None\n"
        )
        
        result = parse_git_diff(diff)
        
        # Check file type
        file_stats = result['files']['deleted_file.py']
        self.assertEqual(file_stats['change_type'], 'deleted')
        
        # Check hunk
        hunk = file_stats['hunks'][0]
        self.assertEqual(hunk['old_start'], 1)
        self.assertEqual(hunk['old_count'], 3)
        self.assertEqual(hunk['new_start'], 0)
        self.assertEqual(hunk['new_count'], 0)
        
        # Check removed lines
        removed_lines = [change for change in hunk['changes'] if change['type'] == 'remove']
        self.assertEqual(len(removed_lines), 3)
        
        # Check line numbers start at 1 and increase sequentially
        for i, change in enumerate(removed_lines):
            self.assertEqual(change['line_number'], i + 1)
        
        # Check content of specific lines
        self.assertEqual(removed_lines[0]['content'], 'def to_be_deleted():')
        self.assertEqual(removed_lines[2]['content'], '    return None')
        
    def test_complex_diff_with_context_lines(self):
        """Test line numbers in a complex diff with context lines"""
        diff = (
            "diff --git a/complex.py b/complex.py\n"
            "--- a/complex.py\n"
            "+++ b/complex.py\n"
            "@@ -15,7 +15,9 @@ class ExampleClass:\n"
            "     def method_one(self):\n"
            "         value = 100\n"
            "         print('Processing')\n"
            "-        return value * 2\n"
            "+        # Calculate result with multiplier\n"
            "+        multiplier = 2\n"
            "+        return value * multiplier\n"
            "     \n"
            "     def method_two(self):\n"
            "         return 'Hello'\n"
        )
        
        result = parse_git_diff(diff)
        
        # Check hunk
        file_stats = result['files']['complex.py']
        hunk = file_stats['hunks'][0]
        
        # Check context lines as well as added/removed
        context_lines = [change for change in hunk['changes'] if change['type'] == 'context']
        added_lines = [change for change in hunk['changes'] if change['type'] == 'add']
        removed_lines = [change for change in hunk['changes'] if change['type'] == 'remove']
        
        # Verify we have context lines
        self.assertTrue(len(context_lines) > 0)
        
        # Check that context lines have both old and new line numbers
        for context_line in context_lines:
            self.assertIn('old_line_number', context_line)
            self.assertIn('new_line_number', context_line)
            
        # Check first context line numbers
        self.assertEqual(context_lines[0]['old_line_number'], 15)
        self.assertEqual(context_lines[0]['new_line_number'], 15)
        
        # Check that the line positions make sense
        self.assertEqual(removed_lines[0]['line_number'], 18)
        self.assertEqual(added_lines[0]['line_number'], 18)
        self.assertEqual(added_lines[1]['line_number'], 19)
        self.assertEqual(added_lines[2]['line_number'], 20)
        
        # Verify the final context lines have the correct line numbers after changes
        if len(context_lines) > 3:
            # The blank line and following context lines should have shifted
            self.assertEqual(context_lines[3]['old_line_number'], 19)
            self.assertEqual(context_lines[3]['new_line_number'], 21)


if __name__ == '__main__':
    unittest.main()