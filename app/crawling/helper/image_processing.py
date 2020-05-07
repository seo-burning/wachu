import os_setup
import logging
import boto3
from botocore.exceptions import ClientError
import requests
import shutil
from botocore.client import Config


def create_presigned_url(bucket_name, object_name, expiration=6048000):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def upload_file(file_name, bucket, store_name='ETC', object_name='no-name.mp4'):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file

    try:
        response = s3_client.upload_file(file_name, bucket, '{media}/{video}/{store}/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=object_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def resize_in_ratio(image_source, max_width_and_height, resize_source, quality=95):
    from PIL import Image
    response = requests.get(image_source, stream=True)
    file_root = './crawling/temp/temp.jpg'
    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    data = Image.open(file_root)
    source_width, source_height = data.size
    if source_width > source_height:
        result_ratio = source_width / max_width_and_height
        result_width = int(source_width / result_ratio)
        result_height = int(source_height / result_ratio)
    else:
        result_ratio = source_height / max_width_and_height
        result_width = int(source_width / result_ratio)
        result_height = int(source_height / result_ratio)
    result_data = data.resize((result_width, result_height))
    result_data.save(resize_source, 'JPEG', quality=quality)
    print(os.path.getsize(file_root), os.path.getsize(resize_source), '{}% 압축'.format(
        int((1 - os.path.getsize(resize_source)/os.path.getsize(file_root))*100)))
    os.remove(file_root)


def upload_to_s3(file_root, upload_root):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             config=Config(signature_version='s3v4'))
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', upload_root)
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/"+upload_root
    video_source = create_presigned_url(
        'wachu', upload_root, expiration=6048000)
