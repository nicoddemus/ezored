import importlib
import os
import re
import tarfile

import sys
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

    def __init__(self, rep_type, rep_path, rep_version):
        self.rep_type = rep_type
        self.rep_path = rep_path
        self.rep_version = rep_version

    def get_name(self):
        if self.rep_type == Repository.TYPE_LOCAL:
            rep_path, rep_file = os.path.split(self.rep_path)
            return slugify(rep_file)
        else:
            return slugify(self.rep_path)

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
                '{0}-{1}'.format(git_data_name_list[1], git_data_version), Constants.GITHUB_DOWNLOAD_EXTENSION
            )
        elif self.rep_type == Repository.TYPE_LOCAL:
            _, filename = os.path.split(self.rep_path)
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
                return self.rep_path, Repository.GIT_TYPE_TAG, self.rep_version
            else:
                return self.rep_path, Repository.GIT_TYPE_BRANCH, 'master'

        return self.rep_path, git_data[0], git_data[2]

    def get_temp_dir(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            return os.path.join(FileUtil.get_current_dir(), Constants.TEMP_DIR, self.get_dir_name())
        elif self.rep_type == Repository.TYPE_LOCAL:
            return self.rep_path
        else:
            return ''

    def get_vendor_dir(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            return os.path.join(FileUtil.get_current_dir(), Constants.VENDOR_DIR, self.get_dir_name())
        elif self.rep_type == Repository.TYPE_LOCAL:
            return os.path.join(FileUtil.get_current_dir(), Constants.VENDOR_DIR, self.get_dir_name())
        else:
            return ''

    def get_source_dir(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            return os.path.join(FileUtil.get_current_dir(), Constants.VENDOR_DIR, self.get_dir_name())
        elif self.rep_type == Repository.TYPE_LOCAL:
            return os.path.join(self.rep_path, 'build')
        else:
            return ''

    def get_dir_name(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            git_data_name, _, git_data_version = self.get_git_data()
            git_data_name_list = str(git_data_name).split('/')
            return '{0}-{1}'.format(git_data_name_list[1], git_data_version)
        elif self.rep_type == Repository.TYPE_LOCAL:
            _, filename = os.path.split(self.rep_path)
            return slugify(filename)
        else:
            return ''

    def download_from_github(self):
        # download
        Logger.i('Downloading repository: {0}...'.format(self.get_name()))

        download_url = self.get_download_url()
        download_filename = self.get_download_filename()
        download_dest_dir = Constants.TEMP_DIR
        download_dest_path = os.path.join(Constants.TEMP_DIR, download_filename)
        unpacked_dir = self.get_temp_dir()
        unpack_dir = Constants.TEMP_DIR
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

    def build(self, project, process_data):
        Logger.i('Building repository: {0}...'.format(self.get_name()))

        sys_path = list(sys.path)
        original_cwd = os.getcwd()

        try:
            sys.path.insert(0, self.get_temp_dir())

            target_module = importlib.import_module(Constants.VENDOR_MODULE_NAME)
            do_build = getattr(target_module, 'do_build')

            do_build(
                params={
                    'project': project,
                    'process_data': process_data,
                }
            )

            del sys.modules[Constants.VENDOR_MODULE_NAME]
            del target_module
            del do_build

            Logger.i('Build finished for repository: {0}'.format(self.get_name()))
        except Exception as e:
            Logger.e("Error while call 'do_build' on repository {0}: {1}".format(self.get_name(), e.message))
            raise

        sys.path = sys_path
        os.chdir(original_cwd)

    def load_target_data_file(self):
        Logger.d('Loading target data file...')

        vendor_dir = self.get_vendor_dir()
        target_file_path = os.path.join(vendor_dir, Constants.TARGET_DATA_FILE)

        try:
            with open(target_file_path, 'r') as stream:
                return yaml.load(stream)
        except IOError as exc:
            Logger.f('Error while read target file: {0}'.format(exc))

    def prepare_from_process_data(self, process_data):
        if process_data:
            self.rep_path = process_data.parse_text(self.rep_path)

    @staticmethod
    def from_dict(dict_data):
        repository = Repository(
            rep_type=dict_data['type'] if 'type' in dict_data else '',
            rep_path=dict_data['path'] if 'path' in dict_data else '',
            rep_version=dict_data['version'] if 'version' in dict_data else '',
        )

        return repository
