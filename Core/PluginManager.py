import json
import os
import importlib


class Plugin:
    def __init__(self, directory):
        self.path = os.path.join(os.path.dirname(__file__), "..", "Plugins", directory)
        with open(os.path.join(self.path, "plugin.json"), "r") as f:
            data = json.load(f)
        self.directory = directory
        self.name = data["name"]
        self.description = data["description"]
        self.version = data["version"]
        self.module = importlib.import_module("Plugins."+directory+"."+data["main_file"])
        self.instance = self.module.instance


class PluginManager:
    def __init__(self, factory, plugins):
        self.factory = factory
        self.plugins = [Plugin(i) for i in plugins]
        self.factory.logger.info("Plugin loaded : {}".format(", ".join([i.name for i in self.plugins])))

    def call(self, function, *args):
        for i in self.plugins:
            if hasattr(i.instance, function):
                fnc = getattr(i.instance, function)
                fnc(*args)

