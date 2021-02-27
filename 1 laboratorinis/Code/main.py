# Python3.8
# Jokubas Akramas IFF-8/12
# 1 laboratorinis darbas
# P176B101 Intelektikos pagrindai 2021
import csv
import errno
import os
import constants as c


def create_package_if_no_exist(path):
    try:
        os.makedirs(path)
        print("Output folder created at: ",
              os.path.dirname(os.path.realpath(path)))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def csv_to_dict_list(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fields = reader.fieldnames
        list_out = [row for row in reader]
        return list_out, fields


def write_to_csv(path, items, header_fields):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=header_fields)
        writer.writeheader()
        for row in items:
            writer.writerow(row)


dataset, fields = csv_to_dict_list(c.DATASET_TRAIN_FILE)
create_package_if_no_exist(c.OUTPUT_FOLDER_NAME)
write_to_csv(c.CATEGORICAL_OUTPUT_PATH, [], c.CATEGORICAL_OUTPUT_HEADER_NAMES)