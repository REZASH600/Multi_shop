from rest_framework.viewsets import ModelViewSet
from apps.account import models
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser
from .pagination import StandardResultsSetPagination


class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (JWTAuthentication,)
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAdminUser,)
    pagination_class = StandardResultsSetPagination
