import pandas as pd
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def build_and_run_model(file, lrate):
    data = pd.read_csv(file)
    data.head()

    inp = data.loc[:, data.columns != 'MALICIOUS_OFFENSE']
    inp.head()

    output = data.loc[:, 'MALICIOUS_OFFENSE']
    output.head()

    train = []
    train_out = []
    test = []
    test_out = []
    for i in range(len(data.values)):
        if i % 10 == 0:
            test.append(list(inp.values[i]))
            test_out.append(output.values[i])
        else:
            train.append(list(inp.values[i]))
            train_out.append(output.values[i])

    model = make_pipeline(StandardScaler(), SGDRegressor(power_t=lrate))
    model.fit(train, train_out)
    prediction = model.predict(test)
    print('------Modelis (mokymosi greitis = ', lrate, ')------')
    print('Vidutinė kvadratinės prognozės klaida (MSE) = ', mean_squared_error(test_out, prediction))
    print('Prognozės absoliutaus nuokrypio mediana (MAD) = ', mean_absolute_error(test_out, prediction))


build_and_run_model('attacks.csv', 0.8)
build_and_run_model('attacks.csv', 0.2)
