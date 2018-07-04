import abc


class DomainEvent(abc.ABC):

    @property
    @abc.abstractmethod
    def event_name(self):
        raise NotImplementedError('event_name not implementend')

    def to_dict(self):
        return self.__dict__
