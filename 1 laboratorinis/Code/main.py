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


def analyse_continuous_data(data):
    csv_list = []
    for i in c.CONTINUOUS_DATA_HEADERS:
        sublist = list(map(lambda x: int(x[i]), data))
        sublist.sort()
        values = [
            i,  # Atributo pavadinimas
            len(sublist),  # Eilučių kiekis
            '%d' % (len(list(filter(lambda x: x == '', sublist))) / len(sublist)) + '%',  # Trūkstamos reikšmės
            len(list(set(sublist))),  # Kardinalumas
            min(sublist),  # Minimali reikšmė
            max(sublist),  # Maksimali reikšmė
            np.quantile(sublist, .25),  # 1-asis kvartilis
            np.quantile(sublist, .75),  # 3-asis kvartilis
            np.average(sublist),  # Vidurkis
            np.median(sublist),  # Mediana
            np.std(sublist)  # Standartinis nuokrypis
        ]
        csv_list.append(append_element_to_headers(c.CONTINUOUS_ANALYSIS_OUTPUT_HEADERS, values))
    handler.write_to_csv(c.CONTINUOUS_OUTPUT_PATH, csv_list, c.CONTINUOUS_ANALYSIS_OUTPUT_HEADERS)


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

def analyse_categorical_data(data):
    csv_list = []
    for i in c.CATEGORICAL_DATA_HEADERS:
        sublist = list(map(lambda x: x[i], data))
        values = [
            i,  # Atributo pavadinimas
            len(sublist),  # Eiluciu kiekis
            '%d' % (len(list(filter(lambda x: x == '', sublist))) / len(sublist)) + '%',  # Trukstamos reiksmes
            len(list(set(sublist)))  # Kardinalumas
        ]
        all_modas(sublist, values)  # 1-oji ir 2-oji modos su charakteristikomis
        csv_list.append(append_element_to_headers(c.CATEGORICAL_ANALYSIS_OUTPUT_HEADERS, values))
    handler.write_to_csv(c.CATEGORICAL_OUTPUT_PATH, csv_list, c.CATEGORICAL_ANALYSIS_OUTPUT_HEADERS)


dataset, fields = handler.csv_to_dict_list(c.DATASET_TRAIN_FILE)
handler.create_package_if_no_exist(c.OUTPUT_FOLDER_NAME)
analyse_continuous_data(dataset)
analyse_categorical_data(dataset)
