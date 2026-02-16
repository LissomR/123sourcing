from rest_framework import authentication
from django.conf import settings


class APIKeyAuthentication(authentication.BaseAuthentication):
    """
    Simple API Key authentication.
    Expects header: X-API-Key: <key>
    The key is validated against the API_KEY environment variable.
    """
    def authenticate(self, request):
        api_key = request.headers.get("X-Api-Key", "")

        if not api_key:
            raise ValueError(50012)

        if api_key != settings.API_KEY:
            raise ValueError(50012)

        return (None, None)