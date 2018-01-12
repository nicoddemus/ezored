class SourceFile(object):

    def __init__(self, source_file, compile_flags=''):
        self.file = source_file
        self.compile_flags = compile_flags

    @staticmethod
    def from_dict(dict_data):
        source_file = SourceFile(
            source_file=dict_data['file'] if 'file' in dict_data else None,
            compile_flags=dict_data['compile_flags'] if 'compile_flags' in dict_data else None
        )

        return source_file
