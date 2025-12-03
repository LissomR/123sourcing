import json,traceback
from custom_lib.helper import get_error_msg
from django.http import  JsonResponse, response
from rest_framework import status



class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error = str(exception)
        print(error)
        try:
            err_msg,error_code=eval(error)
        except Exception as _:
            err_msg=''
            error_code=error
            if not str(error_code).isdigit():
                err_msg = error_code
        if  str(error_code).isdigit():
            err_msg=err_msg or get_error_msg(error_code)
            standard_status = status.HTTP_400_BAD_REQUEST
            if int(error_code) in [50012,50004]:
                standard_status = status.HTTP_401_UNAUTHORIZED
            response = JsonResponse({"errorCode": int(error_code),"errorMessage":err_msg}, status=standard_status)
        else:
            err_msg=error
            response = JsonResponse({"errorCode": 50001,"errorMessage":"Internal System error, Please try again!"}, status=status.HTTP_400_BAD_REQUEST) #error_code
        if hasattr(request,"logObj"):
            code = 50001
            if str(error_code).isdigit():
                code = error_code
            request.logObj.print_log(message = f"{code} - {err_msg}",level="error",stack_trace=traceback.format_tb(exception.__traceback__))
        
        return response

