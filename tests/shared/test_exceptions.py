from flask_toolkit.shared.exceptions import (
    ObjectDoesNotExistException, ForbiddenException, BadRequestException
)


def test_object_does_not_exist_exception():
    exception = ObjectDoesNotExistException()

    assert exception


def test_forbidden_exception():
    exception = ForbiddenException()

    assert exception


def test_bad_request_exception():
    exception = BadRequestException()

    assert exception
