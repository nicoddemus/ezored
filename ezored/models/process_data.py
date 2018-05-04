import os

from ezored.models.constants import Constants
from ezored.models.util.file_util import FileUtil
from os.path import expanduser


class ProcessData(object):
    def __init__(self):
        self.project_name = ''
        self.project_home_dir = ''

        self.temp_dir = ''
        self.build_dir = ''
        self.vendor_dir = ''

        self.target_temp_dir = ''
        self.target_source_dir = ''
        self.target_vendor_dir = ''
        self.target_build_dir = ''
        self.target_name = ''

        self.dependency_temp_dir = ''
        self.dependency_source_dir = ''
        self.dependency_vendor_dir = ''
        self.dependency_build_dir = ''
        self.dependency_name = ''

    def get_environ(self):
        env_data = dict(os.environ)

        env_data['HOME'] = expanduser('~')

        env_data['{0}PROJECT_NAME'.format(Constants.ENV_VAR_PREFIX)] = self.project_name
        env_data['{0}PROJECT_HOME'.format(Constants.ENV_VAR_PREFIX)] = self.project_home_dir

        env_data['{0}TARGET_TEMP_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.target_temp_dir
        env_data['{0}TARGET_SOURCE_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.target_source_dir
        env_data['{0}TARGET_VENDOR_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.target_vendor_dir
        env_data['{0}TARGET_BUILD_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.target_build_dir
        env_data['{0}TARGET_NAME'.format(Constants.ENV_VAR_PREFIX)] = self.target_name

        env_data['{0}DEPENDENCY_TEMP_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.dependency_temp_dir
        env_data['{0}DEPENDENCY_SOURCE_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.dependency_source_dir
        env_data['{0}DEPENDENCY_VENDOR_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.dependency_vendor_dir
        env_data['{0}DEPENDENCY_BUILD_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.dependency_build_dir
        env_data['{0}DEPENDENCY_NAME'.format(Constants.ENV_VAR_PREFIX)] = self.dependency_name

        env_data['{0}TEMP_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.temp_dir
        env_data['{0}BUILD_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.build_dir
        env_data['{0}VENDOR_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.vendor_dir

        return env_data

    def reset(self):
        self.project_name = ''
        self.project_home_dir = FileUtil.normalize_path(FileUtil.get_current_dir())

        self.target_temp_dir = ''
        self.target_source_dir = ''
        self.target_vendor_dir = ''
        self.target_build_dir = ''
        self.target_name = ''

        self.dependency_temp_dir = ''
        self.dependency_source_dir = ''
        self.dependency_vendor_dir = ''
        self.dependency_build_dir = ''
        self.dependency_name = ''

        self.temp_dir = FileUtil.normalize_path(os.path.join(self.project_home_dir, Constants.TEMP_DIR))
        self.build_dir = FileUtil.normalize_path(os.path.join(self.project_home_dir, Constants.BUILD_DIR))
        self.vendor_dir = FileUtil.normalize_path(os.path.join(self.project_home_dir, Constants.VENDOR_DIR))

    def set_dependency_data(self, name, temp_dir, vendor_dir, source_dir, build_dir):
        self.dependency_name = self.parse_text(name)
        self.dependency_temp_dir = self.parse_text(temp_dir)
        self.dependency_vendor_dir = self.parse_text(vendor_dir)
        self.dependency_source_dir = self.parse_text(source_dir)
        self.dependency_build_dir = self.parse_text(build_dir)

    def set_target_data(self, name, temp_dir, vendor_dir, source_dir, build_dir):
        self.target_name = self.parse_text(name)
        self.target_temp_dir = self.parse_text(temp_dir)
        self.target_vendor_dir = self.parse_text(vendor_dir)
        self.target_source_dir = self.parse_text(source_dir)
        self.target_build_dir = self.parse_text(build_dir)

    def parse_text(self, text):
        var_list = self.get_environ()

        if text and var_list:
            for var in var_list:
                text = text.replace('${' + var + '}', var_list.get(var))

        return text

    def parse_text_list(self, text_list):
        if text_list:
            count = 0

            for item in text_list:
                item = self.parse_text(item)
                text_list[count] = item
                count = count + 1

        return text_list

    def parse_task_list(self, task_list):
        if task_list:
            for task in task_list:
                task.parse(self)

        return task_list

    def parse_sourge_group_list(self, source_group_list):
        if source_group_list:
            for source_group in source_group_list:
                source_group.name = self.parse_text(source_group.name)

                # header files
                for source_file in source_group.header_files:
                    source_file.file = self.parse_text(source_file.file)
                    source_file.compile_flags = self.parse_text(source_file.compile_flags)

                # source files
                for source_file in source_group.source_files:
                    source_file.file = self.parse_text(source_file.file)
                    source_file.compile_flags = self.parse_text(source_file.compile_flags)

        return source_group_list
