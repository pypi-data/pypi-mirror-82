"""
Broadworks OCI-P Interface Exception Classes

Exception classes used by the API.
"""
import attr


@attr.s(slots=True, frozen=True)
class OCIError(Exception):
    """Base Exception raised by OCI operations.

    Attributes:
        message -- explanation of why it went bang
        object -- the thing that went bang
    """

    message = attr.ib(type=str)
    object = attr.ib(default=None)

    def __str__(self):
        return f"{self.__class__.__name__}({self.message})"


class OCIErrorResponse(OCIError):
    pass


class OCIErrorTimeOut(OCIError):
    pass


# end
