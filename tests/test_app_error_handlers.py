from flask_toolkit.shared.exceptions import (
    ObjectDoesNotExistException, ForbiddenException, BadRequestException
)


def test_internal_server_error(client, app):
    @app.route('/test-internal-server-error')
    def test_any_exception():
        raise Exception

    response = client.get('/test-internal-server-error')

    assert response.status_code == 500


def test_object_does_not_exist(client, app):
    @app.route('/test-object-does-not-exit')
    def object_does_not_exist():
        raise ObjectDoesNotExistException()

    response = client.get('/test-object-does-not-exit')

    assert response.status_code == 404


def test_forbidden(client, app):
    @app.route('/test-forbidden')
    def forbidden():
        raise ForbiddenException()

    response = client.get('/test-forbidden')

    assert response.status_code == 403


def test_bad_request(client, app):
    @app.route('/test-bad-request')
    def bad_request():
        raise BadRequestException()

    response = client.get('/test-bad-request')

    assert response.status_code == 400
