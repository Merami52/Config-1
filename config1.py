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

    def list_files(self):
        try:
            return os.listdir(self.current_directory)
        except FileNotFoundError:
            return []

    def change_directory(self, path):
        if path == "/":
            self.current_directory = "/tmp/virtual_fs"
            return

        target_path = os.path.join(self.current_directory, path)
        if os.path.exists(target_path) and os.path.isdir(target_path):
            self.current_directory = target_path
        else:
            print(f"cd: no such file or directory: {path}")

    def execute_command(self, command):
        parts = command.strip().split()
        if not parts:
            return
        cmd, *args = parts

        if cmd == "ls":
            print("\n".join(self.list_files()))
        elif cmd == "cd":
            if args:
                self.change_directory(args[0])
            else:
                print("cd: missing operand")
        elif cmd == "exit":
            exit()
        else:
            print(f"{cmd}: command not found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True, help='User name for prompt')
    parser.add_argument('--host', required=True, help='Host name for prompt')
    parser.add_argument('--tar', required=True, help='Path to the tar archive of the virtual filesystem')
    args = parser.parse_args()

    shell_emulator = ShellEmulator(args.user, args.host, args.tar)

    while True:
        command = input(f"{args.user}@{args.host}:{shell_emulator.current_directory}$ ")
        shell_emulator.execute_command(command)
