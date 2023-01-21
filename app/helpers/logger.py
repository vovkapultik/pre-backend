import logging

from colorlog import ColoredFormatter


class Logger(logging.Logger):
    super(logging.Logger)

    log_level = logging.DEBUG
    log_format = "%(white)s[%(asctime)s]  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

    colors = {
        'WARNING': 'yellow',
        'INFO': 'blue',
        'DEBUG': 'white',
        'CRITICAL': 'red',
        'ERROR': 'red'
    }

    logging.root.setLevel(log_level)
    formatter = ColoredFormatter(fmt=log_format,
                                 datefmt="%Y-%m-%d %H:%M:%S",
                                 log_colors=colors)

    stream = logging.StreamHandler()
    stream.setLevel(log_level)
    stream.setFormatter(formatter)

    internal_log = logging.getLogger('pythonConfig')
    internal_log.setLevel(log_level)
    internal_log.addHandler(stream)

    def debug(self, msg, *args, **kwargs):
        self.internal_log.debug(msg)

    def info(self, msg, *args, **kwargs):
        self.internal_log.info(msg)

    def warning(self, msg, *args, **kwargs):
        self.internal_log.warning(msg)

    def error(self, msg, *args, **kwargs):
        self.internal_log.error(msg)


log = Logger('logger')
