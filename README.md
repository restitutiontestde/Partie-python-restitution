
# healthcare paper analysis-ETL
Implémentation d'un ETL pour estimer les citations des médicaments 
dans les journaux scientifiques.

# Documentation
healthcare paper analysis-ETL procède en trois étapes : 
### Extraction des données : 
Deux formats de données en entrée : csv et json
### Transformation de données : 
Utilisation des fonctions de matching pour identifier les citations
des médicaments dans les jouneux
### Chargement des résultats : 
Les résultats de données sont enregistrés sous format json.


# Etapes d'installation du projet
    1. cloner ce repository : 
        git clone https://github.com/restitutiontestde/Partie-python-restitution.git
    2. Créer un environnement virtuel :
        - avec conda : 
                conda create -n env_o_b python=3.7
                conda activate env_o_b
        - avec venv (ubuntu): 
                python3 -m venv env_o_b
                source env_o_b/bin/activate
    3. Installer les dépendences :
        pip install -r requirements.txt
    4. Excuter le projet :
        python run_etl.py
    5. Executer les tests : 
        pytest
