from rest_framework import serializers

from store.models import Store


class StoreSerializer(serializers.ModelSerializer):
    """Serailizer for Store objects"""

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ('id', 'insta_id')
