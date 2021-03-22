import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

module_rating = ctrl.Antecedent(np.arange(1, 11, 1), 'Modulio vertinimas (bal.)')
attendance = ctrl.Antecedent(np.arange(1, 101, 1), 'Lankomumas (%)')
party_days = ctrl.Antecedent(np.arange(0, 8, 1), 'Vakarėlių dienos (d.)')
MODULE_SCORE = ctrl.Antecedent(np.arange(1, 11, 1), 'Modulio įvertinimas (bal.)')

module_rating['Lengvas'] = fuzz.trimf(module_rating.universe, [1, 1, 4])
module_rating['Vidutinis'] = fuzz.trapmf(module_rating.universe, [2, 4, 7, 8])
module_rating['Sunkus'] = fuzz.trapmf(module_rating.universe, [6, 8, 10, 10])

attendance['Retas'] = fuzz.trapmf(attendance.universe, [1, 1, 40, 50])
attendance['Vidutinis'] = fuzz.trimf(attendance.universe, [40, 70, 80])
attendance['Dažnas'] = fuzz.trapmf(attendance.universe, [70, 90, 100, 100])

party_days['Beveik neegzistuojančios'] = fuzz.trimf(party_days.universe, [0, 0, 2])
party_days['Kelios'] = fuzz.trapmf(party_days.universe, [1, 2, 3, 4])
party_days['Didžioji dalis'] = fuzz.trapmf(party_days.universe, [3, 5, 7, 7])

MODULE_SCORE['Prastas'] = fuzz.trapmf(MODULE_SCORE.universe, [1, 1, 5, 6])
MODULE_SCORE['Pažangus'] = fuzz.trapmf(MODULE_SCORE.universe, [5, 6, 7, 8])
MODULE_SCORE['Puikus'] = fuzz.trapmf(MODULE_SCORE.universe, [7, 8, 10, 10])

party_days.view()

plt.show()
