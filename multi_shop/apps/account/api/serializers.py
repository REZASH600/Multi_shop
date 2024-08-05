from rest_framework import serializers
from apps.account import models


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.User
        fields = "__all__"

    def get_full_name(self, obj):
        if obj.full_name is not None:
            return obj.full_name()

        return "user is not full name."
