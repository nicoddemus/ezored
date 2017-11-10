"""Dependency command"""

from .base import Base
from ..models.logger import Logger
from ..models.project import Project


class Dependency(Base):
    def run(self):
        if self.options["update"]:
            self.update()
        elif self.options["list"]:
            self.list()
        else:
            self.list()

    def update(self):
        Logger.d("Checking dependencies...")

    def list(self):
        project = Project.create_from_project_file()
        Logger.clean("Dependency List:")

        for dependency in project.dependencies:
            Logger.clean("  - {}".format(dependency.get_name()))
