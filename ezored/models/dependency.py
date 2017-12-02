from ezored.models.logger import Logger
from ezored.models.source_group import SourceGroup
from ezored.models.target_data import TargetData

from .repository import Repository


class Dependency(object):
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

    def get_target_data_by_target_name_and_parse(self, target_name, process_data):
        Logger.i('Getting target data from dependency: {0}...'.format(self.get_name()))

        target_file_data = self.repository.load_target_file_data()

        if 'targets' in target_file_data:
            targets_data = target_file_data['targets']

            for target_data_item in targets_data:
                current_target_name = target_data_item['name']

                if current_target_name == target_name:
                    # get target data
                    target_data = TargetData()
                    target_data_dict = target_data_item['data']

                    if 'header_search_paths' in target_data_dict:
                        target_data.header_search_paths.extend(target_data_dict['header_search_paths'])

                    if 'library_search_paths' in target_data_dict:
                        target_data.library_search_paths.extend(target_data_dict['library_search_paths'])

                    if 'c_flags' in target_data_dict:
                        target_data.c_flags.extend(target_data_dict['c_flags'])

                    if 'cxx_flags' in target_data_dict:
                        target_data.cxx_flags.extend(target_data_dict['cxx_flags'])

                    if 'framework_links' in target_data_dict:
                        target_data.framework_links.extend(target_data_dict['framework_links'])

                    if 'copy_files' in target_data_dict:
                        target_data.copy_files.extend(target_data_dict['copy_files'])

                    # create source group if have files for it
                    target_data_header_files = []
                    target_data_source_files = []

                    if 'header_files' in target_data_dict:
                        target_data_header_files = target_data_dict['header_files']

                    if 'source_files' in target_data_dict:
                        target_data_source_files = target_data_dict['source_files']

                    if len(target_data_header_files) > 0 or len(target_data_source_files) > 0:
                        target_data_source_group = SourceGroup()
                        target_data_source_group.name = self.get_name()
                        target_data_source_group.header_files = target_data_header_files
                        target_data_source_group.source_files = target_data_source_files

                        target_data.source_groups.append(target_data_source_group)

                    # parse all things
                    target_data.parse(process_data)
                    return target_data

    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data['repository'] if 'repository' in dict_data else {}

        dependency = Dependency(
            name=dict_data['name'] if 'name' in dict_data else '',
            repository=Repository.from_dict(repository_data)
        )

        return dependency
