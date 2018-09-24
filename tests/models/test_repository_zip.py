import os
from unittest import TestCase

from testfixtures import tempdir

from ezored.models.constants import Constants
from ezored.models.repository import Repository
from ezored.models.util.file_util import FileUtil


class TestRepositoryZip(TestCase):
    def test_get_name(self):
        repository = Repository(
            rep_type=Constants.REPOSITORY_TYPE_ZIP,
            rep_path='http://ezored.com/downloads/dependency-sample.zip',
            rep_version=''
        )

        self.assertEqual(repository.get_name(), 'dependency-sample')

    def test_from_dict(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_ZIP,
            'path': 'http://ezored.com/downloads/dependency-sample.zip',
        })

        self.assertEqual(repository.rep_type, Constants.REPOSITORY_TYPE_ZIP)
        self.assertEqual(repository.rep_path, 'http://ezored.com/downloads/dependency-sample.zip')

    def test_download_url(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_ZIP,
            'path': 'http://ezored.com/downloads/dependency-sample.zip',
        })

        download_url = repository.get_download_url()

        self.assertEqual(download_url, 'http://ezored.com/downloads/dependency-sample.zip')

    def test_download_filename(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_ZIP,
            'path': 'http://ezored.com/downloads/dependency-sample.zip',
        })

        download_filename = repository.get_download_filename()

        self.assertEqual(download_filename, 'dependency-sample.zip')

    @tempdir()
    def test_temp_working_dir(self, d):
        os.chdir(d.path)

        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_ZIP,
            'path': 'http://ezored.com/downloads/dependency-sample.zip',
        })

        temp_working_dir = repository.get_temp_dir()

        self.assertEqual(
            temp_working_dir,
            os.path.join(FileUtil.get_current_dir(), Constants.TEMP_DIR, repository.get_temp_dir())
        )

    def test_get_dir_name(self):
        repository = Repository.from_dict({
            'type': Constants.REPOSITORY_TYPE_ZIP,
            'path': 'http://ezored.com/downloads/dependency-sample.zip',
        })

        dir_name = repository.get_dir_name()

        self.assertEqual(dir_name, 'dependency-sample')
