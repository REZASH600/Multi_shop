from rest_framework import serializers
from apps.product import models


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Size
        fields = "__all__"


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Color
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    subs = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all(), allow_null=True, required=False)
    products = serializers.SlugRelatedField(source='product_category', slug_field='name', many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Offer
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=12, decimal_places=2, write_only=True)
    formatted_price = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = "__all__"

    def get_formatted_price(self, obj):
        return obj.formatted_price


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = "__all__"


class AdditionalInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdditionalInformation
        fields = "__all__"


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuestionAnswer
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"



class CouponCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CouponCode
        fields = "__all__"
