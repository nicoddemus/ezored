import os
import sys
from unittest import TestCase

import pytest
from testfixtures import tempdir

from ezored.models.constants import Constants
from ezored.models.process_data import ProcessData
from ezored.models.task import Task
from ezored.models.util.file_util import FileUtil


class TestTask(TestCase):
    @tempdir()
    def test_task_copy_file(self, d):
        os.chdir(d.path)

        from_path = os.path.join(d.path, 'test-copy.txt')
        to_path = os.path.join(d.path, 'test-copy2.txt')

        d.write(from_path, 'sample data'.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_COPY_FILE,
            task_name='Sample copy file task',
            task_params={
                'from_path': from_path,
                'to_path': to_path
            }
        )

        process_data = ProcessData()
        template_data = {}

        task.parse(process_data)
        task.run(
            process_data=process_data,
            template_data=template_data,
            working_dir=d.path
        )

        self.assertTrue(os.path.exists(to_path))

    @tempdir()
    def test_task_parse_file(self, d):
        os.chdir(d.path)

        file_path = os.path.join(d.path, 'test-file.txt')

        d.write(file_path, '{{ name }}'.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_PARSE_FILE,
            task_name='Sample parse file task',
            task_params={
                'file': file_path
            }
        )

        process_data = ProcessData()
        template_data = {
            'name': Constants.PROJECT_NAME
        }

        task.parse(process_data)
        task.run(
            process_data=process_data,
            template_data=template_data,
            working_dir=d.path
        )

        content = FileUtil.read_file(file_path)

        self.assertEqual(Constants.PROJECT_NAME, content)

    @tempdir()
    def test_task_run(self, d):
        os.chdir(d.path)

        file_content = """
file = open("test-target-file.txt", "w") 
file.write("{0}") 
file.close()
        """

        file_content = file_content.format(Constants.PROJECT_NAME)

        file_path = os.path.join(d.path, 'test-file.py')
        target_file_path = os.path.join(d.path, 'test-target-file.txt')

        d.write(file_path, file_content.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_RUN,
            task_name='Sample run task',
            task_params={
                'args': ['python', file_path]
            }
        )

        process_data = ProcessData()
        template_data = {}

        task.parse(process_data)
        task.run(
            process_data=process_data,
            template_data=template_data,
            working_dir=d.path
        )

        content = FileUtil.read_file(target_file_path)

        self.assertEqual(Constants.PROJECT_NAME, content)

    @tempdir()
    def test_task_run_all_tasks(self, d):
        os.chdir(d.path)

        file_content = """
file = open("test-target-file.txt", "w") 
file.write("{0}") 
file.close()
        """

        file_content = file_content.format(Constants.PROJECT_NAME)

        file_path = os.path.join(d.path, 'test-file.py')
        target_file_path = os.path.join(d.path, 'test-target-file.txt')

        d.write(file_path, file_content.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_RUN,
            task_name='Sample run task - run all tasks',
            task_params={
                'args': ['python', file_path]
            }
        )

        process_data = ProcessData()
        template_data = {}

        task.parse(process_data)

        Task.run_all_tasks(
            [task],
            process_data=process_data,
            template_data=template_data,
            working_dir=d.path
        )

        content = FileUtil.read_file(target_file_path)

        self.assertEqual(Constants.PROJECT_NAME, content)

    def test_task_run_all_tasks_with_invalid_list(self):
        Task.run_all_tasks(
            tasks=None,
            process_data=None,
            template_data={},
            working_dir=None
        )

    @tempdir()
    def test_task_run_invalid_binary(self, d):
        os.chdir(d.path)

        task = Task(
            task_type=Task.TYPE_RUN,
            task_name='Sample run task - invalid binary',
            task_params={
                'args': ['dont_exists_xyz']
            }
        )

        process_data = ProcessData()
        template_data = {}

        task.parse(process_data)

        error_type = OSError

        if sys.version_info >= (3,):
            error_type = FileNotFoundError

        with pytest.raises(error_type) as error:
            task.run(
                process_data=process_data,
                template_data=template_data,
                working_dir=d.path
            )

        self.assertEqual(error.type, error_type)

    @tempdir()
    def test_task_run_generate_error(self, d):
        os.chdir(d.path)

        file_content = """
print("Sample task")
raise Exception('Sample task')
        """

        file_path = os.path.join(d.path, 'test-file.py')
        d.write(file_path, file_content.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_RUN,
            task_name='Sample run task',
            task_params={
                'args': ['python', file_path]
            }
        )

        with pytest.raises(SystemExit) as error:
            task.run(
                process_data=ProcessData(),
                template_data={},
                working_dir=d.path
            )

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    def test_task_create_from_dict(self):
        task_name = 'Sample task'
        task_type = Task.TYPE_RUN
        task_params = {
            'args': ['python']
        }

        dict_data = {
            'name': task_name,
            'type': task_type,
            'params': task_params
        }

        task = Task.from_dict(dict_data)

        self.assertEqual(task_name, task.name)
        self.assertEqual(task_type, task.type)
        self.assertEqual(task_params, task.params)

    def test_task_get_name(self):
        # run
        task = Task(
            task_type=Task.TYPE_RUN
        )

        self.assertEqual(task.get_name(), 'Run')

        # parse file
        task = Task(
            task_type=Task.TYPE_PARSE_FILE
        )

        self.assertEqual(task.get_name(), 'Parse file')

        # copy file
        task = Task(
            task_type=Task.TYPE_COPY_FILE
        )

        self.assertEqual(task.get_name(), 'Copy file')

    def test_task_invalid_type(self):
        task = Task(
            task_type='invalid_type_xyz'
        )

        with pytest.raises(SystemExit) as error:
            task.get_name()

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    def test_task_run_invalid_type(self):
        task = Task(
            task_name='Sample task',
            task_type='invalid_type_xyz'
        )

        with pytest.raises(SystemExit) as error:
            task.run(
                process_data=ProcessData(),
                template_data={},
                working_dir=None
            )

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    def test_task_run_invalid_process_data(self):
        task = Task(
            task_name='Sample task',
            task_type=Task.TYPE_RUN
        )

        task.run(
            process_data=None,
            template_data={},
            working_dir=None
        )

    def test_task_parse_invalid_type(self):
        task = Task(
            task_name='Sample task',
            task_type='invalid_type_xyz'
        )

        with pytest.raises(SystemExit) as error:
            task.parse(
                process_data=ProcessData()
            )

        self.assertEqual(error.type, SystemExit)
        self.assertEqual(error.value.code, 1)

    def test_task_parse_invalid_process_data(self):
        task = Task(
            task_type=Task.TYPE_RUN
        )

        task.parse(
            process_data=None
        )
