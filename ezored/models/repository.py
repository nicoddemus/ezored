import os
import re
import tarfile

import yaml
from ezored.models.constants import Constants
from ezored.models.logger import Logger
from ezored.models.util.download_util import DownloadUtil
from ezored.models.util.file_util import FileUtil
from slugify import slugify


class Repository(object):
    TYPE_LOCAL = 'local'
    TYPE_GITHUB = 'github'

    GIT_TYPE_BRANCH = 'b'
    GIT_TYPE_TAG = 't'
    GIT_TYPE_COMMIT = 'c'

    rep_type = ''
    rep_name = ''
    rep_version = ''

    def __init__(self, rep_type, rep_name, rep_version):
        self.rep_type = rep_type
        self.rep_name = rep_name
        self.rep_version = rep_version

    def get_name(self):
        if self.rep_type == Repository.TYPE_LOCAL:
            rep_path, rep_file = os.path.split(self.rep_name)
            return rep_file
        else:
            return self.rep_name

    def get_download_url(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            git_data_name, _, git_data_version = self.get_git_data()
            return 'https://github.com/{0}/archive/{1}.{2}'.format(
                git_data_name,
                git_data_version,
                Constants.GITHUB_DOWNLOAD_EXTENSION
            )
        else:
            return ''

    def get_download_filename(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            git_data_name, _, git_data_version = self.get_git_data()
            git_data_name_list = str(git_data_name).split('/')

            return '{0}.{1}'.format(
                slugify('{0}-{1}'.format(
                    git_data_name_list[1],
                    git_data_version)
                ),
                Constants.GITHUB_DOWNLOAD_EXTENSION
            )
        elif self.rep_type == Repository.TYPE_LOCAL:
            _, filename = os.path.split(self.rep_name)
            return slugify(filename)
        else:
            return ''

    def download(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            self.download_from_github()

    def get_git_data(self):
        # it will return a tuple of 3 elements with this pattern
        # 1 = repository name
        # 2 = git type [b = branch, t = tag, c = commit]
        # 3 = version [tag name, branch name or version name]

        p = re.compile('(.*\w)(:)(.*\w)', re.IGNORECASE)
        git_data_list = p.findall(self.rep_version)
        git_data = git_data_list[0] if len(git_data_list) == 1 else None

        if not git_data or len(git_data) != 3:
            if self.rep_version != '':
                return self.rep_name, Repository.GIT_TYPE_TAG, self.rep_version
            else:
                return self.rep_name, Repository.GIT_TYPE_BRANCH, 'master'

        return self.rep_name, git_data[0], git_data[2]

    def get_temp_working_dir(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            return os.path.join(Constants.TEMPORARY_DIR, self.get_dir_name())
        elif self.rep_type == Repository.TYPE_LOCAL:
            return self.rep_name
        else:
            return ''

    def get_dir_name(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            git_data_name, _, git_data_version = self.get_git_data()
            git_data_name_list = str(git_data_name).split('/')
            return '{0}-{1}'.format(slugify(git_data_name_list[1]), slugify(git_data_version))
        elif self.rep_type == Repository.TYPE_LOCAL:
            _, filename = os.path.split(self.rep_name)
            return slugify(filename)
        else:
            return ''

    def download_from_github(self):
        # download
        Logger.i('Downloading repository: {0}...'.format(self.get_name()))

        download_url = self.get_download_url()
        download_filename = self.get_download_filename()
        download_dest_dir = Constants.TEMPORARY_DIR
        download_dest_path = os.path.join(Constants.TEMPORARY_DIR, download_filename)
        unpacked_dir = self.get_temp_working_dir()
        unpack_dir = Constants.TEMPORARY_DIR
        force_download = False

        _, git_data_type, git_data_version = self.get_git_data()

        if git_data_type == Repository.GIT_TYPE_BRANCH:
            force_download = True

        # skip if exists
        if not force_download and os.path.isfile(download_dest_path):
            Logger.i('Repository already downloaded: {0}'.format(self.get_name()))
        else:
            FileUtil.remove_file(download_dest_path)

            DownloadUtil.download_file(download_url, download_dest_dir, download_filename)

            # check if file was downloaded
            if os.path.isfile(download_dest_path):
                Logger.i('Repository downloaded: {0}'.format(self.get_name()))
            else:
                Logger.f('Problems when download repository: {0}'.format(self.get_name()))

        # unpack
        Logger.i('Unpacking repository: {0}...'.format(self.get_name()))

        if not force_download and os.path.isdir(unpacked_dir):
            Logger.i('Repository already unpacked: {0}...'.format(self.get_name()))
        else:
            FileUtil.remove_dir(unpacked_dir)

            # untar file
            FileUtil.create_dir(unpack_dir)

            tar = tarfile.open(download_dest_path)
            tar.extractall(path=unpack_dir)
            tar.close()

            if os.path.isdir(unpacked_dir):
                Logger.i('Repository unpacked: {0}'.format(self.get_name()))
            else:
                Logger.f('Problems when unpack repository: {0}'.format(self.get_name()))

    def build(self):
        Logger.i('Building repository: {0}...'.format(self.get_name()))

        vendor_file_data = self.load_vendor_file_data()

        if 'vendor' in vendor_file_data:
            vendor_data = vendor_file_data['vendor']

            if 'build' in vendor_data:
                vendor_data_build = vendor_data['build']

                env_data = dict(os.environ)
                env_data['EZORED_PROJECT_ROOT'] = FileUtil.get_current_dir()

                exitcode, stderr, stdout = FileUtil.run(vendor_data_build, self.get_temp_working_dir(), env_data)

                if exitcode == 0:
                    Logger.i('Build finished for repository: {0}'.format(self.get_name()))
                else:
                    if stdout:
                        Logger.i('Build output for repository: {0}'.format(self.get_name()))
                        Logger.clean(stdout)

                    if stderr:
                        Logger.i('Error output while build repository: {0}'.format(self.get_name()))
                        Logger.clean(stderr)

                    Logger.f('Failed to build repository: {0}'.format(self.get_name()))

    def load_vendor_file_data(self):
        Logger.d('Loading vendor file...')

        vendor_dir = self.get_temp_working_dir()
        vendor_file_path = os.path.join(vendor_dir, Constants.VENDOR_FILE)

        try:
            with open(vendor_file_path, 'r') as stream:
                return yaml.load(stream)
        except IOError as exc:
            Logger.f('Error while read vendor file: {0}'.format(exc))

    @staticmethod
    def from_dict(dict_data):
        repository = Repository(
            rep_type=dict_data['type'] if 'type' in dict_data else '',
            rep_name=dict_data['name'] if 'name' in dict_data else '',
            rep_version=dict_data['version'] if 'version' in dict_data else '',
        )

        return repository
