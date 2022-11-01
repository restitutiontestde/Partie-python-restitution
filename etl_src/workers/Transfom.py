# coding=utf-8
""" Transform step (second step) of the ETL. """
import pandas as pd
from etl_src.app_conf.core import etl_config, METIER_DATA, CLEAN_DATA
from etl_src.utils import utils
from etl_src.services import local_data_collector, mapper_data, data_quality


class TransformJob:
    """Class Transform Job"""
    def __init__(self) -> None:
        """_summary_

        Args:

        """
        self.clean_pubmed_csv, self.clean_pubmed_json, self.clean_clinical_trials\
        = local_data_collector.get_dataframes_per_dir(
            dir=CLEAN_DATA
        )
        
        self.all_pub_med = pd.concat([self.clean_pubmed_csv, self.clean_pubmed_json])
        #self.clean_clinical_trials = clean_clinical_trials
        self.drug = local_data_collector.get_drug_data_as_data_frame()
        self.list_drugs = list(self.drug["drug"].unique())
        self.all_data = pd.DataFrame()
     
    
    def rename_col_title_clinical_tirals_df(self) -> None:
        """_summary_
        """
        self.clean_clinical_trials = mapper_data.rename_col_for_data_frame(
            data_frame=self.clean_clinical_trials
        )
    
    def add_type_column(self) -> None:
        """_summary_
        """
        self.clean_clinical_trials[
            etl_config.model_data_config.variable_to_add
        ] = 'clinical_trial'
        
        self.all_pub_med[
            etl_config.model_data_config.variable_to_add
        ] = "article"
    
    def clean_text_data(self) -> None:
        """_summary_
        """
        self.all_data, self.clean_clinical_trials = data_quality.clean_texte_data_all_data_frames(
            pubmed_df=self.all_pub_med,
            trials_clinical_df=self.clean_clinical_trials,
            col_data=["title", "journal"]
        )
    
    def match_drug_with_articles(self):
        """_summary_
        """
        self.all_pub_med, self.clean_clinical_trials = mapper_data.match_drug_per_dataframes(
            pubmed_df=self.all_pub_med,
            clinical_trials_df=self.clean_clinical_trials,
            list_drugs=self.list_drugs
        )
    
    def treate_list_values_drugs(self):
        """_summary_
        """
        self.all_pub_med, self.clean_clinical_trials = mapper_data.duplicate_rows_drugs_for_dataframes(
            pubmed_df=self.all_pub_med,
            trial_clinical_df=self.clean_clinical_trials,
            col_cible="drug"
        )
        self.all_data = pd.concat([self.all_pub_med, self.clean_clinical_trials])
        
    def seralize_data_for_field_experts(self):
        """_summary_
        """
        utils.serialize_dataframe_as_csv(
            data_frame=self.all_pub_med,
            pth_file=METIER_DATA / etl_config.files_input_data_config.pubmed_csv.replace(".csv", "_all.csv")
        )
        utils.serialize_dataframe_as_csv(
            data_frame=self.clean_clinical_trials,
            pth_file=METIER_DATA / etl_config.files_input_data_config.clinical_trials_csv
        )
        utils.serialize_dataframe_as_csv(
            data_frame=self.all_data,
            pth_file=METIER_DATA / etl_config.files_input_data_config.all_data
        )

    def run_worker(self) -> None:
        """ Run worker. """
        self.rename_col_title_clinical_tirals_df()
        self.add_type_column()
        self.clean_text_data()
        self.match_drug_with_articles()
        self.treate_list_values_drugs()
        self.seralize_data_for_field_experts()

        