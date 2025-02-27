"""
Serializers for create user API
"""

from django.contrib.auth import get_user_model, authenticate

from django.utils.translation import gettext as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validate_data):
        """Create a new user with validated data"""
        return get_user_model().objects.create_user(**validate_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input__type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate email and password"""

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            msg = _("Unable to authenticate with provided credentialas")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
