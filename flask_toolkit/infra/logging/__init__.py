import logging
from flask import request
from flask_log_request_id import RequestIDLogFilter


class ContextualWebFilter(logging.Filter):
    def filter(self, record):
        record.url = request.path
        record.method = request.method

        return True


def setup_web_logging(app):
    format_out = '%(asctime)s level=%(levelname)s transaction_id=%(request_id)s %(method)s %(url)s %(message)s'
    formatter = logging.Formatter(format_out)

    logger = app.logger
    logger.setLevel(logging.DEBUG)

    for h in logger.handlers:
        h.addFilter(RequestIDLogFilter())
        h.addFilter(ContextualWebFilter())
        h.setFormatter(formatter)
