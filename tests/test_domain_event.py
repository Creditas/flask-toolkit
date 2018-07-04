import pytest
from flask_toolkit.shared import DomainEvent


def test_raise_when_event_name_is_not_implemented():
    class Foo(DomainEvent):
        pass

    with pytest.raises(TypeError):
        Foo()


def test_does_not_raise_when_event_name_is_implemented():
    class Foo(DomainEvent):
        event_name = 'domain:event_name'

    assert Foo().event_name == 'domain:event_name'
