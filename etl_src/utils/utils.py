# coding=utf-8
"""Useful functions to support ETL opérations. """
from pathlib import Path
from typing import List, Tuple
import calendar
import datetime
import re
import json
import pandas as pd 
import numpy as np
from etl_src.configs.core import etl_config, NAN_DATA



dict_month_index = dict((month.lower(), index) for index, month in enumerate(calendar.month_abbr) if month)
stop_words = [r"\xc3\x28", r"\xc3\xb1"]

def get_data_frame_from_json_data(json_data: str) -> pd.DataFrame:
    """_summary_

    Args:
        json_path (Path): _description_

    Returns:
        Path: _description_
    """
    loaded_json = json.loads(json_data)
  
    
    return pd.DataFrame(loaded_json)

def add_nan_flags_for_data(data_frame: pd.DataFrame, col: str) -> pd.DataFrame:
    """_summary_

    Args:
        data_frame (_type_): _description_
        col (_type_): _description_

    Returns:
        pd.DataFrame: _description_
    """
    data_frame[col].replace("", np.nan)
    return data_frame


def add_missing_indicator(data_frame: pd.DataFrame, col:str) -> pd.DataFrame:
    """
    Pour chaque varibales qui contient des Nan values 
    on ajoute un indicateur de valeurs manquante
    pour une colonne donnée la valeur retourne 1 si nan value
    sinon 0, pour ce faire on a utilisé np.where. 

    Args:
        data_frame : dataframe en etrée
        col (_type_): colonne à checker

    Returns:
        pd.DataFrame: _description_
    """
    data_frame[col+"_nan"] = np.where(data_frame[col].isnull(), 1, 0)
    return data_frame


def serialize_dataframe_as_csv(
    data_frame: pd.DataFrame,
    pth_file: Path
    ) -> None:
    """_summary_

    Args:
        data_frame (_type_): _description_
        pth_file (_type_): _description_
    """
    data_frame.to_csv(
        pth_file,
        sep=";",
        index=False
    )

def serialize_all_dataframes(
    pubmed_csv_df: pd.DataFrame,
    path_1: Path,
    pubmed_json_df: pd.DataFrame,
    path_2: Path,
    trials_clinical_df: pd.DataFrame,
    path_3: Path
) -> None:
    """_summary_

    Args:
        pubmed_csv_df (pd.DataFrame): _description_
        pubmed_json_df (pd.DataFrame): _description_
        trials_clinical_df (pd.DataFrame): _description_

    Returns:
        Tuple[pd.DataFrame]: _description_
    """
    serialize_dataframe_as_csv(
        data_frame=pubmed_csv_df,
        pth_file=path_1
    )
    serialize_dataframe_as_csv(
        data_frame=pubmed_json_df,
        pth_file=path_2
    )
    serialize_dataframe_as_csv(
        data_frame=trials_clinical_df,
        pth_file=path_3
    )

def map_date(date_val):
    pattern = re.compile(r'(\d+/\d+/\d+)')
    if pattern.match(date_val):
        return date_val.replace("/", "-")
    else:
        split_date = date_val.split(" ")
        if len(split_date) == 3:
            month = split_date[1][0:3].lower()
            if month in dict_month_index:
                split_date[1] = str(dict_month_index[month])
                return "-".join(split_date)
    return date_val

def match_drug_title(
    title: str,
    list_drugs: List
) -> List:
    """_summary_

    Args:
        title (str): _description_
        list_drug (List): _description_

    Returns:
        str: _description_
    """
    return list(
        set(title.lower().split(" ")).intersection(
            set([drug.lower() for drug in list_drugs])
        )
    )
    
def remove_special_stop_words_from_texte(texte_data: str) -> str:
    """_summary_

    Args:
        texte_data (_type_): _description_

    Returns:
        str: _description_
    """
    for elm in stop_words: 
        texte_data = texte_data.replace(elm, "")

    return texte_data