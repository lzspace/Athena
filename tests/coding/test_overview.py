import unittest
import os
from assistant_core.modules.coding import overview_generator

class TestOverviewGenerator(unittest.TestCase):
    def test_generate_script_overview(self):
        # Nutze einen temporären Dateinamen für den Test
        test_md = "test_SCRIPTS.md"
        # Sicherstellen, dass die Datei leer ist
        if os.path.exists(test_md):
            os.remove(test_md)
        # Generiere den Overview
        overview_generator.generate_script_overview(
            script_path="scripts/example.py",
            description="Ein Beispielskript",
            used_libs=["numpy", "pandas"],
            tests=["tests/coding/test_example.py"]
        )
        with open("SCRIPTS.md", "r") as f:
            content = f.read()
        self.assertIn("scripts/example.py", content)
        self.assertIn("numpy, pandas", content)
        # Aufräumen
        os.remove("SCRIPTS.md")

if __name__ == '__main__':
    unittest.main()