import os
import tarfile
import json
import xml.etree.ElementTree as ET

class ShellEmulator:
    def __init__(self, config):
        self.username = config['username']
        self.hostname = config['hostname']
        self.vfs_path = config['vfs_path']
        self.log_path = config['log_path']
        self.startup_script = config['startup_script']
        self.current_directory = "/"
        self.load_vfs()
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit,
            'rmdir': self.rmdir,
            'tree': self.tree
        }

    def load_vfs(self):
        with tarfile.open(self.vfs_path) as tar:
            tar.extractall(path='.')

    def log_action(self, action):
        root = ET.Element("log")
        entry = ET.SubElement(root, "entry")
        entry.text = f"{self.username} executed: {action}"
        tree = ET.ElementTree(root)
        tree.write(self.log_path)

    def ls(self):
        files = os.listdir(self.current_directory)
        print("\n".join(files))
        self.log_action("ls")

    def cd(self, path):
        if os.path.isdir(path):
            self.current_directory = path
            self.log_action(f"cd {path}")
        else:
            print(f"{path}: No such file or directory")

    def exit(self):
        self.log_action("exit")
        print("Exiting...")
        exit(0)

    def rmdir(self, path):
        try:
            os.rmdir(path)
            self.log_action(f"rmdir {path}")
        except Exception as e:
            print(e)

    def tree(self):
        for root, dirs, files in os.walk(self.current_directory):
            level = root.replace(self.current_directory, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")
        self.log_action("tree")

    def run(self):
        while True:
            command = input(f"{self.username}@{self.hostname}:{self.current_directory}$ ")
            parts = command.split()
            cmd_name = parts[0]
            args = parts[1:]

            if cmd_name in self.commands:
                if args:
                    self.commands[cmd_name](" ".join(args))
                else:
                    self.commands[cmd_name]()
            else:
                print(f"{cmd_name}: command not found")

if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)
    emulator = ShellEmulator(config)
    emulator.run()