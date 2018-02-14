import unittest
from unittest.mock import patch
import sys


# Mocking "import winreg", for non-Windows systems
sys.modules["winreg"] = __import__("tests.stub_winreg")


import find_windows_signtool
import winreg
import os


class Test_get_winsdk_bin_pathes(unittest.TestCase):

    def test_fake(self):
        pass

if __name__ == "__main__":
    unittest.main()

