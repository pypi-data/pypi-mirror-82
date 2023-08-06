from mms.base_logger import BaseLogger
from google.cloud.logging.resource import Resource


class CloudFunctionLogger(BaseLogger):

    def __init__(self, service_name: str, trace_id: str, project_id: str, function_name: str, local_run=False):
        super().__init__(service_name=service_name,
                         run_id=trace_id,
                         project_id=project_id)
        self.function_name = function_name
        self.local_run = local_run
        self.res = Resource(type='cloud_function', labels={
            "project_id": super().get_project_id(),
            "function_name": self.function_name,
        })
        self.logger = super().create_logger()

    def update_trace_id(self, new_trace_id):
        super().update_trace_id(new_trace_id=new_trace_id)

    def info(self, message):
        super().do_log(message='MMS-INFO: {}'.format(message),
                       severity='INFO',
                       res=self.res,
                       local_run=self.local_run,
                       logger=self.logger)

    def warning(self, message):
        super().do_log(message='MMS-WARNING: {}'.format(message),
                       severity='WARNING',
                       res=self.res,
                       local_run=self.local_run,
                       logger=self.logger)

    def error(self, message):
        super().do_log(message='MMS-ERROR: {}'.format(message),
                       severity='ERROR',
                       res=self.res,
                       local_run=self.local_run,
                       logger=self.logger)

    def critical(self, message):
        super().do_log(message='MMS-CRITICAL: {}'.format(message),
                       severity='CRITICAL',
                       res=self.res,
                       local_run=self.local_run,
                       logger=self.logger)

    def debug(self, message):
        super().do_log(message='MMS-DEBUG: {}'.format(message),
                       severity='DEBUG',
                       res=self.res,
                       local_run=self.local_run,
                       logger=self.logger)

