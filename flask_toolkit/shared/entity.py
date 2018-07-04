class Entity:

    def __init__(self, **kwargs):
        self._domain_events = []
        for key in kwargs:
            if hasattr(self, key):
                setattr(self, key, kwargs[key])

    def add_domain_event(self, event):
        self.domain_events.append(event)

    def remove_domain_event(self, event):
        self.domain_events.remove(event)

    @property
    def domain_events(self):
        if not hasattr(self, '_domain_events'):
            self._domain_events = []

        return self._domain_events

    def __repr__(self):
        attributes = sorted(self.__dict__.items(), key=lambda tuple_: tuple_[0])
        attributes = [f'{key}={value!r}' for key, value in attributes if not key.startswith('_')]
        return f'<{self.__class__.__name__}({", ".join(attributes)})>'
