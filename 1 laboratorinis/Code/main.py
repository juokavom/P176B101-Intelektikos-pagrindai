# Python3.8
# Jokubas Akramas IFF-8/12
# 1 laboratorinis darbas
# P176B101 Intelektikos pagrindai 2021
from functools import reduce
import numpy as np
import constants as c
import matplotlib.pyplot as plt
import handler
import seaborn as sns
import plotly.graph_objects as go
import pandas as pd


def append_element_to_headers(headers, values):
    element = {}
    for i in range(len(values)):
        element[headers[i]] = values[i]
    return element


def handle_noise(data, sublist, header):
    q1 = np.quantile(sublist, .25)
    q3 = np.quantile(sublist, .75)
    lower = q1 - 1.5 * (q3 - q1)
    upper = q3 + 1.5 * (q3 - q1)
    for u in data:  # Triukšmai priskiriami viršutiniams ir apatiniams rėžiams duomenų faile
        if int(u[header]) < lower:
            u[header] = lower
        elif int(u[header]) > upper:
            u[header] = upper
    for i in range(len(sublist)):  # Triukšmai priskiriami viršutiniams ir apatiniams rėžiams nagrinėjamame atribute
        if sublist[i] < lower:
            sublist[i] = lower
        elif sublist[i] > upper:
            sublist[i] = upper
    sublist.sort()
    return q1, q3


def analyse_continuous_data(data, values):
    csv_list = []
    for i in values.keys():
        sublist = list(map(lambda x: int(x[i]) if x[i] != '' else '', data))
        average = np.average(list(filter(lambda x: x != '', sublist)))
        sublist = list(map(lambda x: np.round(average) if x == '' else x, sublist))
        for u in data:  # Tuščios reikšmės užpildomos vidurkiais
            if u[i] == '':
                u[i] = np.round(average)
        sublist.sort()
        q1, q3 = handle_noise(data, sublist, i)
        values[i][2] = values[i][2] * 100  # Trukstamos reiksmes paverciamos %
        values[i].append(len(set(sublist)))  # Kardinalumas
        values[i].append(min(sublist))  # Minimali reikšmė
        values[i].append(max(sublist))  # Maksimali reikšmė
        values[i].append(q1)  # 1-asis kvartilis
        values[i].append(q3)  # 3-asis kvartilis
        values[i].append(np.average(sublist))  # Vidurkis
        values[i].append(np.round(np.median(sublist)))  # Mediana
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
    return unique_values[moda_index[0]]


def analyse_categorical_data(data, values):
    csv_list = []
    for i in values.keys():
        sublist = list(map(lambda x: x[i], data))
        temp = []
        moda = all_modas(list(filter(lambda x: x != '', sublist)), temp)
        sublist = list(map(lambda x: x if x != '' else moda, sublist))
        for u in data:  # Tuščios reikšmės užpildomos vidurkiais
            if u[i] == '':
                u[i] = moda
        values[i][2] = values[i][2] * 100  # Trukstamos reiksmes paverciamos %
        values[i].append(len(set(sublist)))  # Kardinalumas
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
            len(list(filter(lambda x: x == '', sublist))) / len(sublist),  # Trūkstamos reikšmės
        ]
    return values


def horizontal_removal(data, remove_step):
    print('---------------------------------------Horizontalus šalinimas---------------------------------------')
    for row in data:
        empty_values = len(list(filter(lambda x: x == '', row.values()))) / len(row)
        if empty_values >= remove_step:
            data.remove(row)
            print('Eilutės: ', row, '\ntuščiosios reikšmės viršija nustatytą limitą (',
                  100 * remove_step, '%), todėl eilutė PAŠALINAMA.')


def vertical_removal(data, continuous, continuous_headers, categorical, categorical_headers, remove_step):
    print('---------------------------------------Vertikalus šalinimas---------------------------------------')
    for cont in continuous_headers:
        if float(continuous[cont][2]) >= remove_step:
            for i in data:
                del i[cont]
            print('Tolydinio atributo: ', continuous[cont][0], 'tuščiosios reikšmės viršija nustatytą limitą (',
                  100 * remove_step, '%), todėl atributas PAŠALINAMAS.')
            del continuous[cont]
    for cont in categorical_headers:
        if float(categorical[cont][2]) >= remove_step:
            for i in data:
                del i[cont]
            print('Kategorinio atributo: ', categorical[cont][0], 'tuščiosios reikšmės viršija nustatytą limitą (',
                  100 * remove_step, '%), todėl atributas PAŠALINAMAS.')
            del categorical[cont]


def handle_missing_values(data, continuous, continuous_headers, categorical, categorical_headers):
    horizontal_removal(data, 0.6)  # Horizontalus šalinimas (jei 60% eilutės tuščia)
    vertical_removal(data, continuous, continuous_headers, categorical, categorical_headers,
                     0.6)  # Vertikalus šalinimas (jei 60% stulpelio tuščia)


def draw_histograms(data, headers):
    n = round(1 + 3.22 * np.log(len(data)))
    for head in headers:
        sublist = list(map(lambda x: x[head], data))
        plt.title(head)
        plt.hist(sublist, bins=n)
        plt.show()


def draw_scatters(data, headers):
    for i in range(len(headers)):
        x1 = list(map(lambda x: int(x[headers[i]]), data))
        plt.rcParams.update({'figure.figsize': (10, 8), 'figure.dpi': 100})
        for u in range(len(headers)):
            if u == i:
                continue
            x2 = list(map(lambda x: int(x[headers[u]]), data))
            plt.scatter(x1, x2, label=headers[u] + f' koreliacija = {np.round(np.corrcoef(x1, x2)[0, 1], 2)}')
            plt.title(headers[i] + ' ir ' + headers[u])
            plt.legend()
            plt.show()


def draw_splom(df, headers):
    splom_dimensions = []
    for i in headers:
        splom_dimensions.append(dict(label=i, values=list(map(lambda x: x[i], df))))

    fig = go.Figure(data=go.Splom(
        dimensions=splom_dimensions,
        text='SPLOM diagrama',
        marker=dict(showscale=False,  # colors encode categorical variables
                    line_color='white', line_width=0.5)
    ))

    fig.update_layout(
        title='SPLOM diagrama',
        dragmode='select',
        width=600,
        height=600,
        hovermode='closest',
    )

    fig.show()


def draw_barplot(data, headers):
    for head in range(len(headers)):
        sublist = list(map(lambda x: x[headers[head]], data))
        categories = list(set(sublist))
        for cat in categories:
            for head2 in range(len(headers)):
                if head == head2:
                    continue
                sublist2 = list(map(lambda x: x[headers[head2]] if x[headers[head]] == cat else '', data))
                sublist2_unique = list(set(sublist2))
                sublist2_unique.remove('')
                sublist2_counts = list(map(lambda x: len(list(filter(lambda y: y == x, sublist2))), sublist2_unique))
                fig = plt.figure()
                # creating the bar plot
                plt.bar(sublist2_unique, sublist2_counts)

                plt.xlabel(headers[head2])
                # plt.ylabel("No. ")
                plt.title('Atributas: ' + headers[head] + '. Pasirinkimas: ' + cat)
                plt.show()


def draw_histograms_categorical(data, continuous_headers, categorical_headers):
    for cat in categorical_headers:
        sublist = list(map(lambda x: x[cat], data))
        categories = list(set(sublist))
        for cat2 in categories:
            for cont in continuous_headers:
                sublist2 = list(
                    filter(lambda y: y != '', list(map(lambda x: int(x[cont]) if x[cat] == cat2 else '', data))))
                plt.title('Kategorinis atributas: ' + cat + ':' + cat2 + ', tolydus atributas: ' + cont)
                plt.hist(sublist2)
                plt.xlabel(cont)
                plt.ylabel(cat)
                plt.show()


def draw_boxplot(data, continuous_headers, categorical_headers):
    for cont in continuous_headers:
        for cat in categorical_headers:
            sublist = list(map(lambda x: x[cat], data))
            categories = list(set(sublist))
            df = []
            counter = 1
            count = []
            titles = []
            for cat2 in categories:
                sublist2 = list(
                    filter(lambda y: y != '', list(map(lambda x: int(x[cont]) if x[cat] == cat2 else '', data))))
                df.append(sublist2)
                titles.append(cat2)
                count.append(counter)
                counter += 1
            fig = plt.figure(figsize=(10, 7))
            plt.title('Tolydinis: ' + cont + ' su kardinaliu: ' + cat)
            plt.boxplot(df)
            plt.xlabel(cat)
            plt.ylabel(cont)
            plt.xticks(count, titles)
            plt.show()


def calculate_cov_and_cor(data, headers):
    csv_cov = []
    csv_cor = []
    clean_dataset = {}
    for head in headers:
        sublist = list(map(lambda x: float(x[head]), data))
        clean_dataset[head] = sublist
        covariance = {}
        correlation = {}
        covariance[''] = head
        correlation[''] = head
        for head2 in headers:
            sublist2 = list(map(lambda x: float(x[head2]), data))
            covariance[head2] = np.cov(sublist, sublist2)[0][1]
            correlation[head2] = np.corrcoef(sublist, sublist2)[0][1]
        csv_cov.append(covariance)
        csv_cor.append(correlation)
    df = pd.DataFrame(clean_dataset)
    corrMatrix = df.corr()
    sns.heatmap(corrMatrix, annot=True)
    plt.show()
    return csv_cov, csv_cor


# ---DUOMENŲ APDOROJIMAS--- #

# Nuskaitomas duomenų failas
dataset, fields = handler.csv_to_dict_list(c.DATASET_TRAIN_FILE)
# Sukuriamas išvedimo folderis
handler.create_package_if_no_exist(c.OUTPUT_FOLDER_NAME)
# Apdorojamos pradinės tolydžiųjų charakteristikos
continuous = analyze_initial_values(dataset, c.CONTINUOUS_DATA_HEADERS)
# Apdorojamos pradinės kategorinių charakteristikos
categorical = analyze_initial_values(dataset, c.CATEGORICAL_DATA_HEADERS)
# Tuščių reikšmių apdorojimas šalinant horizontaliai ir vertikaliai
handle_missing_values(dataset, continuous, c.CONTINUOUS_DATA_HEADERS,
                      categorical, c.CATEGORICAL_DATA_HEADERS)
# Apdorojamos likusios tolydžiųjų charakteristikos
continuous_dict_list = analyse_continuous_data(dataset, continuous)
# Apdorojamos likusios kategorinių charakteristikos
categorical_dict_list = analyse_categorical_data(dataset, categorical)
# Išvedama tolydžiųjų duomenų charakteristikų lentelė
handler.write_to_csv(c.CONTINUOUS_OUTPUT_PATH, continuous_dict_list,
                     c.CONTINUOUS_ANALYSIS_OUTPUT_HEADERS)
# Išvedama kategorinių duomenų charakteristikų lentelė
handler.write_to_csv(c.CATEGORICAL_OUTPUT_PATH, categorical_dict_list,
                     c.CATEGORICAL_ANALYSIS_OUTPUT_HEADERS)

final_headers = []
for i in categorical.keys():
    final_headers.append(i)
for i in continuous.keys():
    final_headers.append(i)
final_headers.append('MALICIOUS_OFFENSE')

# Išvedami pertvarkyti duomenys .csv formatu
handler.write_to_csv(c.PROCESSED_OUTPUT_PATH, dataset, final_headers)

# ---DIAGRAMŲ BRAIŽYMAS--- #

# # Braižyti histogramas
# draw_histograms(dataset, final_headers)
# # Braižyti scatter plot
# draw_scatters(dataset, list(continuous.keys()))
# # SPLOM diagramos braižymas
# draw_splom(dataset, list(continuous.keys()))
# # Braižyti histogramas tolydiniams pagal kategorinius atributus
# draw_histograms_categorical(dataset, list(continuous.keys()), list(categorical.keys()))
# # Braižyti boxplotus kategoriniams pagal tolydinius atributus
# draw_boxplot(dataset, list(continuous.keys()), list(categorical.keys()))

# Skaiciuoti kovariacijos ir koreliacijos reiksmes
csv_cov, csv_cor = calculate_cov_and_cor(dataset, continuous.keys())

final_headers = ['']
for i in continuous.keys():
    final_headers.append(i)

# Išvesti kovariacijos ir koreliacijos matricas į rezultatų failus
handler.write_to_csv(c.COVARIANCE_OUTPUT_PATH, csv_cov, final_headers)
handler.write_to_csv(c.CORRELATION_OUTPUT_PATH, csv_cor, final_headers)
