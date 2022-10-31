class BaseServiceError(Exception):
    code = 500


class ItemNotFound(BaseServiceError):
    code = 404


class MethodNotAllowed(BaseServiceError):
    code = 405


class UnsuitableData(BaseServiceError):
    code = 405


class AlreadyExists(BaseServiceError):
    code = 303


class CondlictError(BaseServiceError):
    code = 409

