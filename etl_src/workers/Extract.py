# coding=utf-8
""" Extract step (first step) of the ETL. """
from typing import Tuple
import pandas as pd
from etl_src.services import local_data_collector, data_quality
from etl_src.configs.core import etl_config, NAN_DATA, CLEAN_DATA
from etl_src.utils import utils


class ExtratJob:
    """Class of Extraction JOB. """
    def __init__(self) -> None:
        """_summary_
        """
        self.clinical_trials_df, self.drungs, self.pubmed_csv_df = \
            local_data_collector.collect_csv_data_local()
        self.pubmed_json_df = local_data_collector.collect_json_data_local()

    def highlight_missing_data(self) -> None:
        """_summary_
        """
        # treat nan values
        self.clinical_trials_df = data_quality.nan_treatement_data(
            data_frame=self.clinical_trials_df
        )
        self.pubmed_csv_df = data_quality.nan_treatement_data(
            data_frame=self.pubmed_csv_df
        )
        self.pubmed_json_df = data_quality.nan_treatement_data(
            data_frame=self.pubmed_json_df
        )

        # save data
        utils.serialize_all_dataframes(
            pubmed_csv_df=self.pubmed_csv_df,
            path_1=NAN_DATA / etl_config.files_input_data_config.pubmed_csv,
            pubmed_json_df=self.pubmed_json_df,
            path_2=NAN_DATA / etl_config.files_input_data_config.pubmed_json.replace(".json", "_json.csv"),
            trials_clinical_df=self.clinical_trials_df,
            path_3=NAN_DATA / etl_config.files_input_data_config.clinical_trials_csv
        )


    def clean_data(self) -> Tuple[pd.DataFrame]:
        """
            Clean nan values data 
            Clean date data.
        """
        # clean nan values
        self.pubmed_csv_df, self.pubmed_json_df, self.clinical_trials_df = data_quality.clean_nan_values_dataframes(
            pubmed_csv_df=self.pubmed_csv_df,
            pubmed_json_df=self.pubmed_json_df,
            trials_clinical_df=self.clinical_trials_df,
        )
         # clean date data
        self.pubmed_csv_df, \
        self.pubmed_json_df, \
        self.trials_clinical_df = data_quality.treat_date_columns_dataframes(
            pubmed_csv_df=self.pubmed_csv_df,
            pubmed_json_df=self.pubmed_json_df,
            trials_clinical_df=self.clinical_trials_df,
            col_data="date"
        )
        # save data
        utils.serialize_all_dataframes(
            pubmed_csv_df=self.pubmed_csv_df,
            path_1=CLEAN_DATA / etl_config.files_input_data_config.pubmed_csv,
            pubmed_json_df=self.pubmed_json_df,
            path_2=CLEAN_DATA / etl_config.files_input_data_config.pubmed_json.replace(".json", "_json.csv"),
            trials_clinical_df=self.clinical_trials_df,
            path_3=CLEAN_DATA / etl_config.files_input_data_config.clinical_trials_csv
        )
        
    def run_worker(self) -> None:
        """Run operations worker. """
        # mettre en évidance les nans values 
        self.highlight_missing_data()
        self.clean_data()