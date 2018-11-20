import os
from subprocess import PIPE, Popen as popen
from unittest import TestCase

from testfixtures import tempdir


class TestClean(TestCase):
    @tempdir()
    def test_clean(self, d):
        os.chdir(d.path)

        output = popen(['ezored', 'clean'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Finished'
        self.assertTrue(required in output)

    @tempdir()
    def test_init_and_clean(self, d):
        os.chdir(d.path)

        output = popen(['ezored', 'init'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'clean'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Finished'
        self.assertTrue(required in output)

    @tempdir()
    def test_init_download_dependency_and_clean(self, d):
        os.chdir(d.path)

        output = popen(['ezored', 'init'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'dependency', 'install'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        output = popen(['ezored', 'clean'], stdout=PIPE).communicate()[0]
        output = str(output)
        print(output)

        required = 'Finished'
        self.assertTrue(required in output)
