import os
from unittest import TestCase

import pytest
from ezored.models.constants import Constants
from ezored.models.project import Project
from testfixtures import tempdir


class TestProject(TestCase):
    @tempdir()
    def test_create_from_project_file(self, d):
        os.chdir(d.path)

        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))

        project = Project.create_from_project_file()

        self.assertEqual(project.config['name'], 'ezored')

    @tempdir()
    def test_project_file_not_exists(self, d):
        with pytest.raises(SystemExit) as error:
            os.chdir(d.path)
            Project.create_from_project_file()

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    @tempdir()
    def test_project_file_invalid(self, d):
        with pytest.raises(SystemExit) as error:
            os.chdir(d.path)
            d.write(Constants.PROJECT_FILE, '* invalid data *'.encode('utf-8'))
            Project.create_from_project_file()

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    @tempdir()
    def test_project_get_valid_config(self, d):
        os.chdir(d.path)
        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))
        project = Project.create_from_project_file()

        self.assertEqual(project.get_config_value('name'), Constants.PROJECT_NAME)

    @tempdir()
    def test_project_get_invalid_config(self, d):
        os.chdir(d.path)
        d.write(Constants.PROJECT_FILE, Constants.PROJECT_FILE_DATA.encode('utf-8'))
        project = Project.create_from_project_file()

        self.assertEqual(project.get_config_value('unknown'), None)
