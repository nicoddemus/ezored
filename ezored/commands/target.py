"""Target command"""
from ezored.models.process_data import ProcessData
from ezored.models.target_data import TargetData

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
            Logger.clean('  - {0}'.format(target.name))

    def build(self, target_name):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        project = Project.create_from_project_file()

        process_data = ProcessData()
        process_data.reset()
        process_data.project_name = project.get_config_value('name')

        if target_name:
            Logger.d('Build only target: {0}'.format(target_name))
        else:
            Logger.d('Build all targets')

        for target in project.targets:
            can_build = False

            if not target_name:
                can_build = True
            elif target.get_name() == target_name:
                can_build = True

            if can_build:
                # build the target repository after download
                target.prepare_from_process_data(process_data)
                target.repository.download()
                target.repository.build(process_data)

                # get all dependencies data for this target
                target_data = TargetData()

                for dependency in project.dependencies:
                    dependency.prepare_from_process_data(process_data)
                    current_target_data = dependency.get_target_data_by_target_name_and_parse(target_name, process_data)
                    target_data.merge(current_target_data)

                print(target_data)
