import geopandas as gpd
# import base64
# import datetime
# import json
import numpy as np
import pandas as pd
from shapely.geometry import Point
import os

class CurrentLabels:
    """
    Start with the labeled databse, including lat and long and add the code sector (census_code) column
    """

    def __init__(self, path_to_file):
        self.df = pd.read_csv(path_to_file, dtype='str')

    def adjust_nas(self):
        self.df = (self.df
                   .fillna(value={'model_decision': 'NA_string',
                                  'analyst_decision': 'NA_string'})
                   .dropna(subset=['coordinates']).reset_index(drop=True)
        )

    def create_long_lant_cols(self):
        self.df['long'] = pd.to_numeric(self.df.coordinates.str.split(',', expand=True).loc[:,0].str.replace('\(', ''))
        self.df['lat'] = pd.to_numeric(self.df.coordinates.str.split(',', expand=True).loc[:,1].str.replace('\)', ''))
        self.df['state'] = self.df.concat.apply(lambda row: row.split(',')[-1].lower().strip())

        self.df['coordinate_point'] = pd.Series([], dtype='object')
        for idx, row in self.df.iterrows():
            self.df.loc[idx, 'coordinate_point'] = Point(row.long, row.lat)
        
    def drop_cols(self):
        self.df = self.df.drop(columns=['zip_code', 'coordinates', 'Unnamed: 0'])

    def join_sector_code(self):
                
        def join_code_sector_inner(df):
            
            assert len(df.state.unique()) == 1, ('Más de un estado presente en la base')
            state = df.state.unique()[0]
            
            inner_df = df.copy()
            
            if state in os.listdir('data/sharp'):
                file_name = [file for file in os.listdir('data/sharp/'+state) if file.find('.shp')>0][0]
                census_sector = gpd.read_file('data/sharp/{0:s}/{1:s}'.format(state, file_name), encoding='latin1')
                inner_df['census_code'] = inner_df['coordinate_point'].apply(lambda row: census_sector.loc[census_sector.contains(row), 'CD_GEOCODI'].values).str[0]
            
            else :
                inner_df['census_code'] = np.nan
                
            return inner_df
            
        self.df = (self.df
                    .assign(state_index=lambda x: x.state)
                    .groupby('state_index')
                    .apply(lambda df: join_code_sector_inner(df))
                    .reset_index(drop=True)
                   )
    
    def save_df(self, path_to_save='data/procesada/data_with_index.pkl'):
        self.df.to_pickle(path_to_save)

class DataWithDups:

    def __init__(self, path_to_file='data/procesada/data_with_index.pkl'):
        self.df = pd.read_pickle(path_to_file)

    def drop_nas_in_sector(self):
        self.df = self.df.dropna(subset=['census_code'])

    def print_dups(self):
        print('{0:.1%} de la base tiene duplicados'
              .format(self.df
                      .duplicated(subset=['lat', 'long', 'concat'], keep=False)
                      .mean())
                      )
    def unify_decision(self):
        self.df = (self.df
                   .assign(final_decision=lambda x: np.where(x.analyst_decision.isin(['A', 'R']),
                                                             x.analyst_decision, 
                                                             np.where(x.model_decision.isin(['A', 'R']),
                                                                      x.model_decision,
                                                                      'undefined')))
                   .drop(columns=['model_decision', 'analyst_decision'])
                  )
    
    def remove_duplicates(self):
        self.df = (self.df
                   .assign(uno=1)
                   .groupby(['state','census_code', 'concat', 'lat', 'long','final_decision'])
                   .agg(count=('uno', sum))
                   .reset_index()
                   .assign(random_index=lambda x: np.random.normal(size=x.shape[0]))
                   .sort_values(by=['state', 'concat', 'lat', 'long','count', 'random_index'], ascending=False)
                   .drop_duplicates(subset=['census_code', 'concat', 'state', 'lat', 'long'], keep='first')
                   .drop(columns=['count', 'random_index'])
                   .reset_index(drop=True)
                   )

    def save_df(self, path_to_save='data/procesada/data_with_index_nodups.pkl'):
        self.df.to_pickle(path_to_save)


class FinalLabelsWithSector:

    def __init__(self, path_to_file='data/procesada/data_with_index_nodups.pkl'):
        self.df = pd.read_pickle(path_to_file)
        self.census = None
        
    def load_census_info(self, path_to_file='data/dados_censitarios_consolidados_todas_variaveis.csv'):
        self.census = pd.read_csv(path_to_file, dtype='str')
    
    def process_census_info(self, exclude_columns, cat_columns, str_columns):

        # adjust column types
        num_columns = [var_i for var_i in self.census.columns if var_i not in cat_columns + str_columns]
        for cat_i in cat_columns:
            self.census[cat_i] = self.census[cat_i].astype('category')

        for num_i in num_columns:
            self.census[num_i] = pd.to_numeric(self.census[num_i].str.replace(',', '.'), errors='coerce')   

        # drop excluded columns
        self.census = self.census.drop(columns=exclude_columns)

        # hot encoding category columns
        self.census = pd.get_dummies(self.census, columns=cat_columns)

    def join_census_info(self):
        self.df = self.df.merge(self.census,left_on='census_code', right_on='Cod_setor', how='left')
        self.census = None

    def save_df(self, path_to_save='data/procesada/data_plus_census.pkl'):
        self.df.to_pickle(path_to_save)


class DataLabelAndFeatures:

    def __init__(self, path_to_file='data/procesada/data_plus_census.pkl'):
        self.df = pd.read_pickle(path_to_file)

    def create_pct_total_vars(self, name_total_var, list_vars):
        self.df[name_total_var] = self.df.loc[:, list_vars].sum(axis=1)

        for var_i in list_vars:
            self.df[var_i + '_pct'] = self.df[var_i] / self.df[name_total_var]

    def save_df(self, path_to_save='data/procesada/data_plus_census_added_features.pkl'):
        self.df.to_pickle(path_to_save)