# Jokubas Akramas
# IFF-8/12
# 2021-04-30
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression, SGDRegressor, SGDClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 2. Užkrauti failo turinį į darbinę atmintį.
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler

(years, spots) = zip(*[x.split('\n')[0].split('\t') for x in open('sunspot.txt').readlines()])


# 3. Patikrinti ar užkrauta atitinkama matrica – pirmas stulpelis atitinka metus,
# antras – saulės dienų aktyvumą
def parse_int_if_can(number):
    try:
        parsed = int(number)
        return parsed
    except ValueError:
        return -1


def validate_input_data(data, min_val, max_val):
    return reduce(lambda prev, curr: prev and (min_val <= parse_int_if_can(curr) <= max_val), data, True)


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


# 4. Pirma užduotis, kurią turi realizuoti mūsų programa – nubrėžti saulės dėmių aktyvumo už 1700-
# 2014 metus grafiką. Grafikas turi būti pilnai aprašytas – pateikti ašių ir grafiko pavadinimus.
def draw_plot_2d(x, y, title, x_title, y_title):
    plt.plot(x, y)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.show()


years = list(map(lambda x: int(x), years))
spots = list(map(lambda x: int(x), spots))
draw_plot_2d(years, spots, 'Saulės dėmių aktyvumas pagal metus', 'Metai', 'Aktyvios saulės dėmės')


# 5. Priimkime, kad autoregresinio modelio eilė bus lygi 2 (n=2). T.y priimame, kad sekančių metų dėmių
# prognozė yra įmanoma turint tik dviejų ankstesnių metų dėmių skaičių. Tuomet neuronas turės tik
# du įėjimus. Papildykite scenarijų, aprašant matricas P ir T, kuriose atitinkamai pateikiami
# (mokymosi) įvesties duomenys o taip pat išvesties duomenys.
def form_matrix(n, data):
    p = [[data[u] for u in range(i - n, i)] for i in range(n, len(data))]
    t = data[n:]
    return p, t


(P, T) = form_matrix(2, spots)


# 6. Nubrėžti trimatę diagramą, joje vaizduojant įvesties ir išvesties duomenis P ir T atitinkamai.
# Išanalizuoti gautą grafiką - sukiokite kol nepamatysite koreliacijos tarp duomenų požymius. Kokia
# yra neurono svorio koeficientų w1, w2, b optimalių reikšmių parinkimo grafinė interpretacija?
# Pridėti ašių ir grafiko pavadinimus.


def draw_plot_3d(x, y, z, title, x_title, y_title, z_title):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    ax.set_title(title)
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)
    plt.show()


if len(P[0]) == 2:
    (P1, P2) = zip(*P)
    P1 = list(P1)
    P2 = list(P2)
    draw_plot_3d(P1, P2, T, 'Koreliacijos grafikas', 'w1', 'w2', 'b')

# 7. Išskirkime iš įvesties P ir išvesties T duomenų rinkinių fragmentus, turinčius po 200 pradžioje esamų
# duomenų – taip vadinamą apmokymo duomenų rinkinį. Remiantis šiuo rinkiniu apskaičiuosime
# optimalias neurono svorio koeficientų reikšmes (autoregresinio modelio parametrus). Likę
# duomenys bus panaudoti modeliui verifikuoti. Tuomet, panaudojant jau esamas P ir T matricas,
# apibrėžkime dvi naujas – Pu ir Tu, kurios turės pirmus 200 duomenų.

Pu = P[:200]
Tu = T[:200]

# 8. Sukurkite tiesinės autoregresijos modelį panaudojant apmokymo duomenų matricas Pu ir Tu.
# Python mokomoji medžiaga pateikta adresu https://realpython.com/linear-regression-in-python/ .

model = LinearRegression().fit(Pu, Tu)

# 9. Pavaizduoti gautas koeficientų reikšmes
print('Svoriai (w[]) = ', model.coef_)
print('Poslinkis (b) = ', model.intercept_)


# 10. Sekančiame žingsnyje atliksime modelio verifikaciją – t.y. patikrinsime prognozavimo kokybę
# atliekant modelio veikimo imitaciją. Pradžioje tai atliksime su apmokymo duomenų rinkiniu, kuris
# buvo panaudotas svorio koeficientams apskaičiuoti.
# Tarkime, turime suprognozuoti salės dėmių aktyvumą 1702–1901 metais. Tuo tikslu padavinėsime į
# modelio įėjimus aktyvumo rinkinius tokiais metais: 1700 ir 1701, 1701 ir 1702, …, 1899 ir 1900. Tai
# galima atlikti automatizuotu būdu paduodant įvesties duomenis, esančius matricoje Pu. Pasėkoje
# gausime rezultatų vektorių Tsu, t.y. prognozuojamas aktyvumo reikšmes 1702–1901 metams.
# Kadangi turime tikrąsias dėmių aktyvumo reikšmes nagrinėjamu laiko periodu (Tu), jas galime
# patikrinti su prognozuojamomis reikšmėmis (Tsu). Gautame grafike vaizdavimai turi būti
# paženklinti skirtingomis spalvomis bei turėti legendą.
def draw_2_plot_2d(x, y1, y2, title, x_title, y_title, y1_title, y2_title):
    fig, ax = plt.subplots()
    ax.plot(x, y1, label=y1_title)
    ax.plot(x, y2, label=y2_title)
    legend = ax.legend()
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()


Yu = years[:len(Pu)]
Tsu = model.predict(Pu)
draw_2_plot_2d(Yu, Tu, Tsu, 'Modelio verifikacija (apmokoma sritis)',
               'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

# Modelio verifikaciją taip pat atlikite su nematytu duomenų rinkiniu – testavimo rinkiniu, t.y. su
# duomenimis nuo 201 eilutės. Bei sukurkite analogiškus grafikus vaizduojant Tu ir Tsu reikšmes.
Pu_test = P[200:]
Tu_test = T[200:]
Tsu_test = model.predict(Pu_test)
draw_2_plot_2d(Yu, Tu, Tsu, 'Modelio verifikacija (testavimo sritis)',
               'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

# 11. Sukurti prognozės klaidos vektorių e (žr. išraiškos 1.2 paaiškinimą). Nubraižyti prognozės klaidos
# grafiką. Aprašyti jo ašis ir suteikti pavadinimą.
Tsu_all = model.predict(P)
e = [Tsu_all[i] - T[i] for i in range(len(Tsu_all))]
draw_plot_2d(years[len(P[0]):], e, 'Prognozės klaidos grafikas', 'Metai', 'Klaidos dydis')


# 12. Nubraižyti prognozės klaidų histogramą (hist). Ją pakomentuokite.
def draw_histogram(x, title, x_title, y_title):
    fig, axs = plt.subplots()
    axs.hist(x)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()


draw_histogram(e, 'Prognozės klaidų histograma', 'Klaidos dydis', 'Kartai')

# 13. Remiantis (1.3) apskaičiuoti vidutinės kvadratinės prognozės klaidos reikšmę.
# Šiame darbe MSE įvertis neturi viršyti 300.
# Apskaičiuokite prognozės absoliutaus nuokrypio medianą (ang. Median Absolute Deviation)
# Palyginkite skirtumus tarp MSE ir MAD įverčių ir pakomentuokite.
# Sekančiuose punktuose sukurto scenarijaus tekstą modifikuosime, kad modelio svorio koeficientai
# būtų skaičiuojami iteraciniu metodu – atliekant neurono apmokymo procedūrą.

print('Vidutinė kvadratinės prognozės klaida (MSE) = ', mean_squared_error(T, Tsu_all))
print('Prognozės absoliutaus nuokrypio mediana (MAD) = ', mean_absolute_error(T, Tsu_all))


# 15. Panaudojant aprašą pateiktą adresu https://www.bogotobogo.com/python/scikit-learn/SingleLayer-Neural-Network
# -Adaptive-Linear-Neuron.php sukurti tiesinį neuroną.

# 16. Apibrėžti siekiamą mokymosi klaidos MSE reikšmę (ang. error goal) intervale 150 – 300 ir
# maksimalų epochų kiekį (pvz. 1000). (Pastaba. Vienos epochos metu modelis panaudoja visą
# duomenų rinkinį. Vienos iteracijos metu modelis panaudoja tik vieną duomenų rinkinio eilutę.)

class AdaptiveLinearNeuron(object):
    def __init__(self, rate=0.01, niter=10):
        self.rate = rate
        self.niter = niter

    def fit(self, X, y):
        """Fit training data
      X : Training vectors, X.shape : [#samples, #features]
      y : Target values, y.shape : [#samples]
      """

        # weights
        self.weight = np.zeros(1 + X.shape[1])

        # Number of misclassifications
        self.errors = []

        # Cost function
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
        """Calculate net input"""
        return np.dot(X, self.weight[1:]) + self.weight[0]

    def activation(self, X):
        """Compute linear activation"""
        return self.net_input(X)

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.activation(X) >= 0.0, 1, -1)


Pu = np.array(Pu)
Tu = np.array(Tu)

# 17. Įvykdyti modelį. Atspausdinti gautas po apmokymo svorio koeficientų reikšmes. Jas palyginti su
# gautais 9 žingsnyje.
linear_neuron = AdaptiveLinearNeuron(0.000001, 200).fit(Pu, Tu)
print('Tiesinio neurono svoriai: ', linear_neuron.weight)

# 20. Darbą atlikome priimant pradžioje pasiūlytą mūsų modelio struktūrą – sekančios reikšmės
# prognozavimas atliekamas remiantis dviejų ankstesniųjų metų duomenimis (t.y. modelio eilė n=2).
# Tiesinės autoregresijos ir tiesinio neurono modelių scenarijus pakoreguoti tokiu būdu, kad
# prognozė remtųsi didesniu nei anksčiau duomenų kiekiu – kai n=6 ir kai n=10. Tuo tikslu reikės
# atitinkamai modifikuoti matricų P ir T apibrėžimus. Ištirti (grafiškai ir pakomentuojant raštu)
# modelio struktūros keitimo įtaką į prognozavimo kokybę.

# ----------------------------------------------------------------------------------
# Didinant modelio eile mazeja klaida
# ----------------------------------------------------------------------------------
