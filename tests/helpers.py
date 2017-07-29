"""helpers.py: common utilities for tests"""
import json
from os import path

import jsonschema

import prosper.common.prosper_config as p_config

HERE = path.abspath(path.dirname(__file__))
CONFIG_PATH = path.join(HERE, 'test_config.cfg')

CONFIG = p_config.ProsperConfig(CONFIG_PATH)

def validate_schema(
        test_dict,
        path_to_schema,
        schema_basepath=path.join(HERE, 'schemas')
):
    """check if schema is OK

    Args:
        test_dict (:obj:`dict`): object to test
        path_to_schema (str): expected path to .schema file
        schema_basepath (str, optional): path to schema collection

    Returns:
        None: raise if issue

    """
    schema_fullpath = path.join(schema_basepath, path_to_schema)

    if not path.isfile(schema_fullpath):
        print(schema_fullpath)
        raise FileNotFoundError

    with open(schema_fullpath, 'r') as schema_fh:
        schema = json.load(schema_fh)

    jsonschema.validate(test_dict, schema)
