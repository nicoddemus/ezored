import os

import jinja2
from ezored.models.logger import Logger
from ezored.models.util.file_util import FileUtil


class Task(object):
    TYPE_COPY_FILE = 'copy_file'
    TYPE_COPY_FILES = 'copy_files'
    TYPE_PARSE_FILE = 'parse_file'
    TYPE_RUN = 'run'

    def __init__(self, task_type, task_name=None, task_params=None):
        self.type = task_type
        self.name = task_name
        self.params = task_params

    def parse(self, process_data):
        if process_data:
            Logger.d('Parsing task: {0}...'.format(self.get_name()))

            if self.type == self.TYPE_COPY_FILE:
                if self.params and 'from' in self.params:
                    self.params['from'] = process_data.parse_text(self.params['from'])

                if self.params and 'to' in self.params:
                    self.params['to'] = process_data.parse_text(self.params['to'])

            elif self.type == self.TYPE_COPY_FILES:
                if self.params and 'from' in self.params:
                    self.params['from'] = process_data.parse_text(self.params['from'])

                if self.params and 'to' in self.params:
                    self.params['to'] = process_data.parse_text(self.params['to'])

            elif self.type == self.TYPE_PARSE_FILE:
                if self.params and 'file' in self.params:
                    self.params['file'] = process_data.parse_text(self.params['file'])

            elif self.type == self.TYPE_RUN:
                if self.params and 'args' in self.params:
                    self.params['args'] = process_data.parse_text_list(self.params['args'])

            else:
                Logger.f('Invalid task type')
        else:
            Logger.d('Cannot parse task params with invalid process data')

    def get_name(self):
        if self.name and len(self.name) > 0:
            return self.name

        if self.type == self.TYPE_COPY_FILE:
            return 'Copy file'
        elif self.type == self.TYPE_COPY_FILES:
            return 'Copy files'
        elif self.type == self.TYPE_PARSE_FILE:
            return 'Parse file'
        elif self.type == self.TYPE_RUN:
            return 'Run'
        else:
            Logger.f('Invalid task type')

    def run(self, process_data, template_data, working_dir):
        Logger.d('Running task: {0}...'.format(self.get_name()))

        if process_data:
            if self.type == self.TYPE_COPY_FILE:
                from_path = self.params['from'] if self.params['from'] else None
                to_path = self.params['to'] if self.params['to'] else None

                FileUtil.copy_file(from_path=from_path, to_path=to_path)

            elif self.type == self.TYPE_COPY_FILES:
                to_path = self.params['to'] if self.params['to'] else None
                file_pattern = self.params['from'] if 'from' in self.params else None
                file_pattern = process_data.parse_text(file_pattern)
                found_files = FileUtil.find_files(file_pattern)

                for f in found_files:
                    if f:
                        FileUtil.copy_file(from_path=f, to_path=os.path.join(to_path, os.path.basename(f)))

            elif self.type == self.TYPE_PARSE_FILE:
                file_pattern = self.params['file'] if 'file' in self.params else None
                file_pattern = process_data.parse_text(file_pattern)
                found_files = FileUtil.find_files(file_pattern)

                for f in found_files:
                    if f:
                        template_file = os.path.abspath(f)
                        template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_file))
                        template_env = jinja2.Environment(loader=template_loader)
                        template = template_env.get_template(os.path.basename(template_file))
                        templ_result = template.render(template_data)

                        FileUtil.write_to_file(
                            os.path.dirname(template_file),
                            os.path.basename(template_file),
                            str(templ_result)
                        )

            elif self.type == self.TYPE_RUN:
                run_args = self.params['args'] if 'args' in self.params else None

                if run_args:
                    exitcode, stderr, stdout = FileUtil.run(
                        run_args,
                        working_dir,
                        process_data.get_environ()
                    )

                    if exitcode == 0:
                        Logger.i('Run finished for task: {0}'.format(self.get_name()))
                    else:
                        if stdout:
                            Logger.i('Run output for task: {0}'.format(self.get_name()))
                            Logger.clean(stdout)

                        if stderr:
                            Logger.i('Error output while run task: {0}'.format(self.get_name()))
                            Logger.clean(stderr)

                        Logger.f('Failed to run task: {0}'.format(self.get_name()))

            else:
                Logger.f('Invalid task type')
        else:
            Logger.d('Process data is invalid to run task')

    @staticmethod
    def run_all_tasks(tasks, process_data, template_data, working_dir):
        if tasks:
            Logger.d('Tasks to run: {0}...'.format(len(tasks)))

            for task in tasks:
                task.run(
                    process_data=process_data,
                    template_data=template_data,
                    working_dir=working_dir
                )
        else:
            Logger.d('Task list is invalid to execute')

    @staticmethod
    def from_dict(dict_data):
        task = Task(
            task_type=dict_data['type'] if 'type' in dict_data else '',
            task_name=dict_data['name'] if 'name' in dict_data else '',
            task_params=dict_data['params'] if 'params' in dict_data else {}
        )

        return task
