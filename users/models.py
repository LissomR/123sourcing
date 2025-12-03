from django.db import models
from custom_lib.base_model import BaseFields,USER_TYPE_CHOICES,USER_STATUS_CHOICES


class UserModel(BaseFields):
    user_id = models.BigAutoField(primary_key=True)
    user_type = models.CharField(max_length=8,choices=USER_TYPE_CHOICES,default='SUPER_BO')
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    status = models.CharField(max_length=9,choices=USER_STATUS_CHOICES,default='ACTIVE')
    password = models.CharField(max_length=100)
    mobile_code = models.CharField(max_length=10, blank=True, null=True)
    mobile_no = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email_id = models.CharField(unique=True, max_length=100)
    address_one = models.CharField(max_length=250,  blank=True, null=True)
    address_two = models.CharField(max_length=250,  blank=True, null=True)
    city_code = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=50,  blank=True, null=True)
    state_code = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=50,  blank=True, null=True)
    country_code = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50,  blank=True, null=True)
    zip = models.CharField(max_length=20,  blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sb_users'

class UsersTokenModel(BaseFields):
    id = models.AutoField(primary_key=True)
    user_id= models.IntegerField()
    token = models.CharField(max_length=500, blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sb_users_token' 