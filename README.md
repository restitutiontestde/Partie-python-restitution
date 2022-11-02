

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

#### Question 6 : Aller plus loin
Pour répondre à cette question je pose deux hypothèses de départ :

- Hypothèse 1 : le traitement requis pour ce projet est un traitement dit « en batch » , le cas streaming n’est pas pris en considération dans cette réponse.

- Hypothèse 2 : la proposition cloud de la réponse prendra en considération les services du cloud GCP et non pas un autre cloud provider (AZURE, AWS ou IBM).

 

Pour faire évoluer le projet (code restitué) vers une perspective Big data nous devons considérer deux modifications majeures à savoir :

1. Stockage des donnés : Dans un contexte Big data on doit choisir un format de stckage adapté à cette quantité. AVRO ; utilisant json pour les méta-datas (schéma et data types) et une sérialisation au format binaire pour enregistrer les données.
- En onpremise : Les modifications à apporter au script sont comme suit : la classe Extract (contenue dans le directory Workers) devra faire appel un service missionné pour lire/manipuler les fichier de type AVRO. De ce fait dans le répertoire Services du code on ajoute un module dédié aux fonctions qui manipulent le format AVRO.
  De cette manière l’orchestration Airflow ne sera pas touché car elle fait appel à la fonction de la classe Extract (après instanciation).

- En cloud GCP : les fichier AVRO peuvent être déposés sur le storage GCS, et on poura utiliser soit un trigger via pubSub ou bien un operator Sensor d’Airflow pour enlencher le process extract du pipeline.
 

2. Traitement des données :
- En onpremise : un traitement distribué basé sur l’architecture de SPARK (via python, sql ou scala) est recommandé pour les données de grande dimension. De plus Airflow dispose du SparkSubmitOperator pour orchestrer le pipeline big data.
- En cloud GCP : Pour traiter les données de grandes dimension GCP recommande deux services DATAPROC et DATAFLOW. Suivant la documentation de GCP, DATAPROC est plus en adéquation avec des projets de migration depuis spark vers DATAPROC. Cependant, si on part from scratch il est recommandé d’utiliser les pipelines du service DATAFLOW. Airflow ou Cloud Composer (sur GCP) dispose des operators (provision ou run) des deux services DATAPROC et AIRFLOW. 

