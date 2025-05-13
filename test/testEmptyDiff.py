import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest

class TestEmptyDiff(unittest.TestCase):

    def test_empty_diff(self):
        diff = ""
        result = parse_git_diff(diff)
        self.assertEqual(result['total_files_changed'], 0)
        self.assertEqual(result['total_lines_added'], 0)
        self.assertEqual(result['total_lines_removed'], 0)
        self.assertEqual(result['files'], {})

if __name__ == '__main__':
    unittest.main()