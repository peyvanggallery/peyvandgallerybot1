import json
import os.path

class Configuration:

    def __init__(self, configuration_file="config.json"):
        self.__configuration_file = configuration_file
        self.configuration = {}
        # If the config file exists, load it.
        if os.path.isfile(configuration_file):
            self.load()

    def load(self):
        with open(self.__configuration_file, "r") as config:
            self.configuration = json.load(config)
        config.close()

    def save(self):
        with open(self.__configuration_file, "w") as config:
            json.dump(self.configuration, config, indent=4, sort_keys=True)
        config.close()
