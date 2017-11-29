from .constants import Constants


class Logger(object):
    @staticmethod
    def clean(message):
        Logger.show('', message)

    @staticmethod
    def d(message):
        if Constants.DEBUG:
            Logger.show('DEBUG', message)

    @staticmethod
    def w(message):
        Logger.show('WARN', message)

    @staticmethod
    def i(message):
        Logger.show('INFO', message)

    @staticmethod
    def e(message):
        Logger.show('ERROR', message)

    @staticmethod
    def f(message):
        Logger.show('FATAL', message)
        exit(1)

    @staticmethod
    def show(prefix, message):
        if prefix == '':
            print('{0}'.format(message))
        else:
            print('{0}: {1}'.format(prefix, message))
