# -*- coding: utf-8 -*-

"""App configuration (typing + config parser)."""

from pathlib import Path
from typing import Dict, List
from strictyaml import YAML, load
from pydantic import BaseModel


ROOT = Path(__file__).resolve().parent.parent.parent
# chemin vers le répertoire contenant les scripts 
# de l'ETL (classes, modules, objets et congigs)
ETL_SRC = ROOT / "etl_src"
# chemin le dossier contenant le fichier config du projet (ETL)
CONFIG_DIR = ETL_SRC / "config"
# chemin vers le fichier config du projet
PATH_CONFIG_FILE = CONFIG_DIR / "dev.yml"
# chemin vers le répértoire qui contient les dossiers
# qui tracent la vie des données au cours de l'ETL
DATASET_DIR = ETL_SRC / "datasets"
# état des données à etape 1 du cycle de vie ETL (Raw data)
RAW_DATA = DATASET_DIR / "Raw_data"
CSV_DATA_DIR = RAW_DATA / "csv_data"
JSON_DATA_DIR = RAW_DATA / "json_data"
# état des données à etape 2 du cycle de vie ETL (les nan values)
NAN_DATA = DATASET_DIR / "Nan_data"
# état des données à etape 3 du cycle de vie ETL (après nétoyage)
CLEAN_DATA = DATASET_DIR / "Clean_data"
# état des données à etape 3 du cycle de vie ETL (exploitable par le métier)
METIER_DATA =  DATASET_DIR / "Metier_data"
# Résultat de l'ETL (json format)
RESULTS_DIR = ETL_SRC / "results"

    
class FilesInputDataConfig(BaseModel):
    """classe représentant les configs liées aux
     fichiers données d'entrée.

    Args:
        BaseModel (_type_): hérite de la base BaseModel
                             de pydantic
    """
    clinical_trials_csv: str
    drugs_csv: str
    pubmed_csv: str
    pubmed_json: str
    all_data: str
    final_results: str
    resutls_jounral_max_diff_drugs: str


class ModelDataConfig(BaseModel):
    """class des configurations liées
    aux meta-données des nos tables.

    Args:
        BaseModel (_type_): hérite de la base BaseModel
                             de pydantic
    """
    variables_to_rename: Dict
    all_varibales: List[str]
    variables_busniss: List[str]
    variable_to_add: str


class EtlConfig(BaseModel):
    """Master class des toutes les configurations
    ETL configution typing
    """
    
    files_input_data_config: FilesInputDataConfig
    model_data_config: ModelDataConfig

def get_config_file() -> Path:
    """fonction qui vérifie sir le config file existe.
    La localisation du config file est définie comme constante.

    Returns:
        PATH_CONFIG_FILE: constante de type Path, emplacement du fichier config
            ou une exception liée au path_config
    """
    if PATH_CONFIG_FILE.is_file():
        return PATH_CONFIG_FILE
    raise Exception(f"Config not found at {PATH_CONFIG_FILE!r}")


def parse_config_from_yml_file(
    conig_path: Path=None
) -> YAML:
    """ lire le fichier config et le parser via le package strictyaml.


    Args:
        conig_path (Path, optional): en args ou depuis 
        la fonction get_config_file. 
        Defaults to None.

    Raises:
        OSError: si aucun fichier config n'existe on aura un OSERROR

    Returns:
        YAML: le yaml au format parsé pour réccupérer les données.
    """    
    if not conig_path:
        conig_path = get_config_file()
    
    if conig_path:
        with open(conig_path, "r") as config_file:
            parsed_config = load(config_file.read())
            return parsed_config
    raise OSError(
        f"Check you CONFIG directory, did not find config file path:{conig_path}"
        )

def create_and_validate_etl_config(
    parsed_config: YAML=None
) -> EtlConfig:
    """retourne un objet de class EtlConfig, 
        qui contient toutes les configurations du projet.

    Args:
        parsed_config (YAML, optional): le YAML après parsing du fihcier.
        Defaults to None.

    Returns:
        _etl_config : de tyoe EtlConfig, toutes les configuration de l'ETL
    """
    
    if parsed_config is None:
        parsed_config = parse_config_from_yml_file()

    _etl_config = EtlConfig(
        files_input_data_config=FilesInputDataConfig(**parsed_config.data),
        model_data_config=ModelDataConfig(**parsed_config.data)
    )
    return _etl_config

# get etl_config
etl_config = create_and_validate_etl_config()

