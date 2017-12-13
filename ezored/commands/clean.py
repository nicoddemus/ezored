"""Clean command"""

from .base import Base


class Clean(Base):
    def run(self):
        self.initialize()

    def initialize(self):
        from ezored.models.logger import Logger
        from ezored.models.constants import Constants
        from ezored.models.util.file_util import FileUtil

        Logger.i('Cleaning...')

        FileUtil.remove_dir(Constants.TEMP_DIR)
        FileUtil.remove_dir(Constants.VENDOR_DIR)

        Logger.i('Finished')
