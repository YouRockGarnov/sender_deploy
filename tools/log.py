
class Logger:
    def info(self, mess):
        print('\n', '!!! LOGGER INFO: {0}'.format(mess), '\n')

    def error(self, mess):
        print('\n', '!!! LOGGER ERROR: {0}'.format(mess), '\n')

logger = Logger()
