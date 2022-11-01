# coding=utf-8
""" Mapper data """
from typing import List, Tuple
import pandas as pd
import numpy as np
from etl_src.utils import utils
from etl_src.app_conf.core import etl_config
from itertools import chain


def rename_col_for_data_frame(data_frame: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    """
    return data_frame.rename(
        columns=etl_config.model_data_config.variables_to_rename
    )

def _match_drug_per_data_frame(
    data_frame: pd.DataFrame,
    list_drugs: List,
    col_drug: str
) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (pd.DataFrame): _description_
        list_drugs (List): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data_frame[col_drug] = data_frame.apply(
        lambda x: utils.match_drug_title(
            title=x["title"],
            list_drugs=list_drugs
        ),
        axis=1
    )
    return data_frame

def match_drug_per_dataframes(
    pubmed_df: pd.DataFrame,
    clinical_trials_df: pd.DataFrame,
    list_drugs: str
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        pubmed_df (pd.DataFrame): _description_
        clinical_trials_df (pd.DataFrame): _description_
        list_drugs (str): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    pubmed_df = _match_drug_per_data_frame(
        data_frame=pubmed_df,
        list_drugs=list_drugs,
        col_drug="drug"
    )
    
    clinical_trials_df = _match_drug_per_data_frame(
        data_frame=clinical_trials_df,
        list_drugs=list_drugs,
        col_drug="drug"
    )
    return pubmed_df, clinical_trials_df

def _duplicate_rows_according_to_drugs(
    data_frame: pd.DataFrame, 
    col_cible: str
) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    
    cols = [col for col in data_frame.columns if col != col_cible]
    dict_duplicated_df = {
        col: np.repeat(data_frame[col].values, data_frame[col_cible].str.len())
        for col in cols
    }
    dict_duplicated_df[col_cible] = list(chain.from_iterable(data_frame[col_cible]))
    return pd.DataFrame(
        dict_duplicated_df
    )

def duplicate_rows_drugs_for_dataframes(
    pubmed_df: pd.DataFrame,
    trial_clinical_df: pd.DataFrame,
    col_cible: str
) -> Tuple[pd.DataFrame]:
    """_summary_

    Args:
        pubmed_df (pd.DataFrame): _description_
        trial_clinical_df (pd.DataFrame): _description_
        col_cible (str): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    pubmed_df = _duplicate_rows_according_to_drugs(
        data_frame=pubmed_df,
        col_cible=col_cible
    )
    trial_clinical_df = _duplicate_rows_according_to_drugs(
        data_frame=trial_clinical_df,
        col_cible=col_cible
    )
    return pubmed_df, trial_clinical_df