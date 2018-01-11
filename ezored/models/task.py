import os

import jinja2

from ezored.models.logger import Logger
from ezored.models.util.file_util import FileUtil


class Task(object):
    TYPE_COPY_FILE = 'copy_file'
    TYPE_PARSE_FILE = 'parse_file'
    TYPE_RUN = 'run'

    def __init__(self, task_type, task_name, task_params):
        self.type = task_type
        self.name = task_name
        self.params = task_params

    def parse(self, process_data):
        if process_data:
            Logger.d('Parsing task: {0}...'.format(self.get_name()))

            if self.type == self.TYPE_COPY_FILE:
                if self.params and 'from_path' in self.params:
                    self.params['from_path'] = process_data.parse_text(self.params['from_path'])

                if self.params and 'to_path' in self.params:
                    self.params['to_path'] = process_data.parse_text(self.params['to_path'])

            elif self.type == self.TYPE_PARSE_FILE:
                if self.params and 'file' in self.params:
                    self.params['file'] = process_data.parse_text(self.params['file'])

            elif self.type == self.TYPE_RUN:
                if self.params and 'cmd' in self.params:
                    self.params['cmd'] = process_data.parse_text_list(self.params['cmd'])
            else:
                Logger.f('Invalid task type')
        else:
            Logger.d('Cannot parse task params with invalid source')

    def get_name(self):
        if len(self.name) > 0:
            return self.name

        if self.type == self.TYPE_COPY_FILE:
            return 'Copy file'
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
                from_path = self.params['from_path'] if self.params['from_path'] else None
                to_path = self.params['to_path'] if self.params['to_path'] else None

                FileUtil.copy_file(from_path=from_path, to_path=to_path)

            elif self.type == self.TYPE_PARSE_FILE:
                template_file = self.params['file'] if 'file' in self.params else None

                if template_file:
                    template_loader = jinja2.FileSystemLoader(searchpath='/')
                    template_env = jinja2.Environment(loader=template_loader)
                    template_file = template_file
                    template = template_env.get_template(template_file)
                    templ_result = template.render(target=template_data)

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

                        Logger.f('Failed to run task: {0}'.format(task.get_name()))
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
