import typing


__all__ = (
    "NoReverseMatch",
    "NoCodecAvailable",
    "ConfigurationError",
    "HTTPException",
    "Found",
    "BadRequest",
    "AuthenticationError",
    "Forbidden",
    "NotFound",
    "MethodNotAllowed",
    "NotAcceptable",
    "UnsupportedMediaType",
    "DecodeError",
)


class NoReverseMatch(Exception):
    """
    Raised by a Router when `reverse_url` is passed an invalid handler name.
    """


class NoCodecAvailable(Exception):
    """
    Raised when there is no suitable codec.
    """


class ConfigurationError(Exception):
    """
    Raised when wrong configuration is specified.
    """


class DecodeError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


# HTTP exceptions
class HTTPException(Exception):
    default_status_code: int
    default_detail: str

    def __init__(
        self,
        detail: typing.Union[str, typing.Mapping[str, object], None] = None,
        status_code: typing.Optional[int] = None,
    ) -> None:
        self.detail = self.default_detail if (detail is None) else detail
        self.status_code = (
            self.default_status_code if (status_code is None) else status_code
        )

    def get_headers(self) -> typing.Dict[str, str]:
        return {}


class Found(HTTPException):
    default_status_code = 302
    default_detail = "Found"

    def __init__(
        self,
        location: str,
        detail: typing.Union[None, str, typing.Mapping[str, object]] = None,
        status_code: typing.Optional[int] = None,
    ) -> None:
        self.location = location
        super().__init__(detail, status_code)

    def get_headers(self) -> typing.Dict[str, str]:
        return {"Location": self.location}


class BadRequest(HTTPException):
    default_status_code = 400
    default_detail = "Bad request"


class AuthenticationError(HTTPException):
    default_status_code = 401
    default_detail = "Unauthorized"


class Forbidden(HTTPException):
    default_status_code = 403
    default_detail = "Forbidden"


class NotFound(HTTPException):
    default_status_code = 404
    default_detail = "Not found"


class MethodNotAllowed(HTTPException):
    default_status_code = 405
    default_detail = "Method not allowed"


class NotAcceptable(HTTPException):
    default_status_code = 406
    default_detail = "Could not satisfy the request Accept header"


class Conflict(HTTPException):
    default_status_code = 409
    default_detail = "Conflict"


class UnsupportedMediaType(HTTPException):
    default_status_code = 415
    default_detail = "Unsupported Content-Type header in request"
