DATASET_TRAIN_FILE: str = 'train_dataset_Jokubas_Akramas.csv'
OUTPUT_FOLDER_NAME: str = 'output'
# ----
CATEGORICAL_DATA_HEADERS = ['REGION', 'OS', 'PROTOCOL']
CONTINUOUS_DATA_HEADERS = ['X_1', 'X_2', 'X_3', 'X_4', 'X_5', 'X_6', 'X_7']
OUTPUT_VARIABLE: str = 'MALICIOUS_OFFENSE'
# ----
CATEGORICAL_OUTPUT_PATH: str = OUTPUT_FOLDER_NAME + "/kategorinių_duomenų_analizė.csv"
CATEGORICAL_ANALYSIS_OUTPUT_HEADERS = ['Atributo pavadinimas', 'Kiekis (Eilučių sk.)', 'Trūkstamos reikšmės, %',
                                   'Kardinalumas', 'Moda', 'Modos dažnumas', 'Moda, %', '2-oji moda',
                                   '2-osios Modos dažnumas', '2-oji Moda, %']
CONTINUOUS_OUTPUT_PATH: str = OUTPUT_FOLDER_NAME + "/tolydinių_duomenų_analizė.csv"
CONTINUOUS_ANALYSIS_OUTPUT_HEADERS = ['Atributo pavadinimas', 'Kiekis (Eilučių sk.)', 'Trūkstamos reikšmės, %',
                                  'Kardinalumas', 'Minimali reikšmė', '1-asis kvartilis', '3-asis kvartilis',
                                  'Vidurkis', 'Mediana', 'Standartinis nuokrypis']
# ----
