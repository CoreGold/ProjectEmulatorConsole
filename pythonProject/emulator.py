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
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'exit': self.exit,
            'rmdir': self.rmdir,
            'tree': self.tree
        }

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
        tree.write(self.log_path)

    def ls(self):
        with tarfile.open(self.vfs_path) as tar:
            for member in tar.getmembers():
                if member.name.startswith(self.current_directory):
                    print(member.name)
        self.log_action("ls")

    def cd(self, path):
        # Проверка на существование директории


        with tarfile.open(self.vfs_path) as tar:
            if any(member.name == (self.current_directory + '/' + path) for member in tar.getmembers() if
                   member.isdir()):
                self.current_directory = self.current_directory + '/' + path
                self.log_action(f"cd {path}")
            elif any(member.name == path for member in tar.getmembers() if member.isdir()):
                self.current_directory = path
                self.log_action(f"cd {path}")
            else:
                print(f"Директория '{path}' не найдена.")

    def exit(self):
        self.log_action("exit")
        print("Выход...")
        exit(0)

    def rmdir(self, path):
        # Удаление директории (фактически просто логическое действие, так как мы не можем изменять tar файл)
        print(f"Удаление директории '{os.path.join(self.current_directory, path)}' невозможно (Нельзя изменять tar файл).")

    def tree(self):
        with tarfile.open(self.vfs_path) as tar:
            for member in sorted(tar.getmembers(), key=lambda m: m.name):
                if member.name.startswith(self.current_directory):
                    level = member.name.count('/')
                    space = ' ' * 4 * level
                    print(f"{space}{os.path.basename(member.name)}{'/' if member.isdir() else ''}")
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
                    self.commands[cmd_name](*args)
                else:
                    self.commands[cmd_name]()
            else:
                print(f"Команда '{cmd_name}' не найдена.")


if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)
    emulator = ShellEmulator(config)
    emulator.run()
