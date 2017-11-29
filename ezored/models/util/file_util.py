import os
import shutil


class FileUtil(object):
    @staticmethod
    def create_dir(dir_path):
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def remove_dir(dir_path):
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def remove_file(filename):
        if os.path.isfile(filename):
            os.remove(filename)

    @staticmethod
    def write_to_file(dir_path, filename, content):
        full_file_path = os.path.join(dir_path, filename)
        FileUtil.remove_file(full_file_path)
        FileUtil.create_dir(dir_path)

        with open(full_file_path, 'w') as f:
            f.write(content)
            f.close()
