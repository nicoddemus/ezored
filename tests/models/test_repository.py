from unittest import TestCase

from ezored.models.repository import Repository


class TestRepository(TestCase):
    def test_constructor(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name="/tmp/repository-test",
            rep_version="1.0.0",
        )

        self.assertTrue(repository.rep_type == Repository.TYPE_LOCAL)
        self.assertTrue(repository.rep_name == "/tmp/repository-test")
        self.assertTrue(repository.rep_version == "1.0.0")

    def test_local_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_LOCAL,
            rep_name="/tmp/repository-test",
            rep_version="1.0.0",
        )

        self.assertTrue(repository.get_name() == "repository-test")

    def test_github_get_name(self):
        repository = Repository(
            rep_type=Repository.TYPE_GITHUB,
            rep_name="ezored/dependency-sample",
            rep_version="b:master",
        )

        self.assertTrue(repository.get_name() == "ezored/dependency-sample")

    def test_from_dict(self):
        repository = Repository.from_dict({
            "type": "github",
            "name": "ezored/dependency-sample",
            "version": "1.0.0",
        })

        self.assertTrue(repository.rep_type == Repository.TYPE_GITHUB)
        self.assertTrue(repository.rep_name == "ezored/dependency-sample")
        self.assertTrue(repository.rep_version == "1.0.0")
