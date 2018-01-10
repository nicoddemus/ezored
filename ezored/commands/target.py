"""Target command"""

from ezored.models.process_data import ProcessData
from ezored.models.target_data import TargetData
from ezored.models.task import Task
from ezored.models.util.file_util import FileUtil
from .base import Base


class Target(Base):
    def run(self):
        if self.options['list']:
            self.list()
        elif self.options['build']:
            target_name = self.options['<target-name>'] if '<target-name>' in self.options else ''
            self.build(target_name)

    def list(self):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        Logger.d('Listing all targets...')

        project = Project.create_from_project_file()
        Logger.clean('Target List:')

        for target in project.targets:
            Logger.clean('  - {0}'.format(target.get_name()))

    def build(self, target_name):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        project = Project.create_from_project_file()

        if target_name:
            Logger.i('Build only target: {0}'.format(target_name))
        else:
            Logger.i('Build all targets')

        target_found = False

        for target in project.targets:
            process_data = ProcessData()
            process_data.reset()
            process_data.project_name = project.get_config_value('name')

            can_build = False

            if not target_name:
                can_build = True
            elif target.get_name() == target_name:
                can_build = True

            if can_build:
                Logger.d('Getting target data by target name: {0}...'.format(target_name))
                target_found = True

                # targets need be deleted to be always fresh with target data from dependencies
                target.remove()

                # build the target repository after download
                target.prepare_from_process_data(process_data)
                target.repository.download()
                target.repository.build(process_data)

                # get all target data from project dependencies
                target_data = TargetData()
                target_data.project_config = project.config

                for dependency in project.dependencies:
                    dependency.prepare_from_process_data(process_data)

                    new_target_data = dependency.get_target_data_by_target_name_and_parse(
                        target.get_name(),
                        process_data
                    )

                    target_data.merge(new_target_data)

                # back to target data
                target.prepare_from_process_data(process_data)

                # process target data and build
                target_project_file_data = target.load_target_project_file_data()

                if 'target' in target_project_file_data:
                    target_project_data = target_project_file_data['target']

                    # target tasks
                    if 'tasks' in target_project_data:
                        target_tasks_data = target_project_data['tasks']

                        for target_task_data in target_tasks_data:
                            task = Task.from_dict(target_task_data)
                            target_data.tasks.extend(task)

                    # run all tasks
                    Task.run_all_tasks(
                        tasks=target_data.tasks,
                        process_data=process_data,
                        template_data=target_data,
                        working_dir=target.repository.get_vendor_dir()
                    )

                    # build target
                    if 'build' in target_project_data:
                        Logger.i('Building target: {0}...'.format(target.get_name()))

                        target_project_data_build = target_project_data['build']

                        exitcode, stderr, stdout = FileUtil.run(
                            target_project_data_build,
                            target.repository.get_vendor_dir(),
                            process_data.get_environ()
                        )

                        if exitcode == 0:
                            Logger.i('Build finished for target: {0}'.format(target.get_name()))
                        else:
                            if stdout:
                                Logger.i('Build output for target: {0}'.format(target.get_name()))
                                Logger.clean(stdout)

                            if stderr:
                                Logger.i('Error output while build target: {0}'.format(target.get_name()))
                                Logger.clean(stderr)

                            Logger.f('Failed to build target: {0}'.format(target.get_name()))

        if not target_found:
            Logger.f('Target not found: {0}'.format(target_name))
