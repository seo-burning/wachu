import logging
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
import requests

import shutil
import sys
import os
import django
import json
import requests
from botocore.client import Config


PROJECT_ROOT = os.getcwd()
sys.path.append(os.path.dirname(PROJECT_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.prod")
django.setup()
from store.models import Store, StorePost, StoreRanking, PostImage

def create_presigned_url(bucket_name, object_name, expiration=604800):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RSQB24EN2B', 
    aws_secret_access_key='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')
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


def upload_file(file_name, bucket, store_name='ETC',object_name='no-name.mp4'):
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
        response = s3_client.upload_file(file_name, bucket, '{media}/{video}/{store}/{file_name}'.format(media='media', video='video',store=store_name, file_name=object_name))
    except ClientError as e:
        logging.error(e)
        return False
    return True

def video_file_update(obj_post):
    url = obj_post.video_source
    response = requests.get(url, stream=True)
    store_name= obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    file_root = './crawling/'+store_name + '_' + object_name
    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RSQB24EN2B', 
    aws_secret_access_key='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', config=Config(signature_version='s3v4'))
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/{file_name}'.format(media='media', video='video',store=store_name, file_name=object_name))
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/{file_name}".format(store=store_name, file_name=object_name)
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(store=store_name, file_name=object_name, expiration=604800))
    obj_post.video_source = video_source
    obj_post.save()
    os.remove(file_root)
    del response

def video_file_update_with_video_source(obj_post,video_source,video_thumbnail):
    url = video_source
    response = requests.get(url, stream=True)
    response_thumb = requests.get(video_thumbnail, stream=True)

    store_name= obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    thumb_name = str(obj_post.post_taken_at_timestamp) + '.jpg'

    file_root = './crawling/'+store_name + '_' + object_name
    thumb_file_root = './crawling/'+store_name + '_' + thumb_name

    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    with open(thumb_file_root, 'wb') as out_file:
        shutil.copyfileobj(response_thumb.raw, out_file)

    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RSQB24EN2B', 
    aws_secret_access_key='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', config=Config(signature_version='s3v4'))


    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/{file_name}'.format(media='media', video='video',store=store_name, file_name=object_name))
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/{file_name}".format(store=store_name, file_name=object_name)
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(store=store_name, file_name=object_name, expiration=604800))



    with open(thumb_file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/thumbnail/{file_name}'.format(media='media', video='video', store=store_name, file_name=thumb_name))
    post_thumb_image = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/thumbnail/{file_name}".format(store=store_name, file_name=thumb_name)
    post_thumb_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(store=store_name, file_name=thumb_name, expiration=604800))
    obj_post.video_source = video_source
    obj_post.post_thumb_image = post_thumb_image
    obj_post.save()
    os.remove(file_root)
    os.remove(thumb_file_root)
    del response



def video_file_update_credential(obj_post):
    store_name= obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    thumb_name = str(obj_post.post_taken_at_timestamp) + '.jpg'

    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(store=store_name, file_name=object_name, expiration=604800))
    post_thumb_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(store=store_name, file_name=thumb_name, expiration=604800))
    obj_post.video_source = video_source
    obj_post.post_thumb_image = post_thumb_image
    obj_post.save()



import multiprocessing as mp
from functools import partial


def video_update_credential(obj_post):
    post_image_obj_list = PostImage.objects.all().filter(store_post=obj_post, post_image_type='V')
    if len(post_image_obj_list) > 0:
        print(post_image_obj_list)

    
if __name__ == '__main__':
    print('start scrapying')
    print('setup multiprocessing')
    # pool = mp.Pool(processes=6)
    store_obj_list = Store.objects.all().filter(is_active=True).order_by('current_ranking')
    i=0
    for store_obj in store_obj_list:
        i = i + 1
        print(i, store_obj)
        obj_post_list = StorePost.objects.all().filter(store=store_obj)
        # pool.map(partial(video_update_credential),obj_post_list)
        for obj_post in obj_post_list:
            video_file_update_credential(obj_post)

    pool.close()