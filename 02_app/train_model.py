
# model creation
import pandas as pd
import os 
import pickle
import numpy as np
import joblib


from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler


os.chdir('../data/')

data = pd.read_pickle('procesada/data_plus_census.pkl')
data = data.query('state=="sp"').dropna()

options_vars = [col for col in data.dtypes.index if data.dtypes[col]!='object']

variable_to_exclude = ['DOMICILIO_RENDA_V004', 'Tipo_setor_7',
                        'PESSOA_RENDA_V065', 'PESSOA_RENDA_V131',
                        'Tipo_setor_2', 'Tipo_setor_3',
                        'Tipo_setor_8', 'Tipo_setor_6',
                        'Tipo_setor_5', 'Tipo_setor_4',
                        'Situacao_setor_6', 'Situacao_setor_7',
                        'lat', 'long', 'Tipo_setor_2',
                        'Tipo_setor_2']

features = data[[x for x in data.columns if data[x].dtype!='object']]
features = features.drop(columns=variable_to_exclude)
label = pd.to_numeric(data.final_decision=='A').astype(np.int8)

scaler = StandardScaler()

X_train, X_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=42)

features_escaled = data[options_vars]
features_escaled = pd.DataFrame(scaler.fit_transform(features_escaled), columns=features_escaled.columns)

index_A = data.query('final_decision=="A"').index
index_not_A = data.query('final_decision!="A"').index


rf_acceptance = RandomForestClassifier(n_estimators=100)
rf_acceptance.fit(X_train, y_train)

model_acceptance = SelectFromModel(rf_acceptance, prefit=True, max_features=31)
relevant_variables_rf = [var for idx, var in enumerate(X_train.columns.tolist()) if list(model_acceptance.get_support())[idx]]

model_acceptance = RandomForestClassifier(n_estimators=100).fit(X_train.loc[:,relevant_variables_rf], y_train)
print(accuracy_score(y_test, model_acceptance.predict(X_test.loc[:,relevant_variables_rf])))
print(relevant_variables_rf)

# final model fit
final_scaler = StandardScaler()

features_escaled = features.loc[:,relevant_variables_rf]
features_escaled = pd.DataFrame(final_scaler.fit_transform(features_escaled), columns=features_escaled.columns)


model_acceptance = RandomForestClassifier(n_estimators=100).fit(features_escaled, label)


# save var names
filename_colnames = 'var_names.pkl'
with open(filename_colnames, 'wb') as f:
    pickle.dump(relevant_variables_rf, f)

# save scaler
filename_scaler = 'feature_scaler.pkl'
with open(filename_scaler, 'wb') as f:
    pickle.dump(final_scaler, f)

# save model
filename = 'acceptance_model.sav'
joblib.dump(model_acceptance, filename)

# test re load
loaded_model = joblib.load(filename)
print(loaded_model.score(features_escaled, label))


