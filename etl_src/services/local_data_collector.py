# coding=utf-8
""" Service that collects raw data from local CSV and json files"""
from typing import Tuple
import os
from pathlib import Path
from etl_src.app_conf.core import CSV_DATA_DIR, JSON_DATA_DIR, METIER_DATA
from etl_src.app_conf.core import etl_config
from etl_src.utils import utils
from etl_src.services import data_quality
import pandas as pd 



def collect_csv_data_local() -> Tuple[pd.DataFrame]:
    """_summary_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    # clinical trials file
    file_name = etl_config.files_input_data_config.clinical_trials_csv
    path_csv_clinical_trials = CSV_DATA_DIR / file_name 
    clinical_trials_df = pd.read_csv(
        path_csv_clinical_trials,
        sep=",",
        encoding='UTF-8'
    )
    
    # drug file
    file_name = etl_config.files_input_data_config.drugs_csv
    path_csv_drugs = CSV_DATA_DIR / file_name
    drugs_df = pd.read_csv(path_csv_drugs, sep=",", encoding="UTF-8")
    
    # pubmed file
    file_name = etl_config.files_input_data_config.pubmed_csv
    path_pubmed_csv = CSV_DATA_DIR / file_name
    pubmed_df = pd.read_csv(path_pubmed_csv, sep=",", encoding="UTF-8")
    
    return clinical_trials_df, drugs_df, pubmed_df


def collect_json_data_local() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    file_name = etl_config.files_input_data_config.pubmed_json
    path_json_pubmed = JSON_DATA_DIR / file_name
    with open(path_json_pubmed, "r") as json_file:
        json_data = json_file.read()
    
    if not data_quality.validate_json_data(json_data=json_data):
        json_data = data_quality.teat_corrupted_json(
            json_data=json_data,
            index_invalid=len(json_data)-3
        )
    
    
    return utils.get_data_frame_from_json_data(
        json_data=json_data
    )

def get_drug_data_as_data_frame() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    return pd.read_csv(
        CSV_DATA_DIR / etl_config.files_input_data_config.drugs_csv,
        sep=",",
        encoding='UTF-8'
    )


def get_dataframes_per_dir(
    dir: Path
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        dir (Path): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    list_files = dir.glob('**/*')
    pubmed_csv_df = pd.DataFrame()
    pubmed_json_df = pd.DataFrame()
    clinical_trials_df = pd.DataFrame()
    for file_name in list_files:
        name = str(file_name)
        if "clinical" in str(name):
            clinical_trials_df =  pd.read_csv(
                name,
                sep=";"
            )
        elif "pubmed.csv" in str(name):
            pubmed_csv_df = pd.read_csv(
                name,
                sep=";"
            )
        else:
            pubmed_json_df = pd.read_csv(
                name,
                sep=";"
            )
    return pubmed_csv_df, pubmed_json_df, clinical_trials_df

def get_all_data_as_dataframe() -> pd.DataFrame:
    """_summary_

    Returns:
        pd.DataFrame: _description_
    """
    return pd.read_csv(
        METIER_DATA / etl_config.files_input_data_config.all_data,
        sep=";"
    )