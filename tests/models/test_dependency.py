from ezored.models.dependency import Dependency
from ezored.models.repository import Repository
from unittest import TestCase


class TestDependency(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_path='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            name='repository-test',
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test')
        self.assertEqual(dependency.repository.rep_type, Repository.TYPE_LOCAL)
        self.assertEqual(dependency.repository.rep_path, '/tmp/repository-test')
        self.assertEqual(dependency.repository.rep_version, '1.0.0')

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_path='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            name='repository-test',
            repository=repository
        )

        self.assertEqual(dependency.get_name(), 'repository-test')

    def test_local_get_name_with_null_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_path='/tmp/repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            name=None,
            repository=repository
        )

        self.assertEqual(dependency.get_name(), None)

    def test_match_target_name_and_target_data(self):
        # create dependency
        dep_repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_path='dep-repository-test',
            rep_version='1.0.0',
        )

        dependency = Dependency(
            name='repository-test',
            repository=dep_repository
        )

        # check match
        match = dependency.match_name('test1-test2', 'test1-test2')
        self.assertEqual(match, True)

        match = dependency.match_name('test', 'test1-test2')
        self.assertEqual(match, True)

        match = dependency.match_name('test1', 'test1-test2')
        self.assertEqual(match, True)

        match = dependency.match_name('test2', 'test1-test2')
        self.assertEqual(match, True)

        match = dependency.match_name('-', 'test1-test2')
        self.assertEqual(match, True)

        match = dependency.match_name('arm', 'armv7-linux')
        self.assertEqual(match, True)

        match = dependency.match_name('linux', 'armv7-linux')
        self.assertEqual(match, True)
