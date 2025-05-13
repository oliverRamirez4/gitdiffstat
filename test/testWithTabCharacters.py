import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest

class TestTabCharacters(unittest.TestCase):
    def test_filename_with_tab_characters(self):
        diff = (
            "diff --git a/file_with_tab.py\t b/file_with_tab.py\t\n"
            "--- a/file_with_tab.py\t\n"
            "+++ b/file_with_tab.py\t\n"
            "@@ -1 +1 @@\n"
            "-print('old')\n"
            "+print('new')\n"
        )
        result = parse_git_diff(diff)
        self.assertIn('file_with_tab.py', result['files'])
        self.assertNotIn('file_with_tab.py\t', result['files'])
        file_data = result['files']['file_with_tab.py']
        self.assertEqual(file_data['change_type'], 'modified')
        self.assertEqual(file_data['added'], 1)
        self.assertEqual(file_data['removed'], 1)

if __name__ == '__main__':
    unittest.main()