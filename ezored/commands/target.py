"""Target command"""
import os

import jinja2
from ezored.models.process_data import ProcessData
from ezored.models.target_data import TargetData
from ezored.models.util.file_util import FileUtil

from .base import Base


class Target(Base):
    def run(self):
        if self.options['list']:
            self.list()
        elif self.options['build']:
            target_name = self.options['<target-name>'] if '<target-name>' in self.options else ''
            self.build(target_name)

    def list(self):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        Logger.d('Listing all targets...')

        project = Project.create_from_project_file()
        Logger.clean('Target List:')

        for target in project.targets:
            Logger.clean('  - {0}'.format(target.get_name()))

    def build(self, target_name):
        from ezored.models.logger import Logger
        from ezored.models.project import Project

        project = Project.create_from_project_file()

        process_data = ProcessData()
        process_data.reset()
        process_data.project_name = project.get_config_value('name')

        if target_name:
            Logger.d('Build only target: {0}'.format(target_name))
        else:
            Logger.d('Build all targets')

        target_found = False

        for target in project.targets:
            can_build = False

            if not target_name:
                can_build = True
            elif target.get_name() == target_name:
                can_build = True

            if can_build:
                Logger.i('Getting target data by target name: {0}...'.format(target_name))
                target_found = True

                # targets need be deleted to be always fresh with target data from dependencies
                target.remove()

                # build the target repository after download
                target.prepare_from_process_data(process_data)
                target.repository.download()
                target.repository.build(process_data)

                # get all target data from project dependencies
                target_data = TargetData()
                target_data.project_config = project.config

                for dependency in project.dependencies:
                    dependency.prepare_from_process_data(process_data)
                    current_target_data = dependency.get_target_data_by_target_name_and_parse(target_name, process_data)
                    target_data.merge(current_target_data)

                # back to target data
                target.prepare_from_process_data(process_data)

                # copy files from dependencies to target directory
                FileUtil.copy_files_from_list(target_data.copy_files)

                # parse files path and it content
                target_project_file_data = target.load_target_project_file_data()

                if 'target' in target_project_file_data:
                    target_project_data = target_project_file_data['target']

                    # parse files
                    if 'parse_files' in target_project_data:
                        target_project_data_parse_files = target_project_data['parse_files']

                        if target_project_data_parse_files:
                            Logger.d('Files to parse from target: {0}'.format(len(target_project_data_parse_files)))

                            target_project_data_parse_files = process_data.parse_text_list(
                                target_project_data_parse_files
                            )

                            for target_project_data_parse_file in target_project_data_parse_files:
                                template_loader = jinja2.FileSystemLoader(searchpath='/')
                                template_env = jinja2.Environment(loader=template_loader)
                                template_file = target_project_data_parse_file
                                template = template_env.get_template(template_file)
                                templ_result = template.render(target=target_data)

                                FileUtil.write_to_file(
                                    os.path.dirname(target_project_data_parse_file),
                                    os.path.basename(target_project_data_parse_file),
                                    str(templ_result)
                                )
                        else:
                            Logger.d('No files need to parse from target: {0}'.format(target.get_name()))

                    # build target
                    if 'build' in target_project_data:
                        target_project_data_build = target_project_data['build']

                        exitcode, stderr, stdout = FileUtil.run(
                            target_project_data_build,
                            target.repository.get_vendor_dir(),
                            process_data.get_environ()
                        )

                        if exitcode == 0:
                            Logger.i('Build finished for target: {0}'.format(target.get_name()))
                        else:
                            if stdout:
                                Logger.i('Build output for target: {0}'.format(target.get_name()))
                                Logger.clean(stdout)

                            if stderr:
                                Logger.i('Error output while build target: {0}'.format(target.get_name()))
                                Logger.clean(stderr)

                            Logger.f('Failed to build target: {0}'.format(target.get_name()))

        if not target_found:
            Logger.f('Target not found: {0}'.format(target_name))
