# Jokubas Akramas
# IFF-8/12
# 2021-05-01
import math
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import median_abs_deviation
from sklearn.linear_model import LinearRegression

N = 2  # Modelio eilė
dataset = 'sunspot.txt'  # Dataset file


def parse_int_if_can(number):
    try:
        parsed = int(number)
        return parsed
    except ValueError:
        return -1


def draw_plot_2d(x, y, title, x_title, y_title):
    plt.plot(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.show()


def validate_input_data(data, min_val, max_val):
    return reduce(lambda prev, curr: prev and (min_val <= parse_int_if_can(curr) <= max_val), data, True)


def form_matrix(n, data):
    p = [[data[u] for u in range(i - n, i)] for i in range(n, len(data))]
    t = data[n:]
    return p, t


def draw_plot_3d(x, y, z, title, x_title, y_title, z_title):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)
    plt.show()


def draw_2_plot_2d(x, y1, y2, title, x_title, y_title, y1_title, y2_title):
    fig, ax = plt.subplots()
    ax.plot(x, y1, label=y1_title)
    ax.plot(x, y2, label=y2_title)
    ax.legend()
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()


def draw_histogram(x, title, x_title, y_title):
    fig, axs = plt.subplots()
    axs.hist(x)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()


def MSE(test, pred):
    summation = 0
    for i in range(0, len(pred)):
        difference = test[i] - pred[i]
        squared_difference = difference ** 2
        summation = summation + squared_difference
    return summation / len(pred)


(years, spots) = zip(*[x.split('\n')[0].split('\t') for x in open(dataset).readlines()])

years_valid = validate_input_data(years, 1700, 2021)
spots_valid = validate_input_data(spots, 0, 1000)

print("Metai atitinka validaciją"
      if years_valid
      else "Metai neatitinka validacijos")
print("Saules dėmių aktyvumas atitinka validaciją"
      if spots_valid
      else "Saules dėmių aktyvumas neatitinka validacijos")

if not years_valid or not spots_valid:
    sys.exit(-1)

years = list(map(lambda x: int(x), years))
spots = list(map(lambda x: int(x), spots))
draw_plot_2d(years, spots, 'Saulės dėmių aktyvumas pagal metus', 'Metai', 'Aktyvios saulės dėmės')

(P, T) = form_matrix(N, spots)
print('Mokymosi vektorius P (įvestys) = ', P)
print('Mokymosi vektorius T (išvestys) = ', T)

if len(P[0]) == 2:
    (P1, P2) = zip(*P)
    P1 = list(P1)
    P2 = list(P2)
    draw_plot_3d(P1, P2, T, 'Koreliacijos grafikas', 'w1', 'w2', 'b')

Pu = P[:200]
Tu = T[:200]

model = LinearRegression().fit(Pu, Tu)

print('Svoriai (w[]) = ', model.coef_)
print('Poslinkis (b) = ', model.intercept_)

Yu = years[:len(Pu)]
Tsu = model.predict(Pu)
draw_2_plot_2d(Yu, Tu, Tsu, 'Modelio verifikacija (apmokoma sritis)',
               'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

Yu = years[len(Pu) + N:]
Pu_test = P[200:]
Tu_test = T[200:]
Tsu_test = model.predict(Pu_test)
draw_2_plot_2d(Yu, Tu_test, Tsu_test, 'Modelio verifikacija (testavimo sritis)',
               'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

Tsu_all = model.predict(P)
e = [Tsu_all[i] - T[i] for i in range(len(Tsu_all))]
draw_plot_2d(years[len(P[0]):], e, 'Prognozės klaidos grafikas', 'Metai', 'Klaidos dydis')

draw_histogram(e, 'Prognozės klaidų histograma', 'Klaidos dydis', 'Kartai')

# print('Vidutinė kvadratinės prognozės klaida (MSE) = ', mean_squared_error(T, Tsu_all))
print('Vidutinė kvadratinės prognozės klaida (MSE) = ', MSE(T, Tsu_all))
print('Prognozės absoliutaus nuokrypio mediana (MAD) = ', median_abs_deviation(Tsu_all))


class AdaptiveLinearNeuron(object):
    def __init__(self, rate=0.01, niter=10):
        self.rate = rate
        self.niter = niter

    def fit(self, X, y):
        self.weight = np.zeros(1 + X.shape[1])
        self.errors = []
        self.cost = []

        for i in range(self.niter):
            output = self.net_input(X)
            errors = y - output
            self.weight[1:] += self.rate * X.T.dot(errors)
            self.weight[0] += self.rate * errors.sum()
            cost = (errors ** 2).sum() / 2.0
            self.cost.append(cost)
        return self

    def net_input(self, X):
        return np.dot(X, self.weight[1:]) + self.weight[0]

    def activation(self, X):
        return self.net_input(X)

    def predict(self, X):
        return 1 / (1 + math.e ** self.activation(X))


Pu = np.array(Pu)
Tu = np.array(Tu)

linear_neuron = AdaptiveLinearNeuron(0.000001, 200).fit(Pu, Tu)
print('Tiesinio neurono svoriai: ', linear_neuron.weight)
prediction = linear_neuron.predict(Pu_test)

min_v = min(Tu_test)
delta_v = max(Tu_test) - min_v
Tu_test = list(map(lambda x: (x - min_v) / delta_v, Tu_test))

mse = MSE(Tu_test, prediction)
mse = mse * delta_v + min_v
print("Tiesinio neurono MSE: ", mse)
print("Tiesinio neurono MAD: ", median_abs_deviation(prediction))
