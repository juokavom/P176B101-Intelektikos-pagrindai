import csv
import errno
import os


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

