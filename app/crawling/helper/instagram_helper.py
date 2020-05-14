import os
from helper.image_processing import create_presigned_url, upload_file, resize_in_ratio, upload_to_s3


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
