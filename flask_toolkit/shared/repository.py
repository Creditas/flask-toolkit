import logging
from flask_toolkit.infra.domain_event import bus
from flask_toolkit.shared.exceptions import ObjectDoesNotExistException
from sqlalchemy.exc import DataError
from sqlalchemy.orm.base import _entity_descriptor
from sqlalchemy.sql import extract, operators
from sqlalchemy.util import to_list
from .storage import Storage


class Repository(object):
    _entity = None

    __filter_operators__ = {
        'contains': operators.contains_op,
        'day': lambda c, x: extract('day', c) == x,
        'endswith': operators.endswith_op,
        'exact': operators.eq,
        'gt': operators.gt,
        'gte': operators.ge,
        'iendswith': lambda c, x: c.ilike('%' + x.replace('%', '%%')),
        'iexact': operators.ilike_op,
        'in': operators.in_op,
        'isnull': lambda c, x: x and c != None or c == None,
        'istartswith': lambda c, x: c.ilike(x.replace('%', '%%') + '%'),
        'le': operators.le,
        'lte': operators.lt,
        'month': lambda c, x: extract('month', c) == x,
        'range': operators.between_op,
        'startswith': operators.startswith_op,
        'year': lambda c, x: extract('year', c) == x,
    }

    def __init__(self):
        try:
            self.session = Storage().session
        except Exception as e:
            print('You need setup instance for your storage')

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

    def filter(self, **kwargs):
        return self._filter_or_exclude(negate=False, kwargs=kwargs)

    def exclude(self, **kwargs):
        return self._filter_or_exclude(negate=True, kwargs=kwargs)

    def _filter_or_exclude(self, negate, kwargs):
        q = self.query()
        negate_if = lambda expr: expr if not negate else ~expr
        column = None
        for arg, value in kwargs.items():
            for token in arg.split('__'):
                if column is None:
                    column = _entity_descriptor(q._joinpoint_zero(), token)
                    if column.impl.uses_objects:
                        q = q.join(column)
                        column = None
                elif token in self.__filter_operators__:
                    op = self.__filter_operators__[token]
                    q = q.filter(negate_if(op(column, *to_list(value))))
                    column = None
                else:
                    raise ValueError('No idea what to do with %r' % token)
            if column is not None:
                q = q.filter(negate_if(column == value))
                column = None
            q = q.reset_joinpoint()
        return q

    def __dispatch_domain_events(self, entity):
        for event in entity.domain_events:
            logging.info('sent event %s' % event.event_name)
            bus.emit(event.event_name, **event.to_dict())
            entity.remove_domain_event(event)
