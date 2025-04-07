import unittest
from assistant_core.modules.coding import generator

class TestCodingModule(unittest.TestCase):
    def test_generate_script(self):
        result = generator.generate_script("example", {})
        self.assertIn("example", result)

if __name__ == "__main__":
    unittest.main()
