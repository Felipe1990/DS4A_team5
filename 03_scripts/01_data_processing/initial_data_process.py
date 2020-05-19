# process data
import os
from data_preparation_classes import CurrentLabels, DataWithDups, FinalLabelsWithSector, DataLabelAndFeatures
from utils_aws import upload_files_to_s3

#
os.chdir('../../')
keys_aws = {'AWS_ACCESS_KEY': ' AKIARQBCIP76L6XVXIVQ',
            'AWS_SECRET_ACCESS_KEY': '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',
            'S3_BUCKET_NAME': 'ds4ateam5'}

#
# labels = CurrentLabels('data/Copy of registry.csv')
# labels.adjust_nas()
# labels.create_long_lant_cols()
# labels.drop_cols()
# labels.join_sector_code()
# labels.save_df()
# labels = None
# print('initial labes processed')

#
# data_dups = DataWithDups()
# data_dups.drop_nas_in_sector()
# data_dups.print_dups()
# data_dups.unify_decision()
# data_dups.remove_duplicates()
# data_dups.save_df()
# data_dups = None
# print('data duplication process finished')

#
# exclude_columns = ['Unnamed: 0', 'Nome_Grande_Regiao', 'Nome_da_RM',
#                    'Nome_da_UF ', 'Nome_da_meso', 'Nome_da_micro',
#                    'Nome_do_bairro', 'Nome_do_distrito', 'Nome_do_municipio',
#                    'Nome_do_subdistrito']
                   
# cat_columns = ['Tipo_setor', 'Situacao_setor',
#                'Cod_Grandes Regiões','Cod_RM']
# str_columns = ['Cod_UF', 'Cod_bairro', 'Cod_distrito', 
#                'Cod_meso','Cod_micro', 'Cod_municipio',
#                'Cod_subdistrito', 'Cod_setor']

# data_with_label = FinalLabelsWithSector()
# data_with_label.load_census_info()
# data_with_label.process_census_info(exclude_columns=exclude_columns, cat_columns=cat_columns, str_columns=str_columns)
# data_with_label.join_census_info()
# data_with_label.save_df()
# data_with_label = None
# print('add census labels')
# #

list_vars = ['DOMICILIO_RENDA_V001', 'DOMICILIO_RENDA_V005', 'DOMICILIO_RENDA_V006',
                  'DOMICILIO_RENDA_V007', 'DOMICILIO_RENDA_V008', 'DOMICILIO_RENDA_V009',
                  'DOMICILIO_RENDA_V010',  'DOMICILIO_RENDA_V011', 'DOMICILIO_RENDA_V012',
                  'DOMICILIO_RENDA_V013', 'DOMICILIO_RENDA_V014']
name_total_var = 'total_domicilios'

data_features = DataLabelAndFeatures()
data_features.create_pct_total_vars(name_total_var, list_vars)
data_features.save_df()
data_features = None
print('create additional features')

# upload
files_to_upload = ['data/procesada/data_with_index.pkl',
                   'data/procesada/data_with_index_nodups.pkl',
                   'data/procesada/data_plus_census.pkl',
                   'data/procesada/data_plus_census_added_features.pkl']

upload_files_to_s3(keys_aws, files_to_upload)
