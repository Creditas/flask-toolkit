class UseCase(object):
    def process_request(self, *args, **kwargs):
        raise NotImplementedError(
            "process_request() not implemented by UseCase class")

    def execute(self, *args, **kwargs):
        try:
            return self.process_request(*args, **kwargs)
        except Exception as e:
            raise e
