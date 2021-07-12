import grpc
from spectroscope.exceptions import NewKeys, NewValidatorList, InterceptorAction
from proto_files.validator import service_pb2, node_pb2, service_pb2_grpc

class RequestValidatorInterceptor(grpc.aio.ServerInterceptor):
    def __init__(self):
        self._terminator = None

    def intercept_service(self, continuation, handler_call_details):
        if 0 == 1: #dummy code 
            return self._terminator
        response = service_pb2.RequestsResult()
        try:
            continuation(handler_call_details)
            response.status=200
            response.count = 0
        except InterceptorAction as action:
            response.status=201
            response.count = 1
            raise NewKeys()
        finally: 
            return response

 