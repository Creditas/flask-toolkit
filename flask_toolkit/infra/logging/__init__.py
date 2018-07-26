import logging
from flask_log_request_id import RequestIDLogFilter, current_request_id
from flask_log_request_id.ctx_fetcher import ExecutedOutsideContext
from contextlib import contextmanager


def get_request_id():
    request_id = current_request_id()
    return request_id


def telemetry(**kwargs):
    msg = ''
    for key in kwargs:
        msg += f' {key}={kwargs[key]}'

    logging.info(msg)


def _remove_handler(logger):
    for h in logger.handlers:
        logger.removeHandler(h)


def _stream_handler(logger):
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)


def _setup_outside_handler(logger, outside_handler):
    if outside_handler:
        logger.addHandler(outside_handler)


def _logging_formatter():
    format_out = '%(asctime)s level=%(levelname)s request_id=%(request_id)s %(message)s'
    return logging.Formatter(format_out)


def _setup_formatter(logger):
    formatter = _logging_formatter()
    for h in logger.handlers:
        h.addFilter(RequestIDLogFilter())
        h.setFormatter(formatter)


def _setup_logger(logger, outside_handler=None):
    logger.setLevel(logging.INFO)

    _remove_handler(logger)
    _stream_handler(logger)
    _setup_outside_handler(logger, outside_handler)
    _setup_formatter(logger)


def setup_logging(app, outside_handler=None):
    logger = logging.getLogger()
    _setup_logger(logger, outside_handler)

    logger = app.logger
    _setup_logger(logger)


class RequestIdStore:
    id = None

    def update_id(self, request_id):
        self.id = request_id

    def reset(self):
        self.id = None


request_id_store = RequestIdStore()


def ctx_request_id_store():
    if request_id_store.id is None:
        raise ExecutedOutsideContext()

    return request_id_store.id


current_request_id.register_fetcher(ctx_request_id_store)


@contextmanager
def use_request_id(request_id):
    request_id_store.update_id(request_id)
    yield
    request_id_store.reset()
