# Python3.8
# Jokubas Akramas IFF-8/12
# 1 laboratorinis darbas
# P176B101 Intelektikos pagrindai 2021
from functools import reduce
import numpy as np
import constants as c
import handler


def append_element_to_headers(headers, values):
    element = {}
    for i in range(len(values)):
        element[headers[i]] = values[i]
    return element


def analyse_continuous_data(data, values):
    csv_list = []
    for i in c.CONTINUOUS_DATA_HEADERS:
        sublist = list(map(lambda x: int(x[i]), data))
        sublist.sort()
        values[i].append(min(sublist))  # Minimali reikšmė
        values[i].append(max(sublist))  # Maksimali reikšmė
        values[i].append(np.quantile(sublist, .25))  # 1-asis kvartilis
        values[i].append(np.quantile(sublist, .75))  # 3-asis kvartilis
        values[i].append(np.average(sublist))  # Vidurkis
        values[i].append(np.median(sublist))  # Mediana
        values[i].append(np.std(sublist))  # Standartinis nuokrypis
        csv_list.append(append_element_to_headers(c.CONTINUOUS_ANALYSIS_OUTPUT_HEADERS, values[i]))
    return csv_list


def all_modas(data, values_list):
    unique_values = list(set(data))
    value_counts = list(map(lambda x: len(list(filter(lambda y: y == x, data))), unique_values))
    counts_copy = value_counts.copy()
    counts_copy.sort()
    moda_index = value_counts.index(counts_copy.pop()), value_counts.index(counts_copy.pop())
    for index in moda_index:
        values_list.append(unique_values[index])
        values_list.append(value_counts[index])
        values_list.append(100 * value_counts[index] / len(data))


def analyse_categorical_data(data, values):
    csv_list = []
    for i in c.CATEGORICAL_DATA_HEADERS:
        sublist = list(map(lambda x: x[i], data))
        all_modas(sublist, values[i])  # 1-oji ir 2-oji modos su charakteristikomis
        csv_list.append(append_element_to_headers(c.CATEGORICAL_ANALYSIS_OUTPUT_HEADERS, values[i]))
    return csv_list


def analyze_initial_values(data, headers):
    values = {}
    for i in headers:
        sublist = list(map(lambda x: x[i], data))
        values[i] = [
            i,  # Atributo pavadinimas
            len(sublist),  # Eilučių kiekis
            '%d' % (len(list(filter(lambda x: x == '', sublist))) / len(sublist)) + '%',  # Trūkstamos reikšmės
            len(list(set(sublist))),  # Kardinalumas
        ]
    return values


def horizontal_removal(data, remove_step):
    for row in data:
        empty_values = len(list(filter(lambda x: x == '', row.values()))) / len(row)
        if empty_values >= remove_step:
            data.remove(row)
            print('Eilutės: ', row, '\ntuščiosios reikšmės viršija nustatytą limitą (',
                  100 * remove_step, '%), todėl eilutė PAŠALINAMA.')


def handle_missing_values(data, continuous, categorical):
    horizontal_removal(data, 0.6)  # Horizontalus salinimas (jei 60% eilutes tuscia)
    print(len(data))


# Nuskaitomas duomenų failas
dataset, fields = handler.csv_to_dict_list(c.DATASET_TRAIN_FILE)
# Sukuriamas išvedimo folderis
handler.create_package_if_no_exist(c.OUTPUT_FOLDER_NAME)
# Apdorojamos pradinės tolydžiųjų charakteristikos
continuous = analyze_initial_values(dataset, c.CONTINUOUS_DATA_HEADERS)
# Apdorojamos pradinės kategorinių charakteristikos
categorical = analyze_initial_values(dataset, c.CATEGORICAL_DATA_HEADERS)

handle_missing_values(dataset, continuous, categorical)

# # Apdorojamos likusios tolydžiųjų charakteristikos
# continuous_dict_list = analyse_continuous_data(dataset, continuous)
# # Apdorojamos likusios kategorinių charakteristikos
# categorical_dict_list = analyse_categorical_data(dataset, categorical)
# # Išvedama tolydžiųjų duomenų charakteristikų lentelė
# handler.write_to_csv(c.CONTINUOUS_OUTPUT_PATH, continuous_dict_list,
#                      c.CONTINUOUS_ANALYSIS_OUTPUT_HEADERS)
# # Išvedama kategorinių duomenų charakteristikų lentelė
# handler.write_to_csv(c.CATEGORICAL_OUTPUT_PATH, categorical_dict_list,
#                      c.CATEGORICAL_ANALYSIS_OUTPUT_HEADERS)
