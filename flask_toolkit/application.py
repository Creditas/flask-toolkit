from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from flask_log_request_id import RequestID, current_request_id

from flask_toolkit.shared.exceptions import ObjectAlreadyExistException
from .shared.exceptions import (
    ObjectDoesNotExistException, ForbiddenException,
    BadRequestException, InvalidDomainConditions
)
from flask_toolkit.shared.storage import Storage
from .infra.logging import setup_logging, telemetry


def create_application(name='app-python', config=dict(), db=None, config_logging=dict()):
    app = Flask(name)

    app.config.update(config)

    @app.after_request
    def append_request_id(response):
        response.headers.add('X-REQUEST-ID', current_request_id())

        data = request.get_data()
        try:
            data = data.decode('utf-8')
        except Exception as e:
            pass

        user_agent = request.headers.get('User-Agent', None)
        remote_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

        telemetry(
            method=request.method,
            path=request.path,
            args=request.args.to_dict(),
            status=response.status,
            ip=remote_addr,
            user_agent=user_agent,
            payload=data
        )

        return response

    @app.errorhandler(404)
    def default_page_not_found(error):
        return 'This page does not exist', 404

    @app.errorhandler(ObjectDoesNotExistException)
    def page_not_found(error):
        return 'This page does not exist', 404

    @app.errorhandler(ObjectAlreadyExistException)
    def page_not_found(error):
        return 'This object already exists', 409

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

    CORS(app)
    RequestID(app)

    if config_logging:
        setup_logging(app, config_logging)

    if db:
        Migrate(app, db)
        db.init_app(app)
        Storage().setup_instance(db)

    return app
