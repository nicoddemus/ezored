import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from ezored.models.constants import Constants
from ezored.models.dependency import Dependency
from ezored.models.process_data import ProcessData
from ezored.models.project import Project
from ezored.models.repository import Repository
from ezored.models.target import Target
from ezored.models.target_data import TargetData
from testfixtures import tempdir


class TestTarget(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        target = Target(
            name='repository-test',
            repository=repository
        )

        self.assertEqual(target.get_name(), 'repository-test')
        self.assertEqual(target.repository.rep_type, Repository.TYPE_LOCAL)
        self.assertEqual(target.repository.rep_name, '/tmp/repository-test')
        self.assertEqual(target.repository.rep_version, '1.0.0')

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        target = Target(
            name='repository-test',
            repository=repository
        )

        self.assertEqual(target.get_name(), 'repository-test')

    def test_local_get_name_with_different_name_from_repository(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        target = Target(
            name='repository-test-diff',
            repository=repository
        )

        self.assertEqual(target.get_name(), 'repository-test-diff')

    def test_local_get_name_with_null_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        target = Target(
            name=None,
            repository=repository
        )

        self.assertEqual(target.get_name(), 'repository-test')

    def test_merge_target_data(self):
        # create project
        project = Project()
        project.config['name'] = Constants.PROJECT_NAME

        # create dependencies
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            repository=repository
        )

        project.dependencies.append(dependency)

        # process data
        process_data = ProcessData()
        process_data.reset()
        process_data.project_name = project.get_config_value('name')

        # process target data
        for target in project.targets:
            # get all target data from project dependencies
            target_data = TargetData()

            for dependency in project.dependencies:
                dependency.prepare_from_process_data(process_data)

                new_target_data = dependency.get_target_data_by_target_name_and_parse(
                    target.get_name(),
                    process_data
                )

                target_data.merge(new_target_data)

            # TODO: TargetData can only have current target data
