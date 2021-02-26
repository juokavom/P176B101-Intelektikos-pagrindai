# Python3.8
# Jokubas Akramas IFF-8/12
# 1 laboratorinis darbas

import csv


def csv_to_dict_list(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fields = reader.fieldnames
        list_out = [row for row in reader]
        return list_out, fields


dataset, fields = csv_to_dict_list('dataset_Jokubas_Akramas.csv')
print(fields)
