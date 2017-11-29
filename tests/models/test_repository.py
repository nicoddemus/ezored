from unittest import TestCase

from ezored.models.repository import Repository


class TestRepository(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        self.assertEqual(repository.rep_type, Repository.TYPE_LOCAL)
        self.assertEqual(repository.rep_name, '/tmp/repository-test')
        self.assertEqual(repository.rep_version, '1.0.0')

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        self.assertEqual(repository.get_name(), 'repository-test')

    def test_github_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_GITHUB,
            rep_name='ezored/dependency-sample',
            rep_version='b:master',
        )

        self.assertEqual(repository.get_name(), 'ezored/dependency-sample')

    def test_from_dict(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': '1.0.0',
        })

        self.assertEqual(repository.rep_type, Repository.TYPE_GITHUB)
        self.assertEqual(repository.rep_name, 'ezored/dependency-sample')
        self.assertEqual(repository.rep_version, '1.0.0')

    def test_get_git_data_branch(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': 'b:master',
        })

        git_data_name, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_name, 'ezored/dependency-sample')
        self.assertEqual(git_data_type, Repository.GIT_TYPE_BRANCH)
        self.assertEqual(git_data_version, 'master')

    def test_get_git_data_tag_without_prefix(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': '1.0.0',
        })

        git_data_name, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_name, 'ezored/dependency-sample')
        self.assertEqual(git_data_type, Repository.GIT_TYPE_TAG)
        self.assertEqual(git_data_version, '1.0.0')

    def test_get_git_data_tag(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': 't:1.0.0',
        })

        git_data_name, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_name, 'ezored/dependency-sample')
        self.assertEqual(git_data_type, Repository.GIT_TYPE_TAG)
        self.assertEqual(git_data_version, '1.0.0')

    def test_get_git_data_commit(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': 'c:123456',
        })

        git_data_name, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_name, 'ezored/dependency-sample')
        self.assertEqual(git_data_type, Repository.GIT_TYPE_COMMIT)
        self.assertEqual(git_data_version, '123456')

    def test_get_git_data_empty_version(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': '',
        })

        git_data_name, git_data_type, git_data_version = repository.get_git_data()

        self.assertEqual(git_data_name, 'ezored/dependency-sample')
        self.assertEqual(git_data_type, Repository.GIT_TYPE_BRANCH)
        self.assertEqual(git_data_version, 'master')

    def test_github_download_url(self):
        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': 't:1.0.0',
        })

        download_url = repository.get_download_url()

        self.assertEqual(download_url, 'https://github.com/ezored/dependency-sample/archive/1.0.0.zip')
