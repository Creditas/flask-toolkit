class DomainService:
    def process_request(self, *args, **kwargs):
        raise NotImplementedError(
            "process_request() not implemented by DomainService class")

    def execute(self, *args, **kwargs):
        return self.process_request(*args, **kwargs)
