import unittest
import os
import tempfile
import shutil

# Importiere die Funktionen, die du testen möchtest.
from assistant_core.modules.coding.code_tracker import run_flake8_check, collect_file_stats
# Falls get_diff_files implementiert ist, importiere es:
try:
    from assistant_core.modules.coding.code_tracker import get_diff_files
except ImportError:
    get_diff_files = None

class TestLintChecker(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Wenn flake8 nicht installiert ist, überspringe diese Tests.
        if shutil.which("flake8") is None:
            raise unittest.SkipTest("flake8 ist nicht installiert.")

    def test_run_flake8_check_valid_file(self):
        # Erstelle eine temporäre Datei mit validem Python-Code.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write("print('Hello world')\n")
            tmp_name = tmp.name
        try:
            issues = run_flake8_check(tmp_name)
            # Für gültigen Code erwarten wir keine Linting-Fehler.
            self.assertEqual(issues, [])
        finally:
            os.remove(tmp_name)

    def test_run_flake8_check_invalid_file(self):
        # Erstelle eine temporäre Datei mit absichtlich fehlerhaftem Code (z. B. unnötige Leerzeichen).
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write("print('Hello world')   \n")  # Trailing spaces
            tmp_name = tmp.name
        try:
            issues = run_flake8_check(tmp_name)
            # Bei fehlerhaftem Code erwarten wir mindestens einen Linting-Fehler.
            self.assertTrue(len(issues) > 0)
        finally:
            os.remove(tmp_name)

class TestCollectFileStats(unittest.TestCase):
    def test_collect_file_stats_single_file(self):
        # Erstelle ein temporäres Verzeichnis mit einer Python-Datei.
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_path = os.path.join(tmpdirname, "test.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("print('Hello')\nprint('World')\n")
            stats = collect_file_stats(start_dir=tmpdirname)
            # Es sollte genau eine Datei in den Statistiken enthalten sein.
            self.assertEqual(len(stats), 1)
            stat_entry = stats[0]
            self.assertIn("test.py", stat_entry["file"])
            self.assertEqual(stat_entry["line_count"], 2)
            self.assertGreater(stat_entry["size_bytes"], 0)
            # Der Eintrag "lint_issues" wird entweder leer oder gefüllt sein – das Testen des genauen Inhalts kann variieren.

# Optional: Falls du get_diff_files implementiert hast, füge einen Test dafür hinzu.
if get_diff_files is not None:
    class TestDiffFiles(unittest.TestCase):
        def test_get_diff_files_returns_list(self):
            # Dieser Test prüft, ob get_diff_files eine Liste zurückgibt.
            diff = get_diff_files("HEAD~1..HEAD")
            self.assertIsInstance(diff, list)

if __name__ == '__main__':
    unittest.main()