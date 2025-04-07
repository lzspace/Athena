import unittest
import tempfile
import os
from assistant_core.modules.coding import code_tracker

class TestCodeTracker(unittest.TestCase):
    def test_list_py_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # Erstelle testweise eine Python-Datei
            test_file = os.path.join(temp_dir, "test.py")
            with open(test_file, "w") as f:
                f.write("print('Hallo Welt')")
            file_map = code_tracker.list_py_files(start_dir=temp_dir)
            self.assertIn("test.py", [info["name"] for info in file_map.values()])

if __name__ == '__main__':
    unittest.main()