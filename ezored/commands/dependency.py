"""Dependency command"""
from ezored.models.process_data import ProcessData

from .base import Base


class Dependency(Base):
    def run(self):
        if self.options['update']:
            dependency_name = self.options['<dependency-name>'] if '<dependency-name>' in self.options else ''
            self.update(dependency_name)
        elif self.options['list']:
            self.list()

    def update(self, dependency_name):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        project = Project.create_from_project_file()

        if dependency_name:
            Logger.i('Update dependency "{0}"'.format(dependency_name))
        else:
            Logger.i('Update all dependencies')

        dependency_found = False
        total_deps = len(project.dependencies)

        if total_deps > 0:
            for dependency in project.dependencies:
                process_data = ProcessData()
                process_data.reset()
                process_data.project_name = project.get_config_value('name')

                can_build = False

                if not dependency_name:
                    can_build = True
                elif dependency.get_name() == dependency_name:
                    can_build = True

                if can_build:
                    Logger.i('Updating dependency "{0}"...'.format(dependency.get_name()))
                    dependency_found = True

                    dependency.prepare_from_process_data(process_data)
                    dependency.repository.download()
                    dependency.repository.build(
                        project=project,
                        process_data=process_data
                    )

                    Logger.i('Dependency "{0}" updated'.format(dependency.get_name()))

            if not dependency_found:
                Logger.f('Dependency not found: {0}'.format(dependency_name))
        else:
            Logger.i('Your project does not have dependencies')

    def list(self):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        Logger.d('Listing all dependencies...')

        project = Project.create_from_project_file()
        Logger.clean('Dependency List:')

        for dependency in project.dependencies:
            Logger.clean('  - {0}'.format(dependency.get_name()))
