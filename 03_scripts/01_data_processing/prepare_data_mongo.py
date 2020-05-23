import os
from data_preparation_classes import DataForMongo

os.chdir('../../')

data_for_mongo = DataForMongo()

exclude_columns = ['Unnamed: 0', 'Nome_Grande_Regiao', 'Nome_da_RM',
                   'Nome_da_UF ', 'Nome_da_meso', 'Nome_da_micro',
                   'Nome_do_bairro', 'Nome_do_distrito', 'Nome_do_municipio',
                   'Nome_do_subdistrito']
                   
cat_columns = ['Tipo_setor', 'Situacao_setor',
               'Cod_Grandes Regiões','Cod_RM']
str_columns = ['Cod_UF', 'Cod_bairro', 'Cod_distrito', 
               'Cod_meso','Cod_micro', 'Cod_municipio',
               'Cod_subdistrito', 'Cod_setor']

data_for_mongo.process_census_info(exclude_columns=exclude_columns, cat_columns=cat_columns, str_columns=str_columns)
data_for_mongo.filter_state()

list_vars = ['DOMICILIO_RENDA_V001', 'DOMICILIO_RENDA_V005', 'DOMICILIO_RENDA_V006',
                  'DOMICILIO_RENDA_V007', 'DOMICILIO_RENDA_V008', 'DOMICILIO_RENDA_V009',
                  'DOMICILIO_RENDA_V010',  'DOMICILIO_RENDA_V011', 'DOMICILIO_RENDA_V012',
                  'DOMICILIO_RENDA_V013', 'DOMICILIO_RENDA_V014']
name_total_var = 'total_domicilios'

data_for_mongo.create_pct_total_vars(name_total_var, list_vars)

data_for_mongo.save_df()
data_for_mongo.upload_to_mongo()

# chmod a+rx