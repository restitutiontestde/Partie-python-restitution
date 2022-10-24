""" Tests of transform job. """
from etl_src.workers import Transfom


worker = Transfom.TransformJob()

def test_rename_col_title_clinical_tirals_df() -> None:
    assert "scientific_title" in worker.clean_clinical_trials.columns
    worker.rename_col_title_clinical_tirals_df()
    assert "scientific_title" not in  worker.clean_clinical_trials.columns
    assert "title" in worker.clean_clinical_trials.columns
    
def test_add_column():
    assert "type" not in worker.clean_clinical_trials.columns
    worker.add_type_column()
    assert "type" in worker.clean_clinical_trials
    assert "clinical_trial" in worker.clean_clinical_trials["type"].unique()
    
def test_clean_texte_data():
    df_loc = worker.clean_clinical_trials.loc[
        worker.clean_clinical_trials["id"] == "NCT04153396"
        ]
    assert r"\xc3\xb1" in df_loc["title"].iat[0]
    
    worker.clean_text_data()
    df_loc = worker.clean_clinical_trials.loc[
        worker.clean_clinical_trials["id"] == "NCT04153396"
        ]
    assert r"\xc3\xb1" not in df_loc["title"].iat[0]  
    
def test_match_drug_with_articles() -> None:
    assert "drug" not in worker.clean_clinical_trials.columns
    worker.match_drug_with_articles()
    df_loc = worker.clean_clinical_trials.loc[
        worker.clean_clinical_trials["id"] == "NCT01967433"
    ]
    assert df_loc["drug"].iat[0] == ["diphenhydramine"]
    
