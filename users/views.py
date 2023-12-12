from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView

from users.models import User
from users.serializers import UserListSerializer, UserSerializer


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    queryset = User.objects.all()
