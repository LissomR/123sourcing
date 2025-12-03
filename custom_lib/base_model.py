from django.db import models
from rest_framework import serializers
import numbers
from custom_lib.helper import snake_to_camel,camel_case_to_snake_case

class BaseOutputSerializer(serializers.Serializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        non_null_ret = {}
        for key in ret.keys():
            if ret[key] or isinstance(ret[key], numbers.Number):
                non_null_ret[snake_to_camel(key)] = ret[key]
        return non_null_ret

class BaseInputSerializer(serializers.Serializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        non_null_ret = {}
        for key in ret.keys():
            if ret[key] or isinstance(ret[key], numbers.Number):
                non_null_ret[camel_case_to_snake_case(key)] = ret[key]
        return non_null_ret

class BaseFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

USER_TYPE_CHOICES = (
    ('SUPER_BO', 'SUPER_BO'),
    ('BO', 'BO'),
)
STATUS_CHOICES = (
    ('ACTIVE', 'ACTIVE'),
    ('INACTIVE', 'INACTIVE')
)

USER_STATUS_CHOICES = STATUS_CHOICES + (('TERMINATE','TERMINATE'),)

FREQUENCY_CHOICES = (
    ('week', 'week'),
    ('month', 'month')
)


class StateField(models.Model):
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    class Meta:
        abstract = True
