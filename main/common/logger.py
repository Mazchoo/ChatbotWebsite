

class Logger():

    level = 0

    def __init__(self):
        return

    @staticmethod
    def setLevel(level: int):
        Logger.level = level

    @staticmethod
    def printArgs(output: str, *args):
        first_arg = True
        for arg in args:
            if first_arg:
                first_arg = False
            else:
                output += ', '
            output += str(arg)
        return output

    @staticmethod
    def info(*args):
        if Logger.level > 0:
            return
        output_string = 'Log Info <= '
        output_string = Logger.printArgs(output_string, *args)
        print(output_string)

    @staticmethod
    def warn(*args):
        if Logger.level > 1:
            return
        output_string = 'Log Warn <= '
        output_string = Logger.printArgs(output_string, *args)
        print(output_string)

    @staticmethod
    def error(*args):
        if Logger.Loggerlevel > 2:
            return
        output_string = 'Log Error <= '
        output_string = Logger.printArgs(output_string, *args)
        print(output_string)
        raise Exception

    @staticmethod
    def fatal(*args):
        if Logger.level > 3:
            return
        output_string = 'Log Fatal <= '
        output_string = Logger.printArgs(output_string, *args)
        print(output_string)
        raise SystemError


if __name__ == '__main__':
    Logger.info('Dude', 1)
    Logger.warn('Man', {})
    try:
        Logger.error('Uh oh')
    except:
        print('Error causes exception')
