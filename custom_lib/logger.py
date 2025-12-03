import json,sys
from loguru import logger
from django.conf import settings
from custom_lib.helper import get_client_ip,get_now_time
class BaseLog:    
    def print(self,log,level="info"):
        log_str=" "+str(log)
        try:
            getattr(logger,level)(log_str)
        except Exception as _:
            logger.info(log_str)
class Log(BaseLog):
    def __init__(self,request,app_name,class_name):
        logger.add("logs/app_logs.log", rotation="00:00", retention=f"{settings.LOG_DELETION} days",format="{time:YYYY-MM-DD HH:mm:ss} | {level:} - {message}")
        data={}
        if request:
            method=request.method
            if method=="POST":
                data = request.POST
            elif method=="GET":
                data=request.META.get("QUERY_STRING")
            host_name=request.META.get("HTTP_HOST")
            ip_address=get_client_ip(request)
            port=request.META.get("SERVER_PORT")
            url_path = request.path
        else:
            host_name=''
            ip_address=''
            port=''
            method=''
            url_path=''
        self.data={
            "methodName":method,
            "className":class_name,
            "moduleName":app_name,
            "url":url_path,
            "logTime":str(get_now_time()),
            "data":data,
            "hostName":host_name,
			"ipAddress":ip_address,
			"port":port,
            "message":"START"
        }
        
    def print_log(self, message="", level="info",stack_trace=''):
        dt = self.data
        dt["logTime"] = str(get_now_time().replace(microsecond=0,tzinfo=None))
        dt["message"] = ""
        dt["level"] = level
        if message:
            dt["message"] = message
        if stack_trace:
            stack_trace = ''.join(stack_trace)
        message = stack_trace + json.dumps(dt)
        super().print(message, level)