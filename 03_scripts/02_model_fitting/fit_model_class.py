import pandas as pd
import os
import joblib
import pickle
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.model_selection import RandomizedSearchCV, train_test_split
# from sklearn.linear_model import SGDClassifier
# import xgboost as xgb
from sklearn.metrics import accuracy_score, roc_auc_score, roc_curve, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Tran model

class PropertyModel:
    
    def __init__(self):
        self.seed = 2020
        self.X_test = None
        self.y_test = None
        self.model_rf = None
        self.label = None
        self.features = None
        self.dups_pct = None
        self.final_model = None
        self.features_col_names = None

    def split_data_label_features(self, data):
        self.dups_pct = data.isna().any(axis=1).mean() 
        data_no_dups = data.dropna()

        self.features = data_no_dups[[x for x in data_no_dups.columns if data_no_dups[x].dtype!='object']]
        self.label = pd.to_numeric(data_no_dups.final_decision=='A').astype(np.int8)

    def fit_model_in_validation(self):
        X_train, self.X_test, y_train, self.y_test = train_test_split(self.features, self.label, test_size=0.2, random_state=self.seed)

        rf_acceptance = RandomForestClassifier(n_estimators=50)
        pipeline_rf = Pipeline([('scaler', StandardScaler()),
                                ('select_model', SelectFromModel(rf_acceptance, prefit=False)),
                                ('model', RandomForestClassifier(random_state=self.seed))],
                            verbose = False)

        params_rf = {
            'model__n_estimators': [100, 200, 500],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 5, 10]
        }

        self.features_col_names = X_train.columns.tolist()
        self.model_rf = RandomizedSearchCV(pipeline_rf, params_rf, cv=5, random_state=self.seed, n_iter=5, verbose=0, n_jobs=-1)
        self.model_rf = self.model_rf.fit(X_train, y_train)

    def print_model_metrics(self):
        print('-------------------------\n')
        print('Best parameters from CV: {0}'.format(self.model_rf.best_params_))
        print('-------------------------\n')
        print('Best accuracy score in CV: {0:.3f}'.format(self.model_rf.best_score_))
        print('Best model accuracy score in test: {0:.3f}'.format(accuracy_score(self.y_test, self.model_rf.best_estimator_.predict(self.X_test))))
        print('Best model ROC in test: {0:.3f}'.format(roc_auc_score(self.y_test, self.model_rf.best_estimator_.predict_proba(self.X_test)[:,1])))
        print('-------------------------\n')
        print('Confussion matrix in test:\n')
        print(pd.crosstab(self.y_test, self.model_rf.best_estimator_.predict(self.X_test), normalize=True)*100)
        print('Classification report in test: \n')
        print(classification_report(self.y_test, self.model_rf.best_estimator_.predict(self.X_test)))

    def fit_model_whole_data(self):
        self.final_model =  self.model_rf.best_estimator_.fit(self.features, self.label)

    def save_model(self, model_file_name='acceptance_model.sav'):
        joblib.dump(self.final_model, '02_app/' + model_file_name)

    def save_feature_col_names(self, features_colnames_path = 'var_names.pkl'):
        with open('02_app/' + features_colnames_path, 'wb') as f:
            pickle.dump(self.features_col_names, f)