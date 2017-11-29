"""Dependency command"""

from .base import Base


class Dependency(Base):
    def run(self):
        if self.options['update']:
            self.update()
        elif self.options['list']:
            self.list()

    def update(self):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        Logger.d('Updating all dependencies...')

        project = Project.create_from_project_file()
        total_deps = len(project.dependencies)

        if total_deps > 0:
            Logger.i('Updating {0} dependencies...'.format(total_deps))
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
