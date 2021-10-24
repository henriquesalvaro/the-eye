"""
Accounts - API V1 User Serializers
"""
from django.contrib.auth import get_user_model
from rest_auth.models import TokenModel
from rest_framework import serializers

User = get_user_model()


###
# Serializers
###
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = (
            "id",
            "username",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UserTokenSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()

    class Meta:
        model = TokenModel
        fields = (
            "key",
            "user",
        )
