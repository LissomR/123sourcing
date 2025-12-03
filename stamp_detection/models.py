from django.db import models
from custom_lib.base_model import BaseFields

# Create your models here.

class SbCompanyList(BaseFields):
    id = models.BigAutoField(primary_key=True)
    stamp_id = models.CharField(unique=True, max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sb_company_list'
