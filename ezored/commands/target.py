"""Target command"""
import os

from ezored.models.constants import Constants
from ezored.models.process_data import ProcessData
from ezored.models.target_data import TargetData
from ezored.models.task import Task
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
        import importlib
        import sys

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
                target.repository.build(
                    project=project,
                    process_data=process_data
                )

                # get all target data from project dependencies
                target_data = TargetData()
                target_data.project_home = target.repository.get_vendor_dir()
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
                target_data_file = target.repository.load_target_data_file()

                if 'target' in target_data_file:
                    target_project_data = target_data_file['target']

                    # target tasks
                    if 'tasks' in target_project_data:
                        target_tasks_data = target_project_data['tasks']

                        for target_task_data in target_tasks_data:
                            task = Task.from_dict(target_task_data)
                            task.parse(process_data)
                            target_data.tasks.append(task)

                    # run all tasks
                    Task.run_all_tasks(
                        tasks=target_data.tasks,
                        process_data=process_data,
                        template_data={
                            'target': target_data
                        },
                        working_dir=target.repository.get_vendor_dir()
                    )

                    # build target
                    Logger.i('Building target: {0}...'.format(target.get_name()))

                    sys_path = list(sys.path)
                    original_cwd = os.getcwd()

                    try:
                        sys.path.insert(0, target.repository.get_vendor_dir())

                        target_module = importlib.import_module(Constants.TARGET_MODULE_NAME)
                        do_build = getattr(target_module, 'do_build')

                        do_build(
                            params={
                                'project': project,
                                'target': target,
                                'target_data': target_data,
                                'process_data': process_data,
                            }
                        )

                        del sys.modules[Constants.TARGET_MODULE_NAME]
                        del target_module
                        del do_build
                    except Exception as e:
                        Logger.e("Error while call 'do_build' on target {0}: {1}".format(target.get_name(), e.message))
                        raise

                    sys.path = sys_path
                    os.chdir(original_cwd)

        if not target_found:
            Logger.f('Target not found: {0}'.format(target_name))
