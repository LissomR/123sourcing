from custom_lib.api_view_class import GeneralAPIView
from rest_framework.response import Response
from users.serializers import UserRegistrationSerializer,UserLoginSerializer, SignupResponseFormatSerializer, LoginResponseFormatSerializer
from custom_lib.helper import get_now_time, hash_password, check_password
from datetime import timedelta
from django.conf import settings
import jwt
from custom_lib.decorators import swagger_auto_schema_with_serializer_validation
from users.models import UserModel, UsersTokenModel


class UserRegistrationView(GeneralAPIView):
    @swagger_auto_schema_with_serializer_validation(
        tags = ['User'],
        request_body = UserRegistrationSerializer,
        operation_id="SIGNUP API",
        security=[],
        responses={200: SignupResponseFormatSerializer, 400: 'Bad Request'}
    )
    def post(self,request):
        data = request.data
        data.setdefault("status", "ACTIVE")
        data.setdefault("user_type", "SUPER_BO")
        exist_user = UserModel.objects.filter(email_id=data.get('email_id'))
        if exist_user.exists():
            raise ValueError(50005)
        data['password'] = hash_password(data['password'])
        user_obj = UserModel.objects.create(**data)
        user_id = user_obj.pk
        return Response({"userId":user_id}, status=201)


class UserLoginView(GeneralAPIView):
    @swagger_auto_schema_with_serializer_validation(
        tags=["User"],
        request_body=UserLoginSerializer,
        operation_id="LOGIN API",
        security=[],
        responses={200: LoginResponseFormatSerializer, 401: 'Unauthorized', 400: 'Bad Request'}
        )
    def post(self,request):
        data = request.data
        user = UserModel.objects.filter(email_id=data['email_id'])
        if not user.exists() or not check_password(data['password'], user.first().password):
            raise ValueError(50004)
        user = user.first()
        user_id = user.user_id
        ct = get_now_time()
        exp_time = ct + timedelta(minutes=int(settings.AUTH_TOKEN_EXPIRE_TIME))
        payload = {
            'userId': user_id,
            'iat': int(get_now_time().timestamp()),
            'exp': int(exp_time.timestamp())
        }
        token = jwt.encode(payload, settings.JWT_AUTH_SECRET, algorithm='HS256')
        obj, _ = UsersTokenModel.objects.update_or_create(user_id=user_id, defaults={"token": token, "expire_at": exp_time})
        db_exp_time = obj.expire_at

        return Response({"token": token, "userId": user_id, "expireAt": db_exp_time, "firstName": user.first_name, "lastName": user.last_name}, status=200)