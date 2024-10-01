import os
import xml.etree.ElementTree as ET
import pytest
import json
from emulator import ShellEmulator
from VirtCreator import VFSCreation

@pytest.fixture
def emulator():
    VFSCreation()
    with open('config.json') as f:
        config = json.load(f)
    return ShellEmulator(config)

def test_log_creation(emulator):
    emulator.log_creation()
    assert os.path.exists(emulator.log_path)

def test_log_action(emulator):
    emulator.log_creation()
    emulator.log_action("test_action")

    tree = ET.parse(emulator.log_path)
    root = tree.getroot()
    entries = root.findall('time/entry')
    assert len(entries) == 1
    assert "user executed: test_action" in entries[0].text

def test_ls(emulator, capsys):
    emulator.ls()
    captured = capsys.readouterr()
    assert captured.out == 'vfs\nvfs/dir1\nvfs/dir1/file3.txt\nvfs/dir2\nvfs/file1.txt\nvfs/file2.txt\n'

def test_cd_change_directory(emulator):
    emulator.cd('dir1')
    assert emulator.current_directory == 'vfs/dir1'

def test_cd_invalid_directory(emulator, capsys):
    emulator.cd('test_dir')
    captured = capsys.readouterr()
    assert captured.out == "Директория 'test_dir' не найдена.\n"

def test_tree(emulator, capsys):
    emulator.tree()
    captured = capsys.readouterr()
    assert captured.out == "vfs/\n    dir1/\n        file3.txt\n    dir2/\n    file1.txt\n    file2.txt\n"

def test_rmdir(emulator, capsys):
    emulator.rmdir('dir2')
    emulator.ls()
    captured = capsys.readouterr()
    assert 'dir2' not in captured.out

def test_exit(emulator, capsys):
    with pytest.raises(SystemExit):
        emulator.exit()
    captured = capsys.readouterr()
    assert captured.out == "Выход...\n"

if __name__ == "__main__":
    pytest.main()
