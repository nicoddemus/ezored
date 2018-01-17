import os

from ezored.models.constants import Constants
from ezored.models.logger import Logger
from ezored.models.util.file_util import FileUtil
from .repository import Repository


class Target(object):
    def __init__(self, name, repository):
        self.name = name
        self.repository = repository

    def get_name(self):
        if self.name:
            return self.name
        else:
            return self.repository.get_name()

    def prepare_from_process_data(self, process_data):
        if process_data:
            process_data.set_target_data(
                name=self.get_name(),
                temp_dir=self.repository.get_temp_dir(),
                vendor_dir=self.repository.get_vendor_dir(),
                source_dir=self.repository.get_source_dir(),
                build_dir=os.path.join(FileUtil.get_current_dir(), Constants.BUILD_DIR, self.get_name()),
            )

            if self.repository:
                self.repository.prepare_from_process_data(process_data)

    def remove(self):
        Logger.d('Removing files for target: {0}...'.format(self.get_name()))
        vendor_dir = self.repository.get_vendor_dir()
        FileUtil.remove_dir(vendor_dir)

    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data['repository'] if 'repository' in dict_data else {}

        target = Target(
            name=dict_data['name'] if 'name' in dict_data else '',
            repository=Repository.from_dict(repository_data)
        )

        return target
