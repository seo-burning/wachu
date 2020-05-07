import os_setup
from functools import partial
import multiprocessing as mp
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

dateInfo = datetime.datetime.now().strftime('%Y-%m-%d')


def create_presigned_url(bucket_name, object_name, expiration=6048000):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RS3GZCVURG',
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


def video_file_update(obj_post):
    url = obj_post.video_source
    response = requests.get(url, stream=True)
    store_name = obj_post.store.insta_id
    object_name = str(obj_post.post_taken_at_timestamp) + '.mp4'
    file_root = './crawling/'+store_name + '_' + object_name
    with open(file_root, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RS3GZCVURG',
                             aws_secret_access_key='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', config=Config(signature_version='s3v4'))
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', '{media}/{video}/{store}/{file_name}'.format(
            media='media', video='video', store=store_name, file_name=object_name))
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/media/video/{store}/{file_name}".format(
        store=store_name, file_name=object_name)
    video_source = create_presigned_url('wachu', 'media/video/{store}/{file_name}'.format(
        store=store_name, file_name=object_name, expiration=6048000))
    obj_post.video_source = video_source
    obj_post.save()
    os.remove(file_root)
    del response


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

    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RS3GZCVURG',
                             aws_secret_access_key='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', config=Config(signature_version='s3v4'))

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


def video_file_update_credential(obj_post):
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


def video_credential_update_for_all():
    pool = mp.Pool(processes=6)
    store_obj_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')
    i = 0
    for store_obj in store_obj_list:
        i = i + 1
        print(i, store_obj)
        obj_post_list = StorePost.objects.all().filter(store=store_obj, post_type='V')
        pool.map(partial(video_file_update_credential), obj_post_list)
    pool.close()


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
    s3_client = boto3.client('s3', aws_access_key_id='AKIA3KMPT5RS3GZCVURG',
                             aws_secret_access_key='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', config=Config(signature_version='s3v4'))
    with open(file_root, 'rb') as f:
        s3_client.upload_fileobj(f, 'wachu', upload_root)
    video_source = "https://s3.console.aws.amazon.com/s3/object/wachu/"+upload_root
    video_source = create_presigned_url(
        'wachu', upload_root, expiration=6048000)


def resize_thumbnail_by_store(store_obj):
    store_name = store_obj.insta_id
    try:
        image_source = store_obj.recent_post_1
        resize_file_root = './crawling/temp/'+store_name+'_resize.jpg'
        resize_file_root_s3 = 'media/picture/{store}/thumbnail/+'.format(
            store=store_name)+dateInfo+'thumb_1.jpg'
        resize_in_ratio(image_source, 300, resize_file_root, 65)
        upload_to_s3(resize_file_root, resize_file_root_s3)
        os.remove(resize_file_root)
        presigned_url_1 = create_presigned_url('wachu', resize_file_root_s3)
        store_obj.recent_post_1 = presigned_url_1
    except:
        print('error')
        pass
    try:
        thumb_2_image_source = store_obj.recent_post_2
        thumb_2_resize_file_root = './crawling/temp/'+store_name+'_resize_1.jpg'
        thumb_2_resize_file_root_s3 = 'media/picture/{store}/thumbnail/+'.format(
            store=store_name)+dateInfo+'thumb_2.jpg'
        resize_in_ratio(thumb_2_image_source, 300,
                        thumb_2_resize_file_root, 65)
        upload_to_s3(thumb_2_resize_file_root, thumb_2_resize_file_root_s3)
        os.remove(thumb_2_resize_file_root)
        presigned_url_2 = create_presigned_url(
            'wachu', thumb_2_resize_file_root_s3)
        store_obj.recent_post_2 = presigned_url_2
    except:
        print('error')
        pass
    try:
        thumb_3_image_source = store_obj.recent_post_3
        thumb_3_resize_file_root = './crawling/temp/'+store_name+'_resize_2.jpg'
        thumb_3_resize_file_root_s3 = 'media/picture/{store}/thumbnail/+'.format(
            store=store_name)+dateInfo+'thumb_3.jpg'
        resize_in_ratio(thumb_3_image_source, 300,
                        thumb_3_resize_file_root, 65)
        upload_to_s3(thumb_3_resize_file_root, thumb_3_resize_file_root_s3)
        os.remove(thumb_3_resize_file_root)
        presigned_url_3 = create_presigned_url(
            'wachu', thumb_3_resize_file_root_s3)
        store_obj.recent_post_3 = presigned_url_3
    except:
        print('error')
        pass
    store_obj.save()


def video_update_credential(obj_post):
    post_image_obj_list = PostImage.objects.all().filter(
        store_post=obj_post, post_image_type='V')
    if len(post_image_obj_list) > 0:
        print(post_image_obj_list)


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

    # post_image_obj_list = PostImage.objects.all().filter(store_post=obj_post, post_image_type='V')
    # print(len(post_image_obj_list))
    # if len(post_image_obj_list) > 0:
    #     print(post_image_obj_list[0].store_post.pk)

    # store_obj_list = Store.objects.all().filter(is_active=True).order_by('current_ranking')[62:63]
    # obj_post_list = StorePost.objects.all().filter(store=store_obj_list)
    # for obj_post in obj_post_list:
    #     post_image_obj_list = PostImage.objects.all().filter(store_post=obj_post, post_image_type='V')
    # print(len(post_image_obj_list))


def video_credential_update_for_MP_store(store_obj):
    obj_post_list = StorePost.objects.all().filter(store=store_obj)
    print(store_obj.current_ranking, store_obj.insta_id)
    for obj_post in obj_post_list:
        post_image_obj_list = PostImage.objects.all().filter(
            store_post=obj_post, post_image_type='V')
        print(len(post_image_obj_list))
        video_update_credential(obj_post)


def video_credential_update_for_all_MP():
    store_obj_list = Store.objects.all().filter(
        is_active=True).order_by('current_ranking')[63:65]
    pool = mp.Pool(processes=6)
    print(len(store_obj_list))
    pool.map(video_credential_update_for_MP_store, store_obj_list)
    pool.close


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


if __name__ == '__main__':
    print('start scrapying')
    print('setup multiprocessing')
    video_credential_update_for_all()
    video_credential_update_for_all_MP()
    update_profile_credenttial()
