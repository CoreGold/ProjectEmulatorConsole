import unittest
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        config = {
            "username": "testuser",
            "hostname": "localhost",
            "vfs_path": "test_vfs.tar",
            "log_path": "test_log.xml",
            "startup_script": "test_startup.sh"
        }
        self.emulator = ShellEmulator(config)

    def test_ls(self):
        # Проверяем, что ls работает корректно
        output = self.emulator.ls()
        self.assertIsInstance(output, list)  # Здесь можно проверить вывод

        def test_cd(self):
            # Проверяем переход в директорию
            initial_dir = self.emulator.current_directory
            self.emulator.cd('/some_dir')
            self.assertNotEqual(initial_dir, self.emulator.current_directory)

        def test_rmdir(self):
            # Проверяем удаление директории
            # Создаем временную директорию для теста
            os.mkdir('temp_dir')
            self.emulator.rmdir('temp_dir')
            self.assertFalse(os.path.exists('temp_dir'))

        def test_tree(self):
            # Проверяем вывод команды tree
            output = self.emulator.tree()
            self.assertIsInstance(output, str)  # Здесь можно проверить вывод

    if __name__ == '__main__':
        unittest.main()