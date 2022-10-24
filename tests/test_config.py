# -*- coding: utf-8 -*-
"""Test config core functions. """
from etl_src.configs.core import create_and_validate_etl_config

def test_parse_config_from_yml_file(sample_parsed_config):
    """_summary_
    """
    etl_conf = create_and_validate_etl_config(
        parsed_config=sample_parsed_config
    )
    assert etl_conf.files_input_data_config.clinical_trials_csv == "clinical_trials.csv"
    assert etl_conf.model_data_config.all_varibales == ["id", "title", "date", "journal"]