import os

from ezored.models.constants import Constants
from ezored.models.util.file_util import FileUtil


class ProcessData(object):
    project_name = ''
    project_home_dir = ''

    repository_temp_dir = ''
    repository_vendor_dir = ''
    repository_name = ''

    temp_dir = ''
    build_dir = ''
    vendor_dir = ''

    def get_environ(self):
        env_data = dict(os.environ)
        env_data['{0}PROJECT_NAME'.format(Constants.ENV_VAR_PREFIX)] = self.project_name
        env_data['{0}PROJECT_HOME'.format(Constants.ENV_VAR_PREFIX)] = self.project_home_dir

        env_data['{0}REPOSITORY_TEMP_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.repository_temp_dir
        env_data['{0}REPOSITORY_VENDOR_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.repository_vendor_dir
        env_data['{0}REPOSITORY_NAME'.format(Constants.ENV_VAR_PREFIX)] = self.repository_name

        env_data['{0}TEMP_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.temp_dir
        env_data['{0}BUILD_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.build_dir
        env_data['{0}VENDOR_DIR'.format(Constants.ENV_VAR_PREFIX)] = self.vendor_dir

        return env_data

    def reset(self):
        self.project_name = ''
        self.project_home_dir = FileUtil.get_current_dir()

        self.repository_temp_dir = ''
        self.repository_vendor_dir = ''
        self.repository_name = ''

        self.temp_dir = os.path.join(self.project_home_dir, Constants.TEMP_DIR)
        self.build_dir = os.path.join(self.project_home_dir, Constants.BUILD_DIR)
        self.vendor_dir = os.path.join(self.project_home_dir, Constants.VENDOR_DIR)

    def set_repository_name_and_dir(self, rep_name, rep_dir):
        self.repository_name = rep_name
        self.repository_temp_dir = os.path.join(self.project_home_dir, Constants.TEMP_DIR, rep_dir)
        self.repository_vendor_dir = os.path.join(self.project_home_dir, Constants.VENDOR_DIR, rep_dir)

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

    def parse_copy_file_list(self, copy_file_list):
        if copy_file_list:
            for copy_file in copy_file_list:
                copy_file.from_path = self.parse_text(copy_file.from_path)
                copy_file.to_path = self.parse_text(copy_file.to_path)

        return copy_file_list

    def parse_sourge_group_list(self, source_group_list):
        if source_group_list:
            for source_group in source_group_list:
                source_group.name = self.parse_text(source_group.name)
                source_group.header_files = self.parse_text_list(source_group.header_files)
                source_group.source_files = self.parse_text_list(source_group.source_files)

        return source_group_list
