import logging
from sqlalchemy.exc import DataError
from flask_toolkit.shared.exceptions import ObjectDoesNotExistException


class Repository(object):
    _entity = None

    def __iniy__(self):
        from flask_toolkit.application import storage
        self.session = storage.instance.session

    def create(self, entity):
        return self.save(entity)

    def update(self, entity):
        return self.save(entity)

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()

        self.__dispatch_domain_events(entity)

        return entity

    def fetch(self, id, raise_exception=False):
        try:
            return self.query().get(id)
        except DataError:
            if raise_exception:
                raise ObjectDoesNotExistException()
            return None

    def query(self, entity=None):
        if not entity:
            entity = self._entity

        return self.session.query(entity)

    def __dispatch_domain_events(self, entity):
        from app.infra.event_bus import bus
        for event in entity.domain_events:
            logging.info('sent event %s' % event.event_name)
            bus.emit(event.event_name, **event.to_dict())
            entity.remove_domain_event(event)
