from rest_framework.views import APIView
from custom_lib.authentication import UserAuthentication
from custom_lib.custom_mixin import LoggingMixin

class GeneralAPIView(LoggingMixin, APIView):
    permission_classes=()
    authentication_classes = []

class AuthAPIView(LoggingMixin, APIView):
    permission_classes=()
    authentication_classes = [UserAuthentication]