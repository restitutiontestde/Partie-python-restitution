# -*- coding: utf-8 -*-
""" Tests of extract job. """
from etl_src.workers import Extract


worker = Extract.ExtratJob()

def test_extraction_data(sample_json_data, sample_csv_data) -> None:
    d1, _, _ = sample_csv_data
    assert len(sample_json_data) > 0
    assert len(d1) > 0

def test_highlight_missing_data_json() -> None:    

    worker.highlight_missing_data()
    assert  "journal_nan" in worker.clinical_trials_df.columns 
    
def test_clean_data() -> None:
    worker.highlight_missing_data()
    worker.clean_data()
    list_null_ratio = list(worker.clinical_trials_df.isnull().sum())
    assert sum(list_null_ratio) == 0
    
    