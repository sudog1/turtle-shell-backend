from rest_framework import serializers
from .models import Brand, Product


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "name",
            "image",
        )


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = (
            "id",
            "SKU",
            "name",
            "image",
            "brand",
        )


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
