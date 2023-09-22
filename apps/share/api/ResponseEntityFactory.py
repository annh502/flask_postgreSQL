from werkzeug.exceptions import Unauthorized, BadRequest, InternalServerError
from . import ResponseBody

class ResponseEntityFactory:
    def unauthorized(unauthorized):
        response_body = ResponseBody("You are not authorized to use this service","UNAUTHORIZED", None )
        return response_body, 401
    def bad_request(badRequest):
        response_body = ResponseBody("The browser sent a request that this server could not understand","BAD REQUEST", None )
        return response_body, 400
    def ok(data):
        response_body = ResponseBody("Success","SUCCESS", data )
        return response_body, 200
    def internal_server_error(internalServerError):
        response_body = ResponseBody("System error!","INTERNAL SERVER ERROR", None )
        return response_body, 501