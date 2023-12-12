from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Payment
from education.serializers import PaymentListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'comment', 'role')


class UserListSerializer(serializers.ModelSerializer):
    this_user_payments = SerializerMethodField()

    def get_this_user_payments(self, obj):
        user_payments = Payment.objects.filter(user=obj)
        return PaymentListSerializer(user_payments, many=True).data

    class Meta:
        model = User
        fields = ('pk', 'email', 'first_name', 'last_name', 'avatar', 'comment', 'this_user_payments', 'role')
