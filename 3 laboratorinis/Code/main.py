# Jokubas Akramas
# IFF-8/12
# 2021-04-30
from functools import reduce
import matplotlib.pyplot as plt
import sys
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression

# 2. Užkrauti failo turinį į darbinę atmintį.
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


# TODO ijungt
# draw_plot_2d(years, spots, 'Saulės dienų aktyvumas pagal metus', 'Metai', 'Saulės aktyvumo dienos')


# Normalizavimas [-1; 1]
def normalize(data, min_value, delta):
    return [2 * (x - min_value) / delta - 1 for x in data]


# Anti normalizavimas
def unnormalize(data, min_value, delta):
    return [((x + 1) * delta) / 2 + min_value for x in data]


# Normalizacija
# spots_min = min(spots)
# spots_delta = max(spots) - spots_min
# spots = normalize(spots, spots_min, spots_delta)


# 5. Priimkime, kad autoregresinio modelio eilė bus lygi 2 (n=2). T.y priimame, kad sekančių metų dėmių
# prognozė yra įmanoma turint tik dviejų ankstesnių metų dėmių skaičių. Tuomet neuronas turės tik
# du įėjimus. Papildykite scenarijų, aprašant matricas P ir T, kuriose atitinkamai pateikiami
# (mokymosi) įvesties duomenys o taip pat išvesties duomenys.
def form_matrix(n, data):
    p = [[data[u] for u in range(i - n, i)] for i in range(n, len(data))]
    t = data[n:]
    # TODO ijungt
    # print('Suformuotos matricos P[,] = T[]')
    # for i in range(len(p)):
    #     print(p[i], ' = ', t[i])

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
    # TODO ijungt
    # draw_plot_3d(P1, P2, T, 'Koreliacijos grafikas', 'w1', 'w2', 'b')

# 7. Išskirkime iš įvesties P ir išvesties T duomenų rinkinių fragmentus, turinčius po 200 pradžioje esamų
# duomenų – taip vadinamą apmokymo duomenų rinkinį. Remiantis šiuo rinkiniu apskaičiuosime
# optimalias neurono svorio koeficientų reikšmes (autoregresinio modelio parametrus). Likę
# duomenys bus panaudoti modeliui verifikuoti. Tuomet, panaudojant jau esamas P ir T matricas,
# apibrėžkime dvi naujas – Pu ir Tu, kurios turės pirmus 200 duomenų.

# --------------------------------------------------------------------------
# Bandziau pats realizuoti, taciau neduota tiksliu rezultatu - J.A.21/04/30
# --------------------------------------------------------------------------
# def linear_regression_calculation(x, w, b):
#     for i in range(len(x)):
#         b += x[i] * w[i]
#     return math.tanh(b)
#     # return 1 if b >= 0 else 0
#     # return 1 / (1 + math.e ** -b)
#
#
# def recalculate_weights(w, b, step, pred, tu, pu):
#     for i in range(len(w)):
#         w[i] = w[i] + step * (tu - pred) * pu[i]
#     b = b + step * (tu - pred)
#     return w, b
#
#
# def calculate_weights(pu, tu, accuracy=0.1, learning_speed=0.2, epochs=50000):
#     n = len(pu[0])
#     w = np.random.rand(n)
#     b = np.random.random(1)[0]
#     for it in range(epochs):
#         found = True
#         predictions = [linear_regression_calculation(i, w, b) for i in pu]
#         mismatch = [predictions[i] - tu[i] for i in range(len(predictions))]
#         for i in range(len(mismatch)):
#             if abs(mismatch[i]) > accuracy:
#                 found = False
#                 w, b = recalculate_weights(w, b, learning_speed, predictions[i], tu[i], pu[i])
#         if found:
#             print('predictions = ', predictions)
#             print('true = ', tu)
#             print('Weights found, model accuracy = ', max(mismatch))
#             return w, b
#     print('Weights not found!')
#     sys.exit(-1)
#
# ------------------------------------------------------------------------

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
# TODO ijungt
# draw_2_plot_2d(Yu, Tu, Tsu, 'Modelio verifikacija (apmokoma sritis)',
#                'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

# Modelio verifikaciją taip pat atlikite su nematytu duomenų rinkiniu – testavimo rinkiniu, t.y. su
# duomenimis nuo 201 eilutės. Bei sukurkite analogiškus grafikus vaizduojant Tu ir Tsu reikšmes.
Pu_test = P[200:]
Tu_test = T[200:]
Tsu_test = model.predict(Pu_test)
# TODO ijungt
# draw_2_plot_2d(Yu, Tu, Tsu, 'Modelio verifikacija (testavimo sritis)',
#                'Metai', 'Aktyvios saulės dėmės', 'Tikros reikšmės', 'Prognozuojamos reikšmės')

# 11. Sukurti prognozės klaidos vektorių e (žr. išraiškos 1.2 paaiškinimą). Nubraižyti prognozės klaidos
# grafiką. Aprašyti jo ašis ir suteikti pavadinimą.
Tsu_all = model.predict(P)
e = [Tsu_all[i] - T[i] for i in range(len(Tsu_all))]
# TODO ijungt
# draw_plot_2d(years[len(P[0]):], e, 'Prognozės klaidos grafikas', 'Metai', 'Klaidos dydis')


# 12. Nubraižyti prognozės klaidų histogramą (hist). Ją pakomentuokite.
def draw_histogram(x, title, x_title, y_title):
    fig, axs = plt.subplots()
    axs.hist(x)
    plt.title(title)
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.show()

# TODO ijungt
# draw_histogram(e, 'Prognozės klaidų histograma', 'Klaidos dydis', 'Kartai')
