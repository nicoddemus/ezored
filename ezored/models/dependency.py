from ezored.models.logger import Logger
from ezored.models.source_file import SourceFile
from ezored.models.source_group import SourceGroup
from ezored.models.target_data import TargetData
from ezored.models.task import Task

from .repository import Repository


class Dependency(object):
    def __init__(self, repository):
        self.repository = repository
        self.tasks = []

    def get_name(self):
        return self.repository.get_name()

    def prepare_from_process_data(self, process_data):
        if process_data:
            process_data.set_dependency_data(
                name=self.repository.get_name(),
                temp_dir=self.repository.get_temp_dir(),
                vendor_dir=self.repository.get_vendor_dir(),
                source_dir=self.repository.get_source_dir(),
                build_dir=self.repository.get_vendor_dir(),
            )

            if self.repository:
                self.repository.prepare_from_process_data(process_data)

    def get_target_data_by_target_name_and_parse(self, target_name, process_data):
        Logger.d('Getting target data from dependency: {0}...'.format(self.get_name()))

        target_file_data = self.repository.load_target_data_file()

        if target_file_data:
            if 'targets' in target_file_data:
                targets_data = target_file_data['targets']

                for target_data_item in targets_data:
                    current_target_name = target_data_item['name']

                    if current_target_name == target_name:
                        # get target data
                        target_data = TargetData()

                        if 'data' in target_data_item:
                            target_data_dict = target_data_item['data']

                            if 'header_search_paths' in target_data_dict:
                                if target_data_dict['header_search_paths']:
                                    target_data.header_search_paths.extend(target_data_dict['header_search_paths'])

                            if 'library_search_paths' in target_data_dict:
                                if target_data_dict['library_search_paths']:
                                    target_data.library_search_paths.extend(target_data_dict['library_search_paths'])

                            if 'c_flags' in target_data_dict:
                                if target_data_dict['c_flags']:
                                    target_data.c_flags.extend(target_data_dict['c_flags'])

                            if 'cxx_flags' in target_data_dict:
                                if target_data_dict['cxx_flags']:
                                    target_data.cxx_flags.extend(target_data_dict['cxx_flags'])

                            if 'library_links' in target_data_dict:
                                if target_data_dict['library_links']:
                                    target_data.library_links.extend(target_data_dict['library_links'])

                            if 'framework_links' in target_data_dict:
                                if target_data_dict['framework_links']:
                                    target_data.framework_links.extend(target_data_dict['framework_links'])

                            if 'tasks' in target_data_dict:
                                if target_data_dict['tasks']:
                                    for target_data_task in target_data_dict['tasks']:
                                        task = Task.from_dict(target_data_task)
                                        target_data.tasks.append(task)

                            # create source group if have files for it
                            target_data_header_files = []
                            target_data_source_files = []

                            if 'header_files' in target_data_dict:
                                if target_data_dict['header_files']:
                                    for file_data in target_data_dict['header_files']:
                                        source_file = SourceFile.from_dict(file_data)

                                        if source_file:
                                            target_data_header_files.append(source_file)

                            if 'source_files' in target_data_dict:
                                if target_data_dict['source_files']:
                                    for file_data in target_data_dict['source_files']:
                                        source_file = SourceFile.from_dict(file_data)

                                        if source_file:
                                            target_data_source_files.append(source_file)

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
            repository=Repository.from_dict(repository_data)
        )

        return dependency
