import os
from unittest import TestCase

from ezored.models.constants import Constants
from ezored.models.process_data import ProcessData
from ezored.models.repository import Repository
from ezored.models.util.file_util import FileUtil
from testfixtures import tempdir


class TestProcessData(TestCase):
    def test_constructor(self):
        process_data = ProcessData()

        self.assertEqual(process_data.project_name, '')

    @tempdir()
    def test_reset(self, d):
        os.chdir(d.path)

        current_dir = FileUtil.get_current_dir()

        process_data = ProcessData()
        process_data.reset()

        process_data.project_name = Constants.PROJECT_NAME

        self.assertEqual(process_data.project_name, Constants.PROJECT_NAME)
        self.assertEqual(process_data.project_home_dir, current_dir)

        self.assertEqual(process_data.dependency_name, '')
        self.assertEqual(process_data.dependency_source_dir, '')
        self.assertEqual(process_data.dependency_build_dir, '')
        self.assertEqual(process_data.dependency_temp_dir, '')
        self.assertEqual(process_data.dependency_vendor_dir, '')

        self.assertEqual(process_data.target_name, '')
        self.assertEqual(process_data.target_source_dir, '')
        self.assertEqual(process_data.target_build_dir, '')
        self.assertEqual(process_data.target_temp_dir, '')
        self.assertEqual(process_data.target_vendor_dir, '')

        self.assertEqual(process_data.temp_dir, os.path.join(current_dir, Constants.TEMP_DIR))
        self.assertEqual(process_data.build_dir, os.path.join(current_dir, Constants.BUILD_DIR))
        self.assertEqual(process_data.vendor_dir, os.path.join(current_dir, Constants.VENDOR_DIR))

    @tempdir()
    def test_set_repository_name(self, d):
        os.chdir(d.path)

        repository_name = 'test-repository'

        process_data = ProcessData()
        process_data.reset()
        process_data.set_dependency_data(
            name=repository_name
        )

        self.assertEqual(process_data.dependency_name, repository_name)

    @tempdir()
    def test_parse_text(self, d):
        os.chdir(d.path)

        repository_name = 'test-repository'

        process_data = ProcessData()
        process_data.reset()

        repository = Repository.from_dict({
            'type': 'github',
            'name': 'ezored/dependency-sample',
            'version': 't:1.0.0',
        })

        process_data.set_dependency_data(
            name=repository.get_name(),
            temp_dir=repository.get_temp_dir(),
            vendor_dir=repository.get_vendor_dir(),
            source_dir=repository.get_source_dir(),
            build_dir=repository.get_build_dir(),
        )

        parsed_text = process_data.parse_text('${EZORED_DEPENDENCY_TEMP_DIR}')
        self.assertEqual(parsed_text, repository_name)

        parsed_text = process_data.parse_text('${EZORED_REPOSITORY_TEMP_DIR}')
        self.assertEqual(parsed_text, process_data.repository_temp_dir)

        parsed_text = process_data.parse_text('${EZORED_REPOSITORY_VENDOR_DIR}')
        self.assertEqual(parsed_text, process_data.repository_vendor_dir)

        parsed_text = process_data.parse_text('${EZORED_PROJECT_HOME}')
        self.assertEqual(parsed_text, process_data.project_home_dir)

    @tempdir()
    def test_parse_text_list(self, d):
        os.chdir(d.path)

        repository_name = 'test-repository'

        process_data = ProcessData()
        process_data.reset()
        process_data.set_repository_name_and_dir(repository_name, repository_name)

        parse_text_list = [
            '${EZORED_REPOSITORY_NAME}',
            '${EZORED_REPOSITORY_TEMP_DIR}',
            '${EZORED_REPOSITORY_VENDOR_DIR}',
            '${EZORED_PROJECT_HOME}',
        ]

        parsed_text_list = process_data.parse_text_list(parse_text_list)

        self.assertEqual(parsed_text_list[0], repository_name)
        self.assertEqual(parsed_text_list[1], process_data.repository_temp_dir)
        self.assertEqual(parsed_text_list[2], process_data.repository_vendor_dir)
        self.assertEqual(parsed_text_list[3], process_data.project_home_dir)
