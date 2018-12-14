import os
import re
from subprocess import check_output, STDOUT

from ezored.models.constants import Constants
from ezored.models.logger import Logger
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
        if TypeUtil.is_empty(rep_version):
            rep_type = Constants.GIT_TYPE_BRANCH
            rep_version = 'master'

        # clone the repository
        args = [
            'git',
            'clone',
            rep_path,
            dest,
        ]

        exitcode, stderr, stdout = FileUtil.run(
            args=args,
            cwd=FileUtil.get_current_dir(),
            env=dict(os.environ)
        )

        if exitcode == 0:
            Logger.i('Repository cloned with success:')
        else:
            if stdout:
                Logger.i('Repository clone output:')
                Logger.clean(stdout)

            if stderr:
                Logger.i('Error output while clone repository')
                Logger.clean(stderr)

        # change to the desired repository version
        if rep_type == Constants.GIT_TYPE_BRANCH:
            Logger.i('Changing repository to branch {0}...'.format(rep_version))

            args = [
                'git',
                'checkout',
                rep_version,
            ]
        elif rep_type == Constants.GIT_TYPE_COMMIT:
            Logger.i('Changing repository to commit {0}...'.format(rep_version))

            args = [
                'git',
                'checkout',
                '-b',
                rep_version,
                rep_version,
            ]
        elif rep_type == Constants.GIT_TYPE_TAG:
            Logger.i('Changing repository to tag {0}...'.format(rep_version))

            args = [
                'git',
                'checkout',
                'tags/{0}'.format(rep_version),
                '-b',
                rep_version,
            ]
        else:
            raise Exception('Git repository type is invalid')

        exitcode, stderr, stdout = FileUtil.run(args, dest, None)

        if exitcode == 0:
            Logger.i('Repository version changed with success')
        else:
            if stdout:
                Logger.i('Repository version change output:')
                Logger.clean(stdout)

            if stderr:
                Logger.i('Error output while change repository version:')
                Logger.clean(stderr)

    @staticmethod
    def check_if_git_is_installed():
        try:
            check_output(['git', '--version'], stderr=STDOUT)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                raise Exception('Required tool was not installed (git)')
            else:
                raise

    @staticmethod
    def get_repository_name(rep_path):
        p = re.compile('([^/]+)\.git$', re.IGNORECASE)
        data_list = p.findall(rep_path)
        rep_name = data_list[0] if len(data_list) == 1 else None
        return rep_name

    @staticmethod
    def get_current_downloaded_repository_version(path):
        if path is None:
            return None

        if not os.path.isdir(path):
            return None

        args = [
            'git',
            'rev-parse',
            '--abbrev-ref',
            'HEAD',
        ]

        exitcode, stderr, stdout = FileUtil.run(args, path, None)

        if exitcode == 0:
            return os.path.basename(stdout).strip().decode()
        else:
            if stdout:
                Logger.i('Get downloaded repository version output:')
                Logger.clean(stdout)

            if stderr:
                Logger.i('Error output while get downloaded repository version:')
                Logger.clean(stderr)
