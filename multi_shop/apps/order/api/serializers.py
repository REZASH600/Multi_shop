from rest_framework import serializers
from apps.order import models


class ProvinceSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Province
        fields = "__all__"


class CitySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = "__all__"


class AddressSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = "__all__"
