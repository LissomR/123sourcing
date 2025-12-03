from custom_lib.base_model import BaseInputSerializer
from rest_framework import serializers

class UserLoginSerializer(BaseInputSerializer):
    emailId = serializers.EmailField(required=True,allow_blank=False,allow_null=False)
    password = serializers.CharField(required=True,allow_blank=False,allow_null=False)

class UserRegistrationSerializer(UserLoginSerializer):
    firstName = serializers.CharField(required=True)
    lastName = serializers.CharField()


class UserSignupDataSerializer(serializers.Serializer):
    userId = serializers.IntegerField()


class SignupResponseFormatSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()
    errorMessage = serializers.CharField()
    data = UserSignupDataSerializer()


class UserLoginDataSerializer(serializers.Serializer):
    token = serializers.CharField()
    userId = serializers.IntegerField()
    expireAt = serializers.CharField()
    firstName = serializers.CharField()
    lastName = serializers.CharField()


class LoginResponseFormatSerializer(serializers.Serializer):
    errorCode = serializers.IntegerField()
    errorMessage = serializers.CharField()
    data = UserLoginDataSerializer()