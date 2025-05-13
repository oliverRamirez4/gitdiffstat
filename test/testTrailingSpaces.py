import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest

class TestTrailingSpaces(unittest.TestCase):
    def test_filename_with_trailing_spaces(self):
        diff = (
            "diff --git a/spaced_file.py  b/spaced_file.py  \n"
            "--- a/spaced_file.py  \n"
            "+++ b/spaced_file.py  \n"
            "@@ -1 +1 @@\n"
            "-print('spacey')\n"
            "+print('clean')\n"
        )
        result = parse_git_diff(diff)
        self.assertIn('spaced_file.py', result['files'])
        self.assertNotIn('spaced_file.py  ', result['files'])
        file_data = result['files']['spaced_file.py']
        self.assertEqual(file_data['change_type'], 'modified')
        self.assertEqual(file_data['added'], 1)
        self.assertEqual(file_data['removed'], 1)

    def test_file_added_with_trailing_chars(self):
        diff = (
            "diff --git a/new_file.py\t b/new_file.py\t\n"
            "new file mode 100644\n"
            "--- /dev/null\n"
            "+++ b/new_file.py\t\n"
            "@@ -0,0 +1 @@\n"
            "+print('added')\n"
        )
        result = parse_git_diff(diff)
        self.assertIn('new_file.py', result['files'])
        self.assertEqual(result['files']['new_file.py']['change_type'], 'added')
        self.assertEqual(result['files']['new_file.py']['added'], 1)


if __name__ == '__main__':
    unittest.main()