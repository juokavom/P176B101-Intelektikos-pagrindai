import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

module_rating = ctrl.Antecedent(np.arange(1, 11, 1), 'module_rating')
attendance = ctrl.Antecedent(np.arange(1, 101, 1), 'attendance')
party_days = ctrl.Antecedent(np.arange(0, 8, 1), 'party_days')
MODULE_SCORE = ctrl.Consequent(np.arange(1, 11, 1), 'MODULE_SCORE')

# module_rating = ctrl.Antecedent(np.arange(1, 11, 1), 'Modulio vertinimas (bal.)')
# attendance = ctrl.Antecedent(np.arange(1, 101, 1), 'Lankomumas (%)')
# party_days = ctrl.Antecedent(np.arange(0, 8, 1), 'Vakarėlių dienos (d.)')
# MODULE_SCORE = ctrl.Antecedent(np.arange(1, 11, 1), 'Modulio įvertinimas (bal.)')

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

# module_rating.view()
# attendance.view()
# party_days.view()
# MODULE_SCORE.view()


# rule1 = ctrl.Rule(module_rating['Lengvas'] | party_days['Beveik neegzistuojančios'], MODULE_SCORE['Puikus'])
# rule2 = ctrl.Rule(module_rating['Lengvas'] & attendance['Dažnas'], MODULE_SCORE['Puikus'])
# rule3 = ctrl.Rule(module_rating['Vidutinis'] & attendance['Dažnas'] & party_days['Beveik neegzistuojančios'], MODULE_SCORE['Puikus'])
# rule4 = ctrl.Rule(module_rating['Lengvas'] & attendance['Vidutinis'], MODULE_SCORE['Puikus'])
# rule5 = ctrl.Rule(party_days['Beveik neegzistuojančios'], MODULE_SCORE['Puikus'])
# rule6 = ctrl.Rule(~attendance['Retas'], MODULE_SCORE['Pažangus'])
# rule7 = ctrl.Rule(module_rating['Sunkus'] & attendance['Dažnas'], MODULE_SCORE['Pažangus'])
# rule8 = ctrl.Rule(party_days['Kelios'] | module_rating['Vidutinis'], MODULE_SCORE['Pažangus'])
# rule9 = ctrl.Rule(party_days['Didžioji dalis'] & module_rating['Lengvas'], MODULE_SCORE['Pažangus'])
# rule10 = ctrl.Rule(attendance['Retas'] & party_days['Beveik neegzistuojančios'] & module_rating['Vidutinis'], MODULE_SCORE['Pažangus'])
# rule11 = ctrl.Rule(attendance['Vidutinis'] | party_days['Kelios'], MODULE_SCORE['Pažangus'])
# rule12 = ctrl.Rule(~module_rating['Sunkus'], MODULE_SCORE['Pažangus'])
# rule13 = ctrl.Rule(module_rating['Sunkus'] & attendance['Retas'], MODULE_SCORE['Prastas'])
# rule14 = ctrl.Rule(party_days['Didžioji dalis'] | attendance['Retas'], MODULE_SCORE['Prastas'])
# rule15 = ctrl.Rule(module_rating['Sunkus'] & party_days['Kelios'] & attendance['Retas'], MODULE_SCORE['Prastas'])
# rule16 = ctrl.Rule(module_rating['Sunkus'] & party_days['Didžioji dalis'], MODULE_SCORE['Prastas'])
# rule17 = ctrl.Rule(attendance['Retas'] & module_rating['Sunkus'] & party_days['Didžioji dalis'], MODULE_SCORE['Prastas'])
#
# module_score_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17])
# score = ctrl.ControlSystemSimulation(module_score_ctrl)

# `|` (OR), `&` (AND), `~` (NOT)
rules = [
    ctrl.Rule(module_rating['Lengvas'] | party_days['Beveik neegzistuojančios'], MODULE_SCORE['Puikus']),
    ctrl.Rule(module_rating['Lengvas'] & attendance['Dažnas'], MODULE_SCORE['Puikus']),
    ctrl.Rule(module_rating['Vidutinis'] & attendance['Dažnas'] & party_days['Beveik neegzistuojančios'],
              MODULE_SCORE['Puikus']),
    ctrl.Rule(module_rating['Lengvas'] & attendance['Vidutinis'], MODULE_SCORE['Puikus']),
    ctrl.Rule(party_days['Beveik neegzistuojančios'], MODULE_SCORE['Puikus']),
    ctrl.Rule(~attendance['Retas'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(module_rating['Sunkus'] & attendance['Dažnas'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(party_days['Kelios'] | module_rating['Vidutinis'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(party_days['Didžioji dalis'] & module_rating['Lengvas'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(attendance['Retas'] & party_days['Beveik neegzistuojančios'] & module_rating['Vidutinis'],
              MODULE_SCORE['Pažangus']),
    ctrl.Rule(attendance['Vidutinis'] | party_days['Kelios'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(~module_rating['Sunkus'], MODULE_SCORE['Pažangus']),
    ctrl.Rule(module_rating['Sunkus'] & attendance['Retas'], MODULE_SCORE['Prastas']),
    ctrl.Rule(party_days['Didžioji dalis'] | attendance['Retas'], MODULE_SCORE['Prastas']),
    ctrl.Rule(module_rating['Sunkus'] & party_days['Kelios'] & attendance['Retas'], MODULE_SCORE['Prastas']),
    ctrl.Rule(module_rating['Sunkus'] & party_days['Didžioji dalis'], MODULE_SCORE['Prastas']),
    ctrl.Rule(attendance['Retas'] & module_rating['Sunkus'] & party_days['Didžioji dalis'], MODULE_SCORE['Prastas'])
]
module_score_ctrl = ctrl.ControlSystem(rules)
score = ctrl.ControlSystemSimulation(module_score_ctrl)

score.input['module_rating'] = 5
score.input['attendance'] = 50
score.input['party_days'] = 4

score.compute()

print(score.output['MODULE_SCORE'])
MODULE_SCORE.view(sim=score)

plt.show()
