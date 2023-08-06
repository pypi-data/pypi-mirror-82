import os
import yaml
from easydict import EasyDict

def get_config(config_file):
    assert(os.path.isfile(config_file))
    with open(config_file, 'r') as cf:
        parsed_yaml = yaml.load(
            cf,
            Loader=yaml.FullLoader
        )
    return EasyDict(parsed_yaml)


def merge_configs(config_list):
    assert(len(config_list) > 0)
    merged_config = {}
    for cl in config_list:
        merged_config.update(cl)
    return EasyDict(merged_config)
