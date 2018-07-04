import json


class PayloadWrap:
    _payload = dict()

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = json.loads(payload)
        else:
            self._payload = payload

    def to_json(self):
        return json.dumps(self._payload)
