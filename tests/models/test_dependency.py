from unittest import TestCase

from ezored.models.dependency import Dependency
from ezored.models.repository import Repository


class TestDependency(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test')
        self.assertEqual(dependency.repository.rep_type, Repository.TYPE_LOCAL)
        self.assertEqual(dependency.repository.rep_name, '/tmp/repository-test')
        self.assertEqual(dependency.repository.rep_version, '1.0.0')

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test')

    def test_local_get_name_with_different_name_from_repository(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test-diff')

    def test_local_get_name_with_null_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test')
