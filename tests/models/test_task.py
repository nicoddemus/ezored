import os
from unittest import TestCase

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

        d.write(from_path, 'sample data')

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
file.write("EzoRed") 
file.close()
        """

        file_path = os.path.join(d.path, 'test-file.py')
        target_file_path = os.path.join(d.path, 'test-target-file.txt')

        d.write(file_path, file_content.encode('utf-8'))

        task = Task(
            task_type=Task.TYPE_RUN,
            task_name='Sample run task',
            task_params={
                'args': [file_path]
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
