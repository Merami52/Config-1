import os
import tarfile
import argparse

class ShellEmulator:
    def __init__(self, user, host, tar_path):
        self.user = user
        self.host = host
        self.current_directory = "/"
        self.filesystem = {}
        self.load_filesystem(tar_path)

    def load_filesystem(self, tar_path):
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall("/tmp/virtual_fs")  # Временно извлеките для одного сеанса
        self.current_directory = "/tmp/virtual_fs"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True, help='User name for prompt')
    parser.add_argument('--host', required=True, help='Host name for prompt')
    parser.add_argument('--tar', required=True, help='Path to the tar archive of the virtual filesystem')
    args = parser.parse_args()

    shell_emulator = ShellEmulator(args.user, args.host, args.tar)
