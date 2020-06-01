from django.forms.models import BaseInlineFormSet
from django import forms
from product.models import Product


class ProductFormForInstagramPost(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'sub_category',
            'thumb_image_pk',
            'style',
            'color',
            'original_price',
            'discount_price',
            'size',
            'pattern'
        ]
        raw_id_fields = ['store']


class ProductInlineFormSet(BaseInlineFormSet):
    def save_new_objects(self, commit=True):
        saved_instances = super(ProductInlineFormSet, self).save_new_objects(commit)
        print('try to save new object')
        if commit:
            print(saved_instances[0])
            # create book for press
        return saved_instances
