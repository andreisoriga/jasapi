import yaml

from flask import Flask as BaseFlask, Config as BaseConfig


class Config(BaseConfig):
    """Flask config enhanced with a `from_yaml` method."""

    def from_yaml(self, config_file, env):
        self['ENVIRONMENT'] = env.lower()

        with open(config_file, 'rt') as f:
            c = yaml.load(f.read())

        c = c.get(env, c)

        for key in c.keys():
            if key.isupper():
                self[key] = c[key]


class Flask(BaseFlask):
    """Extended version of `Flask` that implements custom config class"""

    def make_config(self, instance_relative=False):
        root_path = self.root_path
        if instance_relative:
            root_path = self.instance_path
        return Config(root_path, self.default_config)
