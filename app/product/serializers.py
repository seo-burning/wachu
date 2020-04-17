from rest_framework import serializers

from product import models
from publish.serializers import StorePostSerializer
from datetime import datetime, timezone, timedelta


class ProductSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    sub_category = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    post = StorePostSerializer(many=False)
    favorite_users_count = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = ('pk', 'is_new', 'name', 'tag',  'style',
                  'post', 'color', 'sub_category', 'price',
                  'category', 'thumb_image_pk', 'favorite_users_count')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'post', 'category',
            'style',
            'sub_category',
            'post__store',
            'post__store__age',
            'post__store__primary_style',
            'post__store__secondary_style')
        queryset = queryset.prefetch_related('tag',
                                             'post__post_image_set',
                                             'color',
                                             'post__store__category',
                                             )
        return queryset

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()

    def get_is_new(self, obj):
        is_new = False
        time_diff = datetime.now(timezone.utc) - obj.created_at - timedelta(2)
        if time_diff.days < 0:
            is_new = True
        return is_new


# {
#     "itemid": 4817479036,
#     "price_max_before_discount": 25000000000,
#     "image": "cac31a408857ac0d88b20631b5852e71",
#     "shopid": 31408791,
#     "currency": "VND",
#     "raw_discount": 2,
#     "show_free_shipping": false,
#     "images": [
#         "cac31a408857ac0d88b20631b5852e71",
#         "a0fa5dbde5cdcd927e5569c9fc43ff95",
#         "9bf39584a6e50c080c641ceaa658d7f7",
#         "c43bc29d1fd9a52ddfb8a7b0510ebeab",
#         "e57f851eb250ed2c0d6e94025a0dcda2",
#         "b8d81e0f27eb3952f8ca6bb38fca9e88",
#         "dc2fa18272ef403febafc46804f3f0d3"
#     ],
#     "price_before_discount": 25000000000,
#     "show_discount": 2,
#     "cmt_count": 14, //리뷰수
#     "view_count": 2443, //조회수
#     "catid": 77,
#     "price_min": 24500000000,
#     "liked_count": 89,
#     "price_min_before_discount": 25000000000,
#     "cb_option": 0,
#     "sold": 16,
#     "stock": 55,
#     "status": 1,
#     "price_max": 24500000000,
#     "price": 24500000000,
#     "item_rating": {
#         "rating_star": 4.785714,
#         "rating_count": [
#             14,
#             0,
#             1,
#             0,
#             0,
#             13
#         ],
#         "rcount_with_image": 3,
#         "rcount_with_context": 3
#     },
#     "tier_variations": [
#         {
#             "images": [
#                 "ec345ab7022b28be11dd8293bdf5b749",
#                 "194b1d2fc6f0ec785bcad84585a07d21",
#                 "9b7df5054c0ab09c87b3e2d608b40f51",
#                 "66ea368e644e802ea01a2487d9020b10",
#                 "25e11fb49a98f63559021d564927ffdf",
#                 "1ab840b03788c0f5d5dd22eea4390005",
#                 "feaa11228527d665ee5027b4765050e6"
#             ],
#             "properties": null,
#             "type": 0,
#             "name": "M\u00e0u ",
#             "options": [
#                 "Tr\u1eafng",
#                 "K\u1ebb xanh",
#                 "K\u1ebb s\u1ecdc \u0111en",
#                 "B\u00e3 tr\u1ea7u",
#                 "N\u00e2u ",
#                 "\u0110en tr\u1eafng",
#                 "Be"
#             ]
#         }
#     ],
#     "discount": "2%",
    
#     "name": "S\u01a1 mi oversize TKA209",

#     "ctime": 1582175115,
#     "label_ids": [
#         1000260,
#         1000268,
#         1000049,
#         1000051,
#         1000277,
#         1000278,
#         1000279,
#         1000255
#     ],
#     "historical_sold": 57,
#     "transparent_background_image": ""
# }