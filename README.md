
## FAQ

#### Question 1 : Le travail à réaliser

L’architecture du code a été réalisé de la manière plus généraliste possible en perspectives d’évolution, elle est constituée de 3 éléments essentiels :

- etl_src : contient les sources (workers + services) requis pour lancer notre pipeline
    - config : contient le fichier « dev.yml » reportant les configurations de notre pipeline.
    - app_conf : core.py est chargé de parser le fichier config du projet pour extraire les informations de notre pipeline
    - datasets : les données de notre pipeline à diverses étapes depuis RAW jusqu’au format METIER
    - results : les résultat attendu pour le projet sous format de json
    - services : les modules permettant de réaliser les opération de l’ETL ; lecture de données, transformation de données, et enregistrement des résultats.
    - utils : les fonctions requises pour assister les modules de « services »
    - worksers : on a 3 workers : Extract, Transform et Load qui utilisent les services pour dérouler notre pipeline.
- requirements.txt : les dépendances du projet
- tests :  contient les tests unitaires de toutes fonctions utilisées dans nos « workers » 

#### Question 2 : Orchestrateur de type airflow

La migration de ce projet vers un vesion avec l'orchestrateur
airflow a été réalisé dans le projet suivant : 

La migration a pris 5 minutes en vue de la générecité du code. 
J'ai ajouté le répertoire etl_src dans le folder dags et
construit le dag en me basant sur les workers du etl_src.

#### Question 3 : Data pipeline 

L’objectif du pipeline est de générer un JSON représentant le graphe 
relationnel entre les papier scientifique (articles et essaies cliniques), 
les journaux et le médicament.
J’ai opté pour une représentation en escalier en imaginant une perspective BI. 
On part du niveau le plus généraliste (journal qui contient plusieurs articles) 
au niveau le plus fin (médicament). De cette manière on peut réaliser diverses 
restitutions et KPI par journal, article ou essai clinique en rapport 
avec les médicaments.


#### Question 4 : Resultat du pipeline

La restitution des résultats de notre pipeline est enregistrée dans :

Restitution_python_test_de\etl_src\results\final_results.json

La restituion du journal qui mentionne le plus de médicaments différents
est enregistrée dans : 
Restitution_python_test_de\etl_src\results\journal_with_max_diff_drugs.json


