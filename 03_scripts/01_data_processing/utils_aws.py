import boto3
import os

def download_data_team5(keys_aws):
    """
    Download all the necesary information from the S3 Bucket

    Parameters
    -----------

    keys_aws: dict
        Dictionary with the expected following keys: AWS_ACCESS_KEY, AWS_ACCESS_KEY, S3_BUCKET_NAME
    """

    s3_client = boto3.resource(
        's3',
        aws_access_key_id=keys_aws['AWS_ACCESS_KEY'],
        aws_secret_access_key=keys_aws['AWS_SECRET_ACCESS_KEY']
    )

    s3_bucket = s3_client.Bucket(keys_aws['S3_BUCKET_NAME'])
    local_folder = '.'

    for obj in s3_bucket.objects.all():
        local_file = os.path.join(local_folder, obj.key)
        
        for i in range(len(obj.key.split('/')[:-1])):
            dir_name = '/'.join(obj.key.split('/')[0:i+1])
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            
        if not os.path.exists(local_file):
            s3_bucket.download_file(obj.key, local_file)
            print(obj.key + '\tdownloaded')

        else:
            print(obj.key + '\talready exists')




def upload_files_to_s3(keys_aws, files):
    """
    Uploads selected files to the S3 Bucket

    Parameters
    -----------

    keys_aws: dict
        Dictionary with the expected following keys: AWS_ACCESS_KEY, AWS_ACCESS_KEY, S3_BUCKET_NAME

    files: list
        List of relative paths of the files to be uploaded
    """
    
    s3_client = boto3.resource(
        's3',
        aws_access_key_id=keys_aws['AWS_ACCESS_KEY'],
        aws_secret_access_key=keys_aws['AWS_SECRET_ACCESS_KEY']
    )

    s3_bucket = s3_client.Bucket(keys_aws['S3_BUCKET_NAME'])

    for file_i in files:
        s3_bucket.upload_file(file_i, file_i)
