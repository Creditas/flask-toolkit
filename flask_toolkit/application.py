from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_log_request_id import RequestID, current_request_id
from .shared.exceptions import (
    ObjectDoesNotExistException, ForbiddenException,
    BadRequestException, InvalidDomainConditions
)
from flask_toolkit.shared.storage import Storage
from .infra.logging import setup_web_logging


def database_health_check(app, db):
    if not db:
        return None
    try:
        db.session.execute('SELECT 1')
    except Exception as error:
        app.logger.error(error)
        raise error


def create_application(config=dict(), db=None, name='app-python', setup_logger=True):
    app = Flask(name)

    app.config.update(config)

    @app.after_request
    def append_request_id(response):
        response.headers.add('X-REQUEST-ID', current_request_id())

        data = request.get_data()
        try:
            data = data.decode('utf-8')
        except:
            pass

        user_agent = request.headers.get('User-Agent', None)
        remote_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        app.logger.info(f'status={response.status} ip={remote_addr} user_agent={user_agent} {data}')

        return response

    @app.route('/health-check')
    def health_check():
        database_health_check(app, db)
        return 'Ok', 200

    @app.errorhandler(404)
    def default_page_not_found(error):
        return 'This page does not exist', 404

    @app.errorhandler(ObjectDoesNotExistException)
    def page_not_found(error):
        return 'This page does not exist', 404

    @app.errorhandler(ForbiddenException)
    def forbidden(error):
        app.logger.error(error)
        return 'This request is forbidden', 403

    @app.errorhandler(BadRequestException)
    def bad_request(error):
        app.logger.error(error)
        return 'Bad request', 400

    @app.errorhandler(InvalidDomainConditions)
    def invalid_domain_conditions(error):
        return jsonify({'errors': [str(error)]}), 422

    @app.errorhandler(Exception)
    def internal_server_error(error):
        app.logger.error(error)
        return 'Something bad happened', 500

    CORS(app)
    RequestID(app)
    if setup_logger:
        setup_web_logging(app)

    if db:
        Migrate(app, db)
        db.init_app(app)
        Storage().setup_instance(db)

    return app
