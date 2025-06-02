from rest_framework import serializers
from .models import (
    ProductCategory,
    Product,
    ProductParams,
    ProductPhoto,
    ParserHistory,
)

class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ("id", "name")


class ProductParamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParams
        fields = ("name", "value")


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ("photo_url",)


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer(read_only=True)
    photos   = ProductPhotoSerializer(
        many=True,
        read_only=True,
        source="product_photos",
    )
    params   = ProductParamSerializer(
        many=True,
        read_only=True,
        source="product_params",
    )

    class Meta:
        model  = Product
        fields = ("id", "name", "category", "articul", "url", "photos", "params")


class ParserHistorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model  = ParserHistory
        fields = ("id", "articul", "is_completed", "product")
