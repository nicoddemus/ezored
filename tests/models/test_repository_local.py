from unittest import TestCase

from ezored.models.constants import Constants
from ezored.models.repository import Repository


class TestRepositoryLocal(TestCase):
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

    def test_local_download_filename(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        download_filename = repository.get_download_filename()

        self.assertEqual(download_filename, 'sample-dependency')

    def test_local_temp_working_dir(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        temp_working_dir = repository.get_temp_dir()

        self.assertEqual(temp_working_dir, '/opt/ezored/sample-dependency')

    def test_local_get_dir_name(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_LOCAL,
            'path': '/opt/ezored/sample-dependency',
            'version': '',
        })

        dir_name = repository.get_dir_name()

        self.assertEqual(dir_name, 'sample-dependency')
