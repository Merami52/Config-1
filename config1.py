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
            tar.extractall("/tmp/virtual_fs")
        self.current_directory = "/tmp/virtual_fs"

    def list_files(self):
        try:
            return os.listdir(self.current_directory)
        except FileNotFoundError:
            return []

    def change_directory(self, path):
        target_path = os.path.join(self.current_directory, path)
        if os.path.exists(target_path) and os.path.isdir(target_path):
            self.current_directory = target_path
        else:
            print(f"cd: no such file or directory: {path}")

    def print_head(self, filename, lines=1):
        path = os.path.join(self.current_directory, filename)
        try:
            with open(path, 'r') as file:
                for _ in range(lines):
                    line = file.readline()
                    if not line:
                        break
                    print(line, end='')
                    print('\n')
        except FileNotFoundError:
            print(f"head: cannot open '{filename}' for reading: No such file or directory")

    def reverse_cat(self, filename):
        path = os.path.join(self.current_directory, filename)
        try:
            with open(path, 'r') as file:
                lines = file.readlines()
                for line in reversed(lines):
                    print(line, end='')
        except FileNotFoundError:
            print(f"tac: {filename}: No such file or directory")

    def touch_file(self, filename):
        path = os.path.join(self.current_directory, filename)
        with open(path, 'a'):
            os.utime(path, None)

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
        elif cmd == "head":
            lines = int(args[1]) if len(args) > 1 else 10
            self.print_head(args[0], lines)
        elif cmd == "tac":
            self.reverse_cat(args[0])
        elif cmd == "touch":
            self.touch_file(args[0])
        else:
            print(f"{cmd}: command not found")

    def run_shell(self):
        while True:
            command = input(f"{self.user}@{self.host}:{self.current_directory}$ ")
            self.execute_command(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', required=True, help='User name for prompt')
    parser.add_argument('--host', required=True, help='Host name for prompt')
    parser.add_argument('--tar', required=True, help='Path to the tar archive of the virtual filesystem')
    args = parser.parse_args()

    shell_emulator = ShellEmulator(args.user, args.host, args.tar)
    shell_emulator.run_shell()
