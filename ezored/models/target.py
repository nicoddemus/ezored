from .repository import Repository


class Target(object):
    target_name = ""
    target_repository = Repository

    def __init__(self, target_name, target_repository):
        self.target_name = target_name
        self.target_repository = target_repository

    @staticmethod
    def from_dict(dict_data):
        repository_data = dict_data["repository"] if "repository" in dict_data else {}

        target = Target(
            target_name=dict_data["name"] if "name" in dict_data else "",
            target_repository=Repository.from_dict(repository_data)
        )

        return target
