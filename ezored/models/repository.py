import os
import re


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

    def download(self):
        pass

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

    @staticmethod
    def from_dict(dict_data):
        repository = Repository(
            rep_type=dict_data['type'] if 'type' in dict_data else '',
            rep_name=dict_data['name'] if 'name' in dict_data else '',
            rep_version=dict_data['version'] if 'version' in dict_data else '',
        )

        return repository
