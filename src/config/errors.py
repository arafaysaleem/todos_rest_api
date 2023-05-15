class ApiException(Exception):
    def __init__(self, message: str, code: int, payload=None):
        super().__init__()
        self.message = message
        self.code = code
        self.payload = payload

class NotFoundException(ApiException):
    def __init__(self, message="Resource not found"):
        code = 404
        super().__init__(message, code)

class DuplicateException(ApiException):
    def __init__(self, message = "Resource already exists"):
        code = 409
        super().__init__(message, code)

class ValidationException(ApiException):
    def __init__(self, errors):
        message = "The request body is invalid"
        code = 422
        super().__init__(message, code, errors)

class UnauthorizedException(ApiException):
    def __init__(self):
        message = "The request is unauthorized"
        code = 401
        super().__init__(message, code)