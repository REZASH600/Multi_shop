from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from . import serializers
from apps.order import models



class ProvinceView(ModelViewSet):
    serializer_class = serializers.ProvinceSerializers
    queryset = models.Province.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)


class CityView(ModelViewSet):
    serializer_class = serializers.CitySerializers
    queryset = models.City.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)

class AddressView(ModelViewSet):
    serializer_class = serializers.AddressSerializers
    queryset = models.Address.objects.all()
    parser_classes = (MultiPartParser,)
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAdminUser,)
