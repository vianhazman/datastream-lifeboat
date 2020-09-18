import os

import yaml


def parse_config(job):
    config = {}
    path = os.path.dirname(os.path.abspath(__file__)) + "/../configs/" + job + ".yaml"
    with open(path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
        return config
