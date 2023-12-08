import json

import pytest
from network_live.beeline.huawei.lte import parse_lte_cms

xmls_path = 'tests/fixtures/beeline/huawei/xml/'

with open('tests/fixtures/physical_parameters.json', 'r') as physical_params_file:
    physical_params = json.load(physical_params_file)

json_results = {
    'moran': 'tests/fixtures/beeline/huawei/results/lte_moran.json',
    'mocn': 'tests/fixtures/beeline/huawei/results/lte_mocn.json',
}


def sort_list_of_dicts(data):
    return sorted(data, key=lambda item: item['cell_name'])


@pytest.mark.parametrize('sharing_type', ['moran', 'mocn'])
def test_parse_lte_cms(sharing_type):
    with open(json_results[sharing_type], 'r') as json_result:
        expected = json.load(json_result)
    lte_cells = parse_lte_cms(xmls_path, sharing_type, physical_params)

    assert sort_list_of_dicts(lte_cells) == sort_list_of_dicts(expected)


def test_parse_lte_cms_empty():
    xmls_path = 'tests/fixtures/empty_folder'
    physical_params = {}
    expected = []

    lte_cells = parse_lte_cms(xmls_path, 'moran', physical_params)

    assert lte_cells == expected
