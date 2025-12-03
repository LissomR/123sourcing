from django.conf import settings
from datetime import datetime
from drf_yasg import openapi
import re,threading
from multiprocessing import Process
import pandas as pd
import bcrypt


error_code = settings.ERROR_JSON


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

def check_password(raw_password, hashed_password):
    return bcrypt.checkpw(raw_password.encode(), hashed_password.encode())

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_error_msg(code=0):
    return error_code.get(str(code), "Something went wrong")

def valid_serializer(serializer):
    if serializer.is_valid():
        return serializer.data
    for x, y in serializer.errors.items():
        error = str(x)+' : '+str(y)
        raise ValueError(error)

def get_now_time():
    return datetime.now()


def snake_to_camel(col):
    return "".join(
            x if i == 0 else x.capitalize() for i, x in enumerate(col.split("_"))
        )


def camel_case_to_snake_case(str):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def create_swagger_params(name, required=True, type='string',header_type="header",extra={}):
    swagger_type = openapi.TYPE_STRING
    header = openapi.IN_HEADER
    if type == "int":
        swagger_type = openapi.TYPE_INTEGER
    elif type == "bool":
        swagger_type = openapi.TYPE_BOOLEAN
    
    if header_type=="query":
        header=openapi.IN_QUERY
    return openapi.Parameter(name, header, type=swagger_type, required=required,**extra)


def run_process_parallel(*fns):
    proc=[]
    for fn in fns:
        p = Process(target=fn["func"])
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def run_thread(func):
    thread = threading.Thread(target=func, args=())
    thread.start()

def get_month_name_mapping(start_date,end_date):
    if not start_date or not end_date:
        return {}
    lbl_df = pd.DataFrame([])
    lbl_df['date'] = pd.date_range(
        start=start_date, end=end_date, freq='M')
    lbl_df['month'] = lbl_df['date'].dt.month
    lbl_df['month_name'] = lbl_df['date'].dt.month_name()
    return dict(zip(lbl_df['month'],lbl_df['month_name']))