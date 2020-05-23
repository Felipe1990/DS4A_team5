import os
from utils_aws import upload_files_to_s3

os.chdir('../../')

keys_aws = {'AWS_ACCESS_KEY': ' AKIARQBCIP76L6XVXIVQ',
            'AWS_SECRET_ACCESS_KEY': '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',
            'S3_BUCKET_NAME': 'ds4ateam5'}
            
files_to_upload = ['data/procesada/data_with_index.pkl',
                   'data/procesada/data_with_index_nodups.pkl',
                   'data/procesada/data_plus_census.pkl',
                   'data/procesada/data_plus_census_added_features.pkl']

upload_files_to_s3(keys_aws, files_to_upload)