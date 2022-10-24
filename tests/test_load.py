# -*- coding: utf-8 -*-
""" Tests of load job. """
from etl_src.workers import Load


worker = Load.LoadJob()

def test_get_results_as_dict() -> None:
    worker.get_results_as_dict()
    dict_results = worker.all_data_as_dict
    
    assert "Journal of back and musculoskeletal rehabilitation" in dict_results
    
def test_extract_journal_with_most_distinct_drugs() -> None:
    worker.get_results_as_dict()
    worker.extract_journal_with_most_distinct_drugs()
    
    assert "Journal of emergency nursing" in worker.journal_max_diff_drugs_dict
    assert "Psychopharmacology" in worker.journal_max_diff_drugs_dict