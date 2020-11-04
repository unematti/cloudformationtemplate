import boto3




s3 = boto3.resource('s3')
bucket = s3.Bucket('templates-cmdrunematti')
exists = True

try:
    s3.meta.client.head_bucket(Bucket='templates-cmdrunematti')
except botocore.exceptions.ClientError as e:
    # If a client error is thrown, then check that it was a 404 error.
    # If it was a 404 error, then the bucket does not exist.
    error_code = e.response['Error']['Code']
    if error_code == '404':
        exists = False

def upload_file(file_name, bucket, folder_name=None, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = folder_name + '/' + file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return False
    return True

upload_file('cloudformation.yaml', 'templates-cmdrunematti', folder_name='templates')
print('first dun')

upload_file('Autoscale.yaml', 'templates-cmdrunematti', folder_name='templates')
print('all dun')
