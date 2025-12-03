from django.contrib.auth.mixins import AccessMixin
from custom_lib.logger import Log

class LoggingMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        app_name = self.__module__.split(".")[0]
        class_name = self.__class__.__name__
        log = Log(request, app_name=app_name, class_name=class_name)
        request.logObj = log
        log.print_log("START")
        response = super(LoggingMixin, self).dispatch(request, *args, **kwargs)
        log.print_log("END")
        return response
