import os
from utils_aws import download_data_team5

os.chdir('../../')

keys_aws = {'AWS_ACCESS_KEY': ' AKIARQBCIP76L6XVXIVQ',
            'AWS_SECRET_ACCESS_KEY': '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',
            'S3_BUCKET_NAME': 'ds4ateam5'}

download_data_team5(keys_aws)