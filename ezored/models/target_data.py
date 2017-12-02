class TargetData(object):
    project_name = ''
    project_config = ''

    header_search_paths = []
    library_search_paths = []

    source_groups = []

    library_links = []
    framework_links = []

    c_flags = []
    cxx_flags = []
    compiler_options = []

    copy_files = []

    def parse_all(self, process_data):
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

    def merge(self, target_data):
        self.header_search_paths.append(target_data.header_search_paths)
        self.library_search_paths.append(target_data.library_search_paths)

        self.source_groups.append(target_data.source_groups)

        self.library_links.append(target_data.library_links)
        self.framework_links.append(target_data.framework_links)

        self.c_flags.append(target_data.c_flags)
        self.cxx_flags.append(target_data.cxx_flags)
        self.compiler_options.append(target_data.compiler_options)

        self.copy_files.append(target_data.copy_files)
