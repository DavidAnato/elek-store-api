from rest_framework import serializers
from .models import Category, Brand, Product, AdditionalImage, KeyWord, ProductRating

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class AdditionalImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalImage
        fields = '__all__'

class KeyWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyWord
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    additional_image_set = AdditionalImageSerializer(many=True, read_only=True)
    keyword_set = KeyWordSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductRating
        fields = ['product', 'rating']
