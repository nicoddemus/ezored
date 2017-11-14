"""Init command"""
import os

from .base import Base


class Init(Base):
    def run(self):
        self.initialize()

    def initialize(self):
        from ezored.models.constants import Constants
        from ezored.models.logger import Logger

        Logger.d("Initializing...")

        if os.path.isfile(Constants.PROJECT_FILE):
            Logger.d("Project file already exists, don't will be created")
        else:
            Logger.d("Creating project file...")
            project_file = open(Constants.PROJECT_FILE, "w")
            project_file.write(Constants.PROJECT_FILE_DATA)
            project_file.close()
            Logger.d("Project file created")

        Logger.i("EzoRed was initialized with success")