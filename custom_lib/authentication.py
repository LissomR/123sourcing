from rest_framework import authentication
from django import db
from django.conf import settings
from custom_lib.helper import get_now_time
import jwt
from users.models import UsersTokenModel,UserModel
from jwt import ExpiredSignatureError

class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = None
        try:
            db.connections.close_all()
            authorize = request.headers.get("Authorization", "")

            if not authorize.startswith("Bearer "):
                raise ValueError(50012)
            
            token = authorize.split("Bearer ")[1]

            if not token:
                raise ValueError(50012)
            try:
                payload = jwt.decode(token,settings.JWT_AUTH_SECRET,algorithms=['HS256'])
            except ExpiredSignatureError:
                raise ValueError(50011)
            except Exception as _:
                raise ValueError(50012)
            user_id = payload['userId']
            user_obj=UserModel.objects.filter(user_id=user_id,status="ACTIVE")
            if not user_obj.exists():
                raise ValueError(50013)
            user_token = UsersTokenModel.objects.filter(user_id=user_id,token=token,expire_at__gt=get_now_time())
            if not user_token.exists():
                raise ValueError(50011)
            request.user_id = user_id
            return (user_obj.first(),None)
        except ValueError as e:
            raise ValueError(str(e))