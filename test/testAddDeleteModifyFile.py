import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))
from gitdiffstats.diffstats import parse_git_diff
import unittest
class TestAddDeleteModifyFile(unittest.TestCase):

    def test_added_file(self):
        diff = (
            "diff --git a/new_file.py b/new_file.py\n"
            "new file mode 100644\n"
            "--- /dev/null\n"
            "+++ b/new_file.py\n"
            "@@ -0,0 +1,3 @@\n"
            "+print('Hello')\n"
            "+print('World')\n"
            "+print('!')\n"
        )
        result = parse_git_diff(diff)
        self.assertEqual(result['total_lines_added'], 3)
        self.assertEqual(result['total_lines_removed'], 0)
        self.assertEqual(result['total_files_changed'], 1)
        file_data = result['files']['new_file.py']
        self.assertEqual(file_data['change_type'], 'added')

    def test_deleted_file(self):
        diff = (
            "diff --git a/old_file.py b/old_file.py\n"
            "deleted file mode 100644\n"
            "--- a/old_file.py\n"
            "+++ /dev/null\n"
            "@@ -1,2 +0,0 @@\n"
            "-print('Goodbye')\n"
            "-print('World')\n"
        )
        result = parse_git_diff(diff)
        self.assertEqual(result['total_lines_added'], 0)
        self.assertEqual(result['total_lines_removed'], 2)
        self.assertEqual(result['total_files_changed'], 1)
        file_data = result['files']['old_file.py']
        self.assertEqual(file_data['change_type'], 'deleted')

    def test_modified_file(self):
        diff = (
            "diff --git a/app/main.py b/app/main.py\n"
            "--- a/app/main.py\n"
            "+++ b/app/main.py\n"
            "@@ -10,7 +10,8 @@ def run():\n"
            "-    return True\n"
            "+    log.info('running')\n"
            "+    return True\n"
        )
        result = parse_git_diff(diff)
        self.assertEqual(result['total_lines_added'], 2)
        self.assertEqual(result['total_lines_removed'], 1)
        self.assertEqual(result['total_files_changed'], 1)
        file_data = result['files']['app/main.py']
        self.assertEqual(file_data['change_type'], 'modified')


if __name__ == '__main__':
    unittest.main()