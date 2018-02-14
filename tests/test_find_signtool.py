import unittest
from unittest.mock import patch
import sys


# Mocking "import winreg", for non-Windows systems
sys.modules["winreg"] = __import__("tests.stub_winreg")


import find_windows_signtool
from conans.errors import ConanException
import os


class Test_find_windows_signtool(unittest.TestCase):

    @patch("os.path.isfile")
    @patch("find_windows_signtool.get_winsdk_bin_pathes")
    def test_normal_x86(self, mock_get_winsdk_bin_pathes, mock_os_path_isfile):
        mock_get_winsdk_bin_pathes.return_value = ["C:\\WinSDK10\\bin", "C:\\WinSDK8\\bin"]
        mock_os_path_isfile.return_value = True

        result = find_windows_signtool.find_signtool("x86")

        normal_result = os.path.join("C:\\WinSDK10\\bin", "x86", "signtool.exe")
        self.assertEqual(result, normal_result)
        mock_os_path_isfile.assert_called_once_with(normal_result)

    @patch("os.path.isfile")
    @patch("find_windows_signtool.get_winsdk_bin_pathes")
    def test_normal_x86_64(self, mock_get_winsdk_bin_pathes, mock_os_path_isfile):
        mock_get_winsdk_bin_pathes.return_value = ["C:\\WinSDK10\\bin", "C:\\WinSDK8\\bin"]
        mock_os_path_isfile.return_value = True

        result = find_windows_signtool.find_signtool("x86_64")

        normal_result = os.path.join("C:\\WinSDK10\\bin", "x64", "signtool.exe")
        self.assertEqual(result, normal_result)
        mock_os_path_isfile.assert_called_once_with(normal_result)

    @patch("os.path.isfile")
    @patch("find_windows_signtool.get_winsdk_bin_pathes")
    def test_skip_if_not_exists(self, mock_get_winsdk_bin_pathes, mock_os_path_isfile):
        mock_get_winsdk_bin_pathes.return_value = ["C:\\WinSDK10\\bin", "C:\\WinSDK8\\bin"]
        mock_os_path_isfile.side_effect = [False, True]

        result = find_windows_signtool.find_signtool("x86_64")

        normal_result = os.path.join("C:\\WinSDK8\\bin", "x64", "signtool.exe")
        self.assertEqual(result, normal_result)
        calls = [
            unittest.mock.call(os.path.join("C:\\WinSDK10\\bin", "x64", "signtool.exe")),
            unittest.mock.call(normal_result)
        ]
        mock_os_path_isfile.assert_has_calls(calls)

    @patch("os.path.isfile")
    @patch("find_windows_signtool.get_winsdk_bin_pathes")
    def test_bad_sdk(self, mock_get_winsdk_bin_pathes, mock_os_path_isfile):
        mock_get_winsdk_bin_pathes.return_value = ["C:\\BadSDK\\bin"]
        mock_os_path_isfile.return_value = False

        with self.assertRaises(ConanException):
            find_windows_signtool.find_signtool("x86_64")
        mock_os_path_isfile.assert_called_once_with(os.path.join("C:\\BadSDK\\bin", "x64", "signtool.exe"))

    @patch("os.path.isfile")
    @patch("find_windows_signtool.get_winsdk_bin_pathes")
    def test_not_found_sdk(self, mock_get_winsdk_bin_pathes, mock_os_path_isfile):
        mock_get_winsdk_bin_pathes.return_value = []

        with self.assertRaises(ConanException):
            find_windows_signtool.find_signtool("x86_64")
        mock_os_path_isfile.assert_not_called()


if __name__ == "__main__":
    unittest.main()

