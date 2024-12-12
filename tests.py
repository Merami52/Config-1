import unittest
import os
from unittest import mock
from config1 import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(ShellEmulator, "load_filesystem"):
            self.emulator = ShellEmulator('user', 'host', 'tar_path')

    @mock.patch('os.listdir', return_value=['file1', 'file2'])
    def test_list_files(self, mock_list):
        self.assertEqual(self.emulator.list_files(), ['file1', 'file2'])

    @mock.patch('os.path')
    @mock.patch('os.listdir', return_value=['file1', 'file2'])
    def test_change_directory_valid(self, mock_list, mock_path):
        mock_path.join.return_value = '/new_path'
        mock_path.exists.return_value = True
        mock_path.isfile.return_value = False
        self.emulator.change_directory('new_path')
        self.assertEqual(self.emulator.current_directory, '/new_path')

    @mock.patch('os.path')
    def test_change_directory_invalid(self, mock_path):
        mock_path.join.return_value = '/invalid_path'
        mock_path.exists.return_value = False
        self.emulator.change_directory('invalid_path')
        self.assertEqual(self.emulator.current_directory, '/')

    @mock.patch('os.path')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='line1\nline2\nline3\n')
    def test_print_head(self, mock_file, mock_path):
        mock_path.join.return_value = 'file'
        self.emulator.print_head('file', 2)
        mock_file.assert_called_once_with('file', 'r')

    @mock.patch('os.path')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data='line1\nline2\nline3\n')
    def test_reverse_cat(self, mock_file, mock_path):
        mock_path.join.return_value = 'file'
        self.emulator.reverse_cat('file')
        mock_file.assert_called_once_with('file', 'r')

    @mock.patch('os.path')
    @mock.patch('os.utime')
    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_touch_file(self, mock_file, mock_utime, mock_path):
        mock_path.join.return_value = 'new_file'
        self.emulator.touch_file('new_file')
        mock_file.assert_called_once_with('new_file', 'a')
        mock_utime.assert_called_once_with('new_file', None)

if __name__ == '__main__':
    unittest.main()
