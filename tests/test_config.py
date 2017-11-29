"""validate prosper.datareader.config general functions"""
import re

import pytest
import pandas as pd
import numpy

import prosper.datareader.config as config

def test_listify():
    """validate expected behavior for _listify()"""
    demo_data = {
        'key1': {
            'val1': 1,
            'val2': 2
        },
        'key2': {
            'val1': 10,
            'val2': 20
        }
    }
    fixed_data = config._listify(demo_data, 'key')
    assert isinstance(fixed_data, list)
    expected_keys = ['val1', 'val2', 'key']
    expected_keys.sort()
    for row in fixed_data:
        keys = list(row.keys())
        keys.sort()
        assert keys == expected_keys


def test_ticker_list_to_str():
    """make sure ticker_list_to_str returns as expected"""
    no_caps_pattern = re.compile('[a-z]+')

    single_stock = config._list_to_str('MU')
    assert not no_caps_pattern.match(single_stock)
    assert single_stock == 'MU'

    lower_stock = config._list_to_str('mu')
    assert not no_caps_pattern.match(lower_stock)
    assert lower_stock == 'MU'

    multi_stock = config._list_to_str(['MU', 'INTC', 'BA'])
    assert not no_caps_pattern.match(multi_stock)
    assert multi_stock == 'MU,INTC,BA'

    lower_multi_stock = config._list_to_str(['MU', 'intc', 'BA'])
    assert not no_caps_pattern.match(lower_multi_stock)
    assert lower_multi_stock == 'MU,INTC,BA'

    with pytest.raises(TypeError):
        bad_stock = config._list_to_str({'butts':1})

def test_cast_str_to_int():
    """validate behavior for cast_str_to_int"""
    demo_json = [
        {
            "string_value": "butts",
            "int_value": "12",
            "float_value": "10.50"
        },
        {
            "string_value": "otherbutts",
            "int_value": "-99",
            "float_value": "-5.00"
        }
    ]

    demo_df = pd.DataFrame(demo_json)
    assert demo_df['string_value'].dtype == object
    assert demo_df['int_value'].dtype == object
    assert demo_df['float_value'].dtype == object

    with pytest.raises(TypeError):
        demo_df['diff'] = demo_df['int_value'] - demo_df['float_value']

    updated_df = config._cast_str_to_int(demo_df)

    assert updated_df['string_value'].dtype == object
    assert updated_df['int_value'].dtype == numpy.int64
    assert updated_df['float_value'].dtype == numpy.float64

    updated_df['diff'] = updated_df['int_value'] - updated_df['float_value']
    assert updated_df['diff'].dtype == numpy.float64
