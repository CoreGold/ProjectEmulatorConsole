import os
import tarfile
import json
import xml.etree.ElementTree as ET
from datetime import datetime

class ShellEmulator:
    def __init__(self, config):
        self.username = config['username']
        self.hostname = config['hostname']
        self.vfs_path = config['vfs_path']
        self.log_path = config['log_path']

        self.startup_script = config['startup_script']
        self.current_directory = "vfs"
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
            tar.extractall()

    def log_creation(self):
        root = ET.Element("log")
        tree = ET.ElementTree(root)
        tree.write(self.log_path)
    def log_action(self, action):
        tree = ET.parse(self.log_path)
        root = tree.getroot()
        time = ET.SubElement(root, "time")
        entry = ET.SubElement(time, "entry")
        date = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        time.text = date
        entry.text = f"{self.username} executed: {action}"
        tree = ET.ElementTree(root)
        tree.write(self.log_path)


    def ls(self):
        files = os.listdir(self.current_directory)
        print("\n".join(files))
        self.log_action("ls")

    def cd(self, path):
        path2 = self.current_directory + '/' + path
        if os.path.isdir(path2):
            self.current_directory = path2
            self.log_action(f"cd {path}")
        elif os.path.isdir(path):
            self.current_directory = path
            self.log_action(f"cd {path}")
        else:
            print(f"Директория '{path}' не найдена.")

    def exit(self):
        self.log_action("exit")
        print("Выход...")
        exit(0)

    def rmdir(self, path):
        path = self.current_directory + '/' + path
        if os.path.exists(path) and not os.listdir(path):
            os.rmdir(path)
            print(f"Директория '{path}' успешно удалена.")
        elif os.path.exists(path) and os.listdir(path):
            print(f"Директория '{path}' не пуста.")
        else:
            print(f"Директория '{path}' не найдена.")

    def tree(self):
        test = os.walk(self.current_directory);
        for root, dirs, files in os.walk(self.current_directory):
            level = root.replace(self.current_directory, '').count(os.sep)
            space = ' ' * 4 * (level)
            print(f"{space}{os.path.basename(root)}/")
            space2 = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{space2}{f}")
        self.log_action("tree")

    def run(self):
        self.log_creation()
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
                print(f"Команда '{cmd_name}' не найдена.")

if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)
    emulator = ShellEmulator(config)
    emulator.run()