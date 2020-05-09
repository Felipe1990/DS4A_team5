import pandas as pd
import os

os.chdir('../data/')

dt_cns_tds_vrbls = pd.read_csv('dados_censitarios_consolidados_todas_variaveis.csv', dtype='str')
dt_cns_tds_vrbls = dt_cns_tds_vrbls.query('Cod_RM=="20"')

# dict_names = dt_cns_tds_vrbls[[ 'Cod_Grandes Regiões','Cod_RM',
#                                'Cod_UF', 'Cod_bairro', 'Cod_distrito', 
#                                'Cod_meso','Cod_micro', 'Cod_municipio',
#                                'Cod_subdistrito', 'Nome_Grande_Regiao',
#                                'Nome_da_RM', 'Nome_da_UF ',
#                                'Nome_da_meso', 'Nome_da_micro',
#                                'Nome_do_bairro', 'Nome_do_distrito',
#                                'Nome_do_municipio', 'Nome_do_subdistrito']].drop_duplicates(keep='first')

dt_cns_tds_vrbls = (dt_cns_tds_vrbls
                   .drop(columns=['Unnamed: 0', 'Nome_Grande_Regiao', 'Nome_da_RM',
                                  'Nome_da_UF ', 'Nome_da_meso', 'Nome_da_micro',
                                  'Nome_do_bairro', 'Nome_do_distrito', 'Nome_do_municipio',
                                  'Nome_do_subdistrito'])
                   )

cat_vars = ['Tipo_setor', 'Situacao_setor']
str_vars = ['Cod_Grandes Regiões','Cod_RM',
            'Cod_UF', 'Cod_bairro', 'Cod_distrito', 
            'Cod_meso','Cod_micro', 'Cod_municipio',
            'Cod_subdistrito', 'Cod_setor']

num_vars = [var_i for var_i in dt_cns_tds_vrbls.columns if var_i not in cat_vars + str_vars]

for cat_i in cat_vars:
    dt_cns_tds_vrbls[cat_i] = dt_cns_tds_vrbls[cat_i].astype('category')

for num_i in num_vars:
    dt_cns_tds_vrbls[num_i] = pd.to_numeric(dt_cns_tds_vrbls[num_i].str.replace(',', '.'), errors='coerce')    

dt_cns_tds_vrbls = pd.get_dummies(dt_cns_tds_vrbls, columns=cat_vars)

dt_cns_tds_vrbls = dt_cns_tds_vrbls.dropna()

# print(dt_cns_tds_vrbls.shape)

dt_cns_tds_vrbls.to_csv('procesada/data_censo_sp.csv', index=False)

## upload to mongo

# mongoimport --host Cluster0-shard-0/cluster0-shard-00-00-2stua.mongodb.net:27017,cluster0-shard-00-01-2stua.mongodb.net:27017,cluster0-shard-00-02-2stua.mongodb.net:27017 --ssl --username felipe_A --password cambio09 --authenticationDatabase admin --db DS4A --collection census_information --type csv --file data_censo_sp.csv --headerline