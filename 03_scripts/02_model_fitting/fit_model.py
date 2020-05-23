import os
import pandas as pd
from fit_model_class import PropertyModel

os.chdir('../../')

data = pd.read_pickle('data/procesada/data_plus_census.pkl')

model_property = PropertyModel()
model_property.split_data_label_features(data)
model_property.fit_model_in_validation()
model_property.print_model_metrics()
model_property.fit_model_whole_data()
model_property.save_model()
model_property.save_feature_col_names()
