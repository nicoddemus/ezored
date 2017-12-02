import os
import shutil
import subprocess
from subprocess import PIPE

from ezored.models.logger import Logger


class FileUtil(object):
    @staticmethod
    def create_dir(dir_path):
        Logger.d('Create a new dir: {0}'.format(dir_path))

        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

    @staticmethod
    def remove_dir(dir_path):
        Logger.d('Remove dir: {0}'.format(dir_path))

        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def remove_file(filename):
        Logger.d('Remove file: {0}'.format(filename))

        if os.path.isfile(filename):
            os.remove(filename)

    @staticmethod
    def write_to_file(dir_path, filename, content):
        Logger.d('Create file {0} in dir {1} with {2} bytes'.format(filename, dir_path, len(content)))

        full_file_path = os.path.join(dir_path, filename)
        FileUtil.remove_file(full_file_path)
        FileUtil.create_dir(dir_path)

        with open(full_file_path, 'w') as f:
            f.write(content)
            f.close()

    @staticmethod
    def get_current_dir():
        return os.getcwd()

    @staticmethod
    def run(args, cwd, env):
        proc = subprocess.Popen(
            args,
            env=env,
            cwd=cwd,
            stdout=PIPE,
            stderr=PIPE
        )

        out, err = proc.communicate()
        exitcode = proc.returncode

        return exitcode, err, out

    @staticmethod
    def copy_files_from_list(copy_file_list):
        if copy_file_list:
            for copy_file in copy_file_list:
                shutil.copyfile(copy_file.from_path, copy_file.to_path)
