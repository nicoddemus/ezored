import os


class Repository(object):
    TYPE_LOCAL = "local"
    TYPE_GITHUB = "github"

    rep_type = ""
    rep_name = ""
    rep_version = ""

    def __init__(self, rep_type, rep_name, rep_version):
        self.rep_type = rep_type
        self.rep_name = rep_name
        self.rep_version = rep_version

    def get_name(self):
        if self.rep_type == Repository.TYPE_LOCAL:
            rep_path, rep_file = os.path.split(self.rep_name)
            return rep_file
        else:
            return self.rep_name

    @staticmethod
    def from_dict(dict_data):
        repository = Repository(
            rep_type=dict_data["type"] if "type" in dict_data else "",
            rep_name=dict_data["name"] if "name" in dict_data else "",
            rep_version=dict_data["version"] if "version" in dict_data else "",
        )

        return repository
