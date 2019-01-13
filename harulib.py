import logging
import yaml

VERSION = 1

class YAML_Provider(object):

    def __init__(self, path):
        self.logger = Log(name='YAML Provider')
        self._path = path
        self.data = {}
        self.load()

    def load(self):
        """Loading data from self.data"""
        try:
            self.data = yaml.load(open(self._path, 'r'))
            self.logger.debug("Loaded load()")
        except Exception as e:
            self.logger.debug(f"Exception in load(), calling save(). Exception: {e}")
        self.logger.debug("Return data")
        return self.data

    def save(self, data=None):
        """Save data to file from data"""
        if data:
            self.data = data
        yaml.dump(self.data, open(self._path, 'w'))
        self.logger.debug("Data saved!")

class Log:
    """Some logger for lib."""

    def __init__(self, name='bot', level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        Formatter = logging.Formatter('%(levelname)s [%(asctime)s] %(name)s : %(message)s')
        # Adding filehandler
        fh = logging.FileHandler('log.txt', 'a')
        self.logger.addHandler(fh)
        fh.setFormatter(Formatter)
        # Adding Streamhandler
        sh = logging.StreamHandler()
        self.logger.addHandler(sh)
        sh.setFormatter(Formatter)

    def debug(self, *message):
        self.logger.debug(" ".join(message))

    def info(self, *message):
        self.logger.info(" ".join(message))

    def warning(self, *message):
        self.logger.warning(" ".join(message))

    def error(self, *message):
        self.logger.error(" ".join(message))