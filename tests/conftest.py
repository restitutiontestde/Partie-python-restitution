# -*- coding: utf-8 -*-
"""Define fixtures for static data used by tests. """
import pytest
from etl_src.services import local_data_collector
from etl_src.app_conf import core 


@pytest.fixture()
def sample_csv_data():
    return local_data_collector.collect_csv_data_local()

@pytest.fixture()
def sample_json_data():
    return local_data_collector.collect_json_data_local()

@pytest.fixture()
def sample_parsed_config():
    return core.parse_config_from_yml_file()

