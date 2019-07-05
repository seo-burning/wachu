from rest_framework import serializers

from store.models import Store, StorePost, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb',)


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)

    class Meta:
        model = StorePost
        fields = ('post_url', 'post_type', 'post_thumb_image',
                  'post_description', 'post_image_set', )


class StoreSerializer(serializers.ModelSerializer):
    """Serailizer for Store objects"""
    region = serializers.StringRelatedField(many=True)
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    tpo = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_id',
                  'current_ranking',
                  'current_ranking_changed',
                  'insta_url',
                  'profile_image',
                  'region',
                  'primary_style',
                  'secondary_style',
                  'tpo',
                  'age',
                  'facebook_url',
                  'shopee_url',)
        read_only_fields = ('insta_id',
                            'current_ranking',
                            'current_ranking_changed',
                            'insta_url',
                            'profile_image',
                            'region',
                            'primary_style',
                            'secondary_style',
                            'tpo',
                            'age',
                            'facebook_url',
                            'shopee_url')
