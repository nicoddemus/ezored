import os
from subprocess import check_output, STDOUT

from ezored.models.logger import Logger
from ezored.models.repository import Repository
from ezored.models.util.file_util import FileUtil
from ezored.models.util.type_util import TypeUtil


class GitUtil(object):
    @staticmethod
    def download(rep_path, rep_type=None, rep_version=None, dest=None):
        """
        Clone the repository specified by path, type and version to dest directory.
        """
        Logger.d('New git clone request')

        GitUtil.check_if_git_is_installed()

        # if repository type or version is empty, we will use "branch:master"
        if TypeUtil.is_empty(rep_type) or TypeUtil.is_empty(rep_version):
            rep_type = Repository.GIT_TYPE_BRANCH
            rep_version = 'master'

        # clone the repository
        args = [
            'git',
            'clone',
            '--depth',
            '1',
            rep_path,
            dest,
        ]

        FileUtil.run(args, FileUtil.get_current_dir(), None)

        # change to the desired repository version
        if rep_type == Repository.GIT_TYPE_BRANCH:
            args = [
                'git',
                'checkout',
                rep_version,
            ]
        elif rep_type == Repository.GIT_TYPE_COMMIT:
            args = [
                'git',
                'reset',
                '--hard',
                rep_version,
            ]
        elif rep_type == Repository.GIT_TYPE_TAG:
            args = [
                'git',
                'checkout',
                rep_version,
            ]
        else:
            raise Exception('Git repository type is invalid')

        FileUtil.run(args, dest, None)

    @staticmethod
    def check_if_git_is_installed():
        try:
            check_output(['git', '--version'], stderr=STDOUT)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                raise Exception('Required tool was not installed (git)')
            else:
                raise
