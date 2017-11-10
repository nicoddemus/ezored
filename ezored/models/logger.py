class Logger(object):
    @staticmethod
    def clean(message):
        Logger.show("", message)

    @staticmethod
    def d(message):
        Logger.show("DEBUG", message)

    @staticmethod
    def w(message):
        Logger.show("WARN", message)

    @staticmethod
    def i(message):
        Logger.show("INFO", message)

    @staticmethod
    def e(message):
        Logger.show("ERROR", message)

    @staticmethod
    def f(message):
        Logger.show("FATAL", message)
        exit(1)

    @staticmethod
    def show(prefix, message):
        if prefix == "":
            print("{}".format(message))
        else:
            print("{}: {}".format(prefix, message))
