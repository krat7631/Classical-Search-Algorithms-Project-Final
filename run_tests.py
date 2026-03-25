"""Simple test runner. Run with: python3 run_tests.py"""

import sys
import unittest

sys.path.insert(0, ".")

loader = unittest.TestLoader()
suite = loader.loadTestsFromName("tests.test_algorithms")
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
