import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest

class TestMultipleFiles(unittest.TestCase):
    def test_multiple_files(self):
            diff = (
                "diff --git a/added.py b/added.py\n"
                "new file mode 100644\n"
                "--- /dev/null\n"
                "+++ b/added.py\n"
                "@@ -0,0 +1 @@\n"
                "+print('new')\n"
                "diff --git a/deleted.py b/deleted.py\n"
                "deleted file mode 100644\n"
                "--- a/deleted.py\n"
                "+++ /dev/null\n"
                "@@ -1 +0,0 @@\n"
                "-print('bye')\n"
                "diff --git a/modified.py b/modified.py\n"
                "--- a/modified.py\n"
                "+++ b/modified.py\n"
                "@@ -1 +1,2 @@\n"
                "-print('old')\n"
                "+print('new')\n"
                "+print('again')\n"
            )
            result = parse_git_diff(diff)
            self.assertEqual(result['total_files_changed'], 3)
            self.assertEqual(result['total_lines_added'], 3)
            self.assertEqual(result['total_lines_removed'], 2)

            self.assertEqual(result['files']['added.py']['change_type'], 'added')
            self.assertEqual(result['files']['deleted.py']['change_type'], 'deleted')
            self.assertEqual(result['files']['modified.py']['change_type'], 'modified')

if __name__ == '__main__':
    unittest.main()