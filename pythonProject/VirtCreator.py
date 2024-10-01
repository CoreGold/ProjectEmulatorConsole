import tarfile
import os

def VFSCreation():
    os.makedirs('vfs/dir1', exist_ok=True)
    os.makedirs('vfs/dir2', exist_ok=True)
    with open('vfs/file1.txt', 'w') as f:
        f.write("Hello, World!")

    with open('vfs/file2.txt', 'w') as f:
        f.write("This is file 2.")

    with open('vfs/dir1/file3.txt', 'w') as f:
        f.write("File in dir1.")

    with tarfile.open('virtual_filesystem.tar', 'w') as tar:
        tar.add('vfs', arcname=os.path.basename('vfs'))

    os.remove('vfs/file1.txt')
    os.remove('vfs/file2.txt')
    os.remove('vfs/dir1/file3.txt')
    os.rmdir('vfs/dir1')
    os.rmdir('vfs/dir2')
    os.rmdir('vfs')
VFSCreation()