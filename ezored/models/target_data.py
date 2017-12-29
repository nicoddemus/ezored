from ezored.models.logger import Logger


class TargetData(object):
    project_name = ''

    def __init__(self):
        self.project_config = {}

        self.header_search_paths = []
        self.library_search_paths = []

        self.source_groups = []

        self.library_links = []
        self.framework_links = []

        self.c_flags = []
        self.cxx_flags = []
        self.compiler_options = []

        self.copy_files = []

    def parse(self, process_data):
        if process_data:
            Logger.d('Parsing target data...')

            self.project_name = process_data.parse_text(self.project_name)

            self.header_search_paths = process_data.parse_text_list(self.header_search_paths)
            self.library_search_paths = process_data.parse_text_list(self.library_search_paths)

            self.source_groups = process_data.parse_sourge_group_list(self.source_groups)

            self.library_links = process_data.parse_text_list(self.library_links)
            self.framework_links = process_data.parse_text_list(self.framework_links)

            self.c_flags = process_data.parse_text_list(self.c_flags)
            self.cxx_flags = process_data.parse_text_list(self.cxx_flags)
            self.compiler_options = process_data.parse_text_list(self.compiler_options)

            self.copy_files = process_data.parse_copy_file_list(self.copy_files)
        else:
            Logger.d('Cannot parse target data with invalid source')

    def merge(self, target_data):
        if target_data:
            Logger.d('Merging target data...')

            self.header_search_paths.extend(target_data.header_search_paths)
            self.library_search_paths.extend(target_data.library_search_paths)

            self.source_groups.extend(target_data.source_groups)

            self.library_links.extend(target_data.library_links)
            self.framework_links.extend(target_data.framework_links)

            self.c_flags.extend(target_data.c_flags)
            self.cxx_flags.extend(target_data.cxx_flags)
            self.compiler_options.extend(target_data.compiler_options)

            self.copy_files.extend(target_data.copy_files)
        else:
            Logger.d('Cannot merge target data with invalid source')
