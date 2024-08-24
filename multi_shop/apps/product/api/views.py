from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from . import serializers
from apps.product import models
class SizeView(ModelViewSet):
    serializer_class = serializers.SizeSerializer
    queryset = models.Size.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)



class ColorView(ModelViewSet):
    serializer_class = serializers.ColorSerializer
    queryset = models.Color.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)



class CategoryView(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.filter(is_publish=True)
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class BrandView(ModelViewSet):
    serializer_class = serializers.BrandSerializer
    queryset = models.Brand.objects.filter(is_publish=True)
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)


class OfferView(ModelViewSet):
    serializer_class = serializers.OfferSerializer
    queryset = models.Offer.objects.filter(is_publish=True)
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class ProductView(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.filter(is_publish=True)
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class ImageView(ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class AdditionalInformationView(ModelViewSet):
    serializer_class = serializers.AdditionalInformationSerializer
    queryset = models.AdditionalInformation.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class QuestionAnswerView(ModelViewSet):
    serializer_class = serializers.QuestionAnswerSerializer
    queryset = models.QuestionAnswer.objects.filter(is_publish=True)
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class LikeView(ModelViewSet):
    serializer_class = serializers.LikeSerializer
    queryset = models.Like.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class CommentView(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    queryset = models.Comment.objects.filter(is_publish=True)
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

