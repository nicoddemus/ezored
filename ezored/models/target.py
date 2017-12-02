import os

import yaml
from ezored.models.constants import Constants
from ezored.models.logger import Logger

from .repository import Repository


class Target(object):
    name = ''
    repository = Repository

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
            self.name = process_data.parse_text(self.get_name())

            if self.repository:
                self.repository.prepare_from_process_data(process_data)

    def load_target_project_file_data(self):
        Logger.d('Loading target project file for target: {0}...'.format(self.get_name()))

        vendor_dir = self.repository.get_vendor_dir()
        target_file_path = os.path.join(vendor_dir, Constants.TARGET_PROJECT_FILE)

        try:
            with open(target_file_path, 'r') as stream:
                return yaml.load(stream)
        except IOError as exc:
            Logger.f('Error while read target project file: {0}'.format(exc))


    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data['repository'] if 'repository' in dict_data else {}

        target = Target(
            name=dict_data['name'] if 'name' in dict_data else '',
            repository=Repository.from_dict(repository_data)
        )

        return target
