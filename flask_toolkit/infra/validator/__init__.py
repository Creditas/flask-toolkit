import json
from functools import wraps
from flask import request, jsonify, g


def validator_params(validator_class):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            validator_class.clean()
            validator_class.from_request(request)

            if not validator_class.validate():
                return jsonify(success=False, errors=validator_class.errors), 400

            validated_params = validator_class.to_dict()
            g.validated_params = validated_params
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def validate_schema(schema):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            data = json.loads(request.data)

            validated_params, errors = schema.load(data)

            if errors:
                return jsonify(success=False, errors=errors), 400

            g.validated_params = validated_params
            return f(*args, **kwargs)
        return wrapped
    return wrapper
