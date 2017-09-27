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

def get_sample_json(
        filename,
        sample_basepath=path.join(HERE, 'samples')
):
    """fetch sample JSON for parsers/pretty testing

    Args:
        filename (str): name of sample file
        sample_basepath (str, optional): path to sample collection

    Returns:
        (:obj:`dict`): processed JSON

    """
    sample_fullpath = path.join(sample_basepath, filename)

    if not path.isfile(sample_fullpath):
        print(sample_fullpath)
        raise FileNotFoundError

    with open(sample_fullpath, 'r') as json_fh:
        data = json.load(json_fh)

    return data

def dump_debug(
        data,
        filename='debug_data.json',
        dump_path=HERE
):
    """used for object dumping for debug help

    Args:
        data (:obj:`dict`): JSON serializable data
        filename (str, optional): name of file to dump to
        dump_path (str, optional): path to dump file to

    Returns:
        None

    """
    with open(path.join(dump_path, filename), 'w') as dump_fh:
        json.dump(data, dump_fh, indent=4)

def find_uniques(
        test_list,
        expected_list
):
    """checks for unique values between two lists.

    Args:
        test_list (:obj:`list`): values found in test
        expected_list (:obj:`list`): values expected

    Returns:
        (:obj:`list`): unique_test
        (:obj:`list`): unique_expected

    """
    unique_test = list(set(test_list) - set(expected_list))
    print('Unique test vals: {}'.format(unique_test))

    #unique_expected = list(expected_list)
    #for key in test_list:
    #    try:
    #        unique_expected.remove(key)
    #        print('removed key: {}'.format(key))
    #    except Exception:
    #        print('key not in expected: {}'.format(key))
    #        pass
    #print(unique_expected)
    unique_expected = list(set(expected_list) - set(test_list))
    print('Unique expected vals: {}'.format(unique_expected))

    return unique_test, unique_expected
