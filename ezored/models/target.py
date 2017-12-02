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
            self.name = process_data.parse_string(self.get_name())

            if self.repository:
                self.repository.prepare_from_process_data(process_data)

    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data['repository'] if 'repository' in dict_data else {}

        target = Target(
            name=dict_data['name'] if 'name' in dict_data else '',
            repository=Repository.from_dict(repository_data)
        )

        return target
