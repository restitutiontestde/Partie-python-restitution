# coding=utf-8
"""Quality data functions. """
from typing import Tuple, List
import numpy as np
import pandas as pd
import json

from pyparsing import col
from etl_src.utils import utils
from etl_src.app_conf.core import etl_config


def validate_json_data(
    json_data:str
) -> bool:
    """_summary_

    Args:
        json_data (str): _description_

    Returns:
        bool: _description_
    """
    try:
        json.loads(json_data)
    except ValueError:
        return False
    
    return True

def teat_corrupted_json(
    json_data: str,
    index_invalid: int
) -> str:
    """_summary_

    Args:
        json_data (str): _description_
        index_invalid (int): _description_

    Returns:
        str: _description_
    """
    return json_data[0: index_invalid] + json_data[index_invalid+1: :]
    
def nan_treatement_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (_type_): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data_frame = data_frame.replace("", np.nan, regex=True)
    nulls_ratio = data_frame.isnull().sum()
    if sum(list(nulls_ratio)) > 0:
        list_cols_nan = [
            col for col, nan_r in nulls_ratio.to_dict().items()
            if nan_r>0 and col in etl_config.model_data_config.variables_busniss
        ]
        for col in list_cols_nan:
            data_frame = utils.add_nan_flags_for_data(data_frame, col)
            data_frame = utils.add_missing_indicator(data_frame, col)
    return data_frame


def _clean_nan_values_data(data_frame: pd.DataFrame) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    col_with_nan = [col for col in data_frame.columns if "_nan" in col]

    # json_pubmed_df = json_pubmed_df.dropna()
    for col in col_with_nan:
        data_frame = data_frame.loc[data_frame[col] == 0]
    data_frame = data_frame[
        [col for col in data_frame.columns
         if col not in col_with_nan
         ]
    ]
    return data_frame

def clean_nan_values_dataframes(
    pubmed_csv_df: pd.DataFrame,
    pubmed_json_df: pd.DataFrame,
    trials_clinical_df: pd.DataFrame
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        pubmed_csv_df (pd.DataFrame): _description_
        pubmed_json_df (pd.DataFrame): _description_
        trials_clinical_df (pd.DataFrame): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    pubmed_csv_df = _clean_nan_values_data(
        data_frame=pubmed_csv_df,
    )
    
    pubmed_json_df = _clean_nan_values_data(
        data_frame=pubmed_json_df,
    )
    
    trials_clinical_df = _clean_nan_values_data(
        data_frame=trials_clinical_df,
    )
    return pubmed_csv_df, pubmed_json_df, trials_clinical_df

def _treat_date_column_df(data_frame: pd.DataFrame, col_date:str) -> pd.DataFrame:
    data_frame[col_date] = data_frame.apply(
        lambda x: utils.map_date(x[col_date])
        if str(x[col_date]) else x[col_date],
        axis=1
    )
    return data_frame

def treat_date_columns_dataframes(
    pubmed_csv_df: pd.DataFrame,
    pubmed_json_df: pd.DataFrame,
    trials_clinical_df: pd.DataFrame,
    col_data: str
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        pubmed_csv_df (pd.DataFrame): _description_
        pubmed_json_df (pd.DataFrame): _description_
        trials_clinical_df (pd.DataFrame): _description_
        col_data (str): _description_

    Returns:
        Tupe[pd.DataFrame]: _description_
    """
    pubmed_csv_df = _treat_date_column_df(
        data_frame=pubmed_csv_df,
        col_date=col_data
    )
    
    pubmed_json_df = _treat_date_column_df(
        data_frame=pubmed_json_df,
        col_date=col_data
    )
    
    trials_clinical_df = _treat_date_column_df(
        data_frame=trials_clinical_df,
        col_date=col_data
    )
    return pubmed_csv_df, pubmed_json_df, trials_clinical_df

def _clean_text_data_col(
    data_frame: pd.DataFrame,
    col_cible: List[str]
) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (pd.DataFrame): _description_
        col_cible (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data_frame[col_cible[0]] = data_frame.apply(
        lambda x: utils.remove_special_stop_words_from_texte(
            texte_data=x[col_cible[0]]
        )
            if x[col_cible[0]] else x[col_cible[0]],
            axis=1
        
    )

    data_frame[col_cible[1]] = data_frame.apply(
        lambda x: utils.remove_special_stop_words_from_texte(
            texte_data=x[col_cible[1]]
        )
            if x[col_cible[1]] else x[col_cible[1]],
            axis=1
        
    )
    return data_frame

def clean_texte_data_all_data_frames(
    pubmed_df: pd.DataFrame,
    trials_clinical_df: pd.DataFrame,
    col_data: List[str]
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        pubmed_csv_df (pd.DataFrame): _description_
        pubmed_json_df (pd.DataFrame): _description_
        trials_clinical_df (pd.DataFrame): _description_
        col_data (List[str]): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """

    pubmed_df = _clean_text_data_col(
        data_frame=pubmed_df,
        col_cible = col_data
    )

    trials_clinical_df = _clean_text_data_col(
        data_frame=trials_clinical_df,
        col_cible = col_data
    )
    return pubmed_df, trials_clinical_df