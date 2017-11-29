import os
import re

from ezored.models.constants import Constants
from ezored.models.logger import Logger
from ezored.models.util.download_util import DownloadUtil
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
            return 'https://github.com/{0}/archive/{1}.zip'.format(git_data_name, git_data_version)
        else:
            return ''

    def get_download_filename(self):
        if self.rep_type == Repository.TYPE_GITHUB:
            _, _, git_data_version = self.get_git_data()
            return '{0}.{1}'.format(
                slugify('{0}-{1}'.format(
                    self.rep_name,
                    git_data_version)
                ),
                Constants.GITHUB_DOWNLOAD_EXTENSION)
        elif self.rep_type == Repository.TYPE_LOCAL:
            _, filename = os.path.split(self.rep_name)
            return slugify(filename)
        else:
            return ''

    def download(self):
        # check repository type
        if self.rep_type == Repository.TYPE_GITHUB:
            Logger.i('Getting dependency: {0}...'.format(self.rep_name))

            # prepare download data
            download_url = self.get_download_url()
            download_filename = self.get_download_filename()
            download_dest_dir = Constants.TEMPORARY_DIR
            download_dest_path = os.path.join(Constants.TEMPORARY_DIR, download_filename)

            _, _, git_data_version = self.get_git_data()

            # skip if exists
            if os.path.isfile(download_dest_path):
                Logger.i('Dependency already downloaded: {0}'.format(self.rep_name))
            else:
                DownloadUtil.download_file(download_url, download_dest_dir, download_filename)

                # check if file was downloaded
                if os.path.isfile(download_dest_path):
                    Logger.i('Dependency downloaded: {0}'.format(self.rep_name))
                else:
                    Logger.f('Problems when obtain dependency: {0}'.format(self.rep_name))

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

    @staticmethod
    def from_dict(dict_data):
        repository = Repository(
            rep_type=dict_data['type'] if 'type' in dict_data else '',
            rep_name=dict_data['name'] if 'name' in dict_data else '',
            rep_version=dict_data['version'] if 'version' in dict_data else '',
        )

        return repository
