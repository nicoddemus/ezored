"""Target command"""

from .base import Base


class Target(Base):
    def run(self):
        if self.options["list"]:
            self.list()

    def list(self):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        Logger.d("Listing all targets...")

        project = Project.create_from_project_file()
        Logger.clean("Target List:")

        for target in project.targets:
            Logger.clean("  - {0}".format(target.target_name))
