import pytest
from flask_toolkit.application import create_application


@pytest.fixture(scope='function')
def app(request):
    application = create_application()
    context = application.app_context()

    def teardown():
        context.pop()

    request.addfinalizer(teardown)
    context.push()

    return application


@pytest.fixture(scope='function')
def client(request, app):
    client = app.test_client()
    return client
