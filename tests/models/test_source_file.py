from unittest import TestCase

from ezored.models.source_file import SourceFile


class TesSourceFile(TestCase):
    def test_source_file(self):
        source_file = SourceFile(
            source_file='/tmp/main.cpp',
            compile_flags='-std=c++11'
        )

        self.assertEqual('/tmp/main.cpp', source_file.file)
        self.assertEqual('-std=c++11', source_file.compile_flags)

    def test_source_file_from_dict(self):
        dict_data = {
            'file': '/tmp/main.cpp',
            'compile_flags': '-std=c++11'
        }

        source_file = SourceFile.from_dict(dict_data)

        self.assertEqual(dict_data['file'], source_file.file)
        self.assertEqual(dict_data['compile_flags'], source_file.compile_flags)
