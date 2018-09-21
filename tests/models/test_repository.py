import os
from unittest import TestCase

from testfixtures import tempdir

from ezored.models.constants import Constants
from ezored.models.repository import Repository
from ezored.models.util.file_util import FileUtil


class TestRepository(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Constants.REPOSITORY_TYPE_LOCAL,
            rep_path='/tmp/repository-test',
            rep_version='1.0.0',
        )

        self.assertEqual(repository.rep_type, Constants.REPOSITORY_TYPE_LOCAL)
        self.assertEqual(repository.rep_path, '/tmp/repository-test')
        self.assertEqual(repository.rep_version, '1.0.0')

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Constants.REPOSITORY_TYPE_LOCAL,
            rep_path='/tmp/repository-test',
            rep_version='1.0.0',
        )

        self.assertEqual(repository.get_name(), 'repository-test')

    def test_git_get_name(self):
        repository = Repository(
            rep_type=Constants.REPOSITORY_TYPE_GIT,
            rep_path='https://github.com/ezored/dependency-sample.git',
            rep_version='b:master',
        )

        self.assertEqual(repository.get_name(), 'dependency-sample')

    def test_from_dict(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': '1.0.0',
        })

        self.assertEqual(repository.rep_type, Constants.REPOSITORY_TYPE_GIT)
        self.assertEqual(repository.rep_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(repository.rep_version, '1.0.0')

    def test_get_git_data_branch(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 'b:master',
        })

        git_data_path, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(git_data_type, Constants.GIT_TYPE_BRANCH)
        self.assertEqual(git_data_version, 'master')

    def test_get_git_data_tag_without_prefix(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': '1.0.0',
        })

        git_data_path, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(git_data_type, Constants.GIT_TYPE_TAG)
        self.assertEqual(git_data_version, '1.0.0')

    def test_get_git_data_tag(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 't:1.0.0',
        })

        git_data_path, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(git_data_type, Constants.GIT_TYPE_TAG)
        self.assertEqual(git_data_version, '1.0.0')

    def test_get_git_data_commit(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 'c:123456',
        })

        git_data_path, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(git_data_type, Constants.GIT_TYPE_COMMIT)
        self.assertEqual(git_data_version, '123456')

    def test_get_git_data_empty_version(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': '',
        })

        git_data_path, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_path, 'https://github.com/ezored/dependency-sample.git')
        self.assertEqual(git_data_type, Constants.GIT_TYPE_BRANCH)
        self.assertEqual(git_data_version, 'master')

    def test_git_download_url(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 't:1.0.0',
        })

        download_url = repository.get_download_url()

        self.assertEqual(download_url, 'https://github.com/ezored/dependency-sample.git')

    def test_git_download_filename(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 't:1.0.0',
        })

        download_filename = repository.get_download_filename()

        self.assertEqual(download_filename, 'dependency-sample')

    def test_local_download_filename(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        download_filename = repository.get_download_filename()

        self.assertEqual(download_filename, 'sample-dependency')

    @tempdir()
    def test_git_temp_working_dir(self, d):
        os.chdir(d.path)

        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 't:1.0.0',
        })

        temp_working_dir = repository.get_temp_dir()

        self.assertEqual(
            temp_working_dir,
            os.path.join(FileUtil.get_current_dir(), Constants.TEMP_DIR, repository.get_temp_dir())
        )

    def test_local_temp_working_dir(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        temp_working_dir = repository.get_temp_dir()

        self.assertEqual(temp_working_dir, '/opt/ezored/sample-dependency')

    def test_git_get_dir_name(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_GIT,
            'path': 'https://github.com/ezored/dependency-sample.git',
            'version': 't:1.0.0',
        })

        dir_name = repository.get_dir_name()

        self.assertEqual(dir_name, 'dependency-sample')

    def test_local_get_dir_name(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        dir_name = repository.get_dir_name()

        self.assertEqual(dir_name, 'sample-dependency')
