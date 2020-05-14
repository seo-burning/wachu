import os_setup
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
import datetime
from store.models import Store, StorePost, StoreRanking, PostImage
from product.models import Product, ProductImage
from helper.image_processing import create_presigned_url, upload_file, resize_in_ratio, upload_to_s3
dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')

AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')


def video_file_update_with_video_source(obj_post, video_source, video_thumbnail):
    url = video_source
    response = requests.get(url, stream=True)
    response_thumb = requests.get(video_thumbnail, stream=True)

    store_name = obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    thumb_name = str(obj_post.post_taken_at_timestamp) + '.jpg'

    file_root = './crawling/'+store_name + '_' + object_name
    thumb_file_root = './crawling/'+store_name + '_' + thumb_name

    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    with open(thumb_file_root, 'wb') as out_file:
        shutil.copyfileobj(response_thumb.raw, out_file)

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=object_name))
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/{file_name}".format(
        store=store_name, file_name=object_name)
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(
        store=store_name, file_name=object_name, expiration=6048000))

    with open(thumb_file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/thumbnail/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=thumb_name))
    post_thumb_image = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/thumbnail/{file_name}".format(
        store=store_name, file_name=thumb_name)
    post_thumb_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(
        store=store_name, file_name=thumb_name, expiration=6048000))
    obj_post.video_source = video_source
    obj_post.post_thumb_image = post_thumb_image
    obj_post.save()
    os.remove(file_root)
    os.remove(thumb_file_root)
    del response


def video_file_update_with_video_source_post_product_image(obj_image, video_source, video_thumbnail):
    url = video_source
    response = requests.get(url, stream=True)
    response_thumb = requests.get(video_thumbnail, stream=True)

    store_name = obj_image.store_post.store.insta_id

    object_name = str(obj_image.store_post.pk)+'-'+str(obj_image.pk) + '.mp4'
    thumb_name = str(obj_image.store_post.pk)+'-'+str(obj_image.pk) + '.jpg'

    file_root = './crawling/'+store_name + '_' + object_name
    thumb_file_root = './crawling/'+store_name + '_' + thumb_name

    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    with open(thumb_file_root, 'wb') as out_file:
        shutil.copyfileobj(response_thumb.raw, out_file)

    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=object_name))
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/{file_name}".format(
        store=store_name, file_name=object_name)
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(
        store=store_name, file_name=object_name, expiration=6048000))

    with open(thumb_file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/thumbnail/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=thumb_name))
    post_thumb_image = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/thumbnail/{file_name}".format(
        store=store_name, file_name=thumb_name)
    post_thumb_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(
        store=store_name, file_name=thumb_name, expiration=6048000))
    obj_image.source = video_source
    obj_image.source_thumb = post_thumb_image
    obj_image.save()
    os.remove(file_root)
    os.remove(thumb_file_root)
    del response


def _video_file_update_credential_post(obj_post):
    print('update video credential')
    print(obj_post.pk)
    store_name = obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    thumb_name = str(obj_post.post_taken_at_timestamp) + '.jpg'
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(
        store=store_name, file_name=object_name, expiration=6048000))
    post_thumb_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(
        store=store_name, file_name=thumb_name, expiration=6048000))
    obj_post.video_source = video_source
    obj_post.post_thumb_image = post_thumb_image
    obj_post.save()


def _video_file_update_credential_product(obj_product):
    print('update video credential')
    print(obj_product.pk)
    store_name = obj_product.store.insta_id
    object_name = str(obj_product.post.post_taken_at_timestamp) + '.mp4'
    thumb_name = str(obj_product.post.post_taken_at_timestamp) + '.jpg'
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(
        store=store_name, file_name=object_name, expiration=6048000))
    product_thumbnail_image = create_presigned_url('wachu', 'media/video/{store}/thumbnail/{file_name}'.format(
        store=store_name, file_name=thumb_name, expiration=6048000))
    obj_product.video_source = video_source
    obj_product.product_thumbnail_image = product_thumbnail_image
    obj_product.save()


def video_credential_update_for_all():
    obj_post_list = StorePost.objects.all().filter(post_type='V')
    for obj_post in obj_post_list:
        _video_file_update_credential_post(obj_post)
    obj_product_list = Product.objects.all().filter(product_image_type='V')
    for obj_product in obj_product_list:
        _video_file_update_credential_product(obj_product)
    post_image_obj_list = PostImage.objects.all().filter(post_image_type='V')
    for post_image_obj in post_image_obj_list:
        _post_image_video_update_credential(post_image_obj)


def _post_image_video_update_credential(post_image_obj):
    pass


def resize_profile_image_by_store():
    store_obj_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')
    for store_obj in store_obj_list:
        resize_profile_image_by_store(store_obj)
        store_name = store_obj.insta_id
        try:
            upload_root = 'media/picture/{store}/thumbnail/+'.format(
                store=store_name)+'profile_thumb.jpg'
            url_source = "https://s3.console.aws.amazon.com/s3/object/wachu/"+upload_root
            presigned_url = create_presigned_url('wachu', url_source)
            store_obj.profile_image = presigned_url
        except:
            print('error')
            pass
        store_obj.save()


def update_profile_credenttial():
    store_obj_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')
    for store_obj in store_obj_list:
        store_name = store_obj.insta_id
        try:
            resize_file_root_s3 = 'media/picture/{store}/thumbnail/+'.format(
                store=store_name)+'profile_thumb.jpg'
            presigned_url = create_presigned_url('wachu', resize_file_root_s3)
            store_obj.profile_image = presigned_url
            print('success')
        except:
            print('error')
            pass
        store_obj.save()
