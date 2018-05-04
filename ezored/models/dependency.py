import re

from ezored.models.logger import Logger
from ezored.models.source_file import SourceFile
from ezored.models.source_group import SourceGroup
from ezored.models.target_data import TargetData
from ezored.models.task import Task
from ezored.models.util.file_util import FileUtil

from .repository import Repository


class Dependency(object):
    def __init__(self, name, repository):
        self.name = name
        self.repository = repository
        self.tasks = []

    def get_name(self):
        return self.name

    def prepare_from_process_data(self, process_data):
        if process_data:
            process_data.set_dependency_data(
                name=self.get_name(),
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

                    if self.match_name(pattern=current_target_name, name=target_name):
                        # get target data
                        target_data = TargetData()

                        if 'data' in target_data_item:
                            target_data_dict = target_data_item['data']

                            if 'header_search_paths' in target_data_dict:
                                if target_data_dict['header_search_paths']:
                                    target_data.header_search_paths.extend(FileUtil.normalize_path_from_list(
                                        target_data_dict['header_search_paths']
                                    ))

                            if 'library_search_paths' in target_data_dict:
                                if target_data_dict['library_search_paths']:
                                    target_data.library_search_paths.extend(FileUtil.normalize_path_from_list(
                                        target_data_dict['library_search_paths']
                                    ))

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
                                        # find all files
                                        source_file_to_find = SourceFile.from_dict(file_data)

                                        if source_file_to_find:
                                            # process file pattern before
                                            file_pattern = source_file_to_find.file
                                            file_pattern = process_data.parse_text(file_pattern)
                                            found_files = FileUtil.find_files(file_pattern)

                                            # create new source file for each found file
                                            for f in found_files:
                                                target_data_header_files.append(
                                                    SourceFile(
                                                        source_file=f,
                                                        compile_flags=source_file_to_find.compile_flags
                                                    )
                                                )

                            if 'source_files' in target_data_dict:
                                if target_data_dict['source_files']:
                                    for file_data in target_data_dict['source_files']:
                                        # find all files
                                        source_file_to_find = SourceFile.from_dict(file_data)

                                        if source_file_to_find:
                                            # process file pattern before
                                            file_pattern = source_file_to_find.file
                                            file_pattern = process_data.parse_text(file_pattern)
                                            found_files = FileUtil.find_files(file_pattern)

                                            # create new source file for each found file
                                            for f in found_files:
                                                target_data_source_files.append(
                                                    SourceFile(
                                                        source_file=FileUtil.normalize_path(f),
                                                        compile_flags=source_file_to_find.compile_flags
                                                    )
                                                )

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
            name=dict_data['name'],
            repository=Repository.from_dict(repository_data)
        )

        return dependency

    def match_name(self, pattern, name):
        match_pattern = re.compile(re.escape(pattern), flags=re.IGNORECASE | re.MULTILINE)
        match = re.search(match_pattern, name)

        if match is None:
            return False
        else:
            return True
