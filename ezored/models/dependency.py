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
        Logger.i('Getting target data by target name: {0}...'.format(target_name))

        target_file_data = self.repository.load_target_file_data()

        if 'targets' in target_file_data:
            targets_data = target_file_data['targets']

            for target_data_item in targets_data:
                current_target_name = target_data_item['name']

                if current_target_name == target_name:
                    # get target data
                    target_data = TargetData()
                    target_data_dict = target_data_item['data']

                    target_data.header_search_paths.append(target_data_dict['header_search_paths'])
                    target_data.library_search_paths.append(target_data_dict['header_search_paths'])

                    target_data.c_flags.append(target_data_dict['c_flags'])
                    target_data.cxx_flags.append(target_data_dict['cxx_flags'])
                    target_data.framework_links.append(target_data_dict['framework_links'])

                    target_data.copy_files.append(target_data_dict['copy_files'])

                    # create source group if have files for it
                    target_data_header_files = target_data_dict['header_files']
                    target_data_source_files = target_data_dict['source_files']

                    if len(target_data_header_files) > 0 or len(target_data_source_files) > 0:
                        target_data_source_group = SourceGroup()
                        target_data_source_group.header_files = target_data_header_files
                        target_data_source_group.source_files = target_data_source_files

                        target_data.source_groups.append(target_data_source_group)

                    # parse all things
                    target_data.parse_all(process_data)


    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data['repository'] if 'repository' in dict_data else {}

        dependency = Dependency(
            name=dict_data['name'] if 'name' in dict_data else '',
            repository=Repository.from_dict(repository_data)
        )

        return dependency
