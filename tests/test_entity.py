import pytest
from flask_toolkit import Entity


def test_setter_attributes():
    class Foo(Entity):
        bar = None

    foo = Foo(bar='foo')

    assert foo.bar == 'foo'


def test_does_not_setter_attributes_when_attribute_is_not_presence():
    class Foo(Entity):
        pass

    foo = Foo(bar='foo')

    with pytest.raises(AttributeError):
        foo.bar


def test_does_not_share_reference():
    class Foo(Entity):
        pass

    class Bar(Entity):
        pass

    foo = Foo()
    foo.add_domain_event('foo')

    bar = Bar()

    assert len(foo.domain_events) == 1
    assert len(bar.domain_events) == 0


def test_add_domain_events():
    class Foo(Entity):
        pass

    foo = Foo()
    foo.add_domain_event('foo')
    foo.add_domain_event('bar')

    assert foo.domain_events[0] == 'foo'
    assert foo.domain_events[1] == 'bar'


def test_remove_domain_events():
    class Foo(Entity):
        pass

    foo = Foo()
    foo.add_domain_event('foo')
    foo.add_domain_event('bar')

    foo.remove_domain_event('foo')

    assert foo.domain_events[0] == 'bar'


def test_representation():
    class Foo(Entity):
        a = None
        b = None

    foo = Foo(a=1, b=2)

    assert foo.__repr__() == '<Foo(a=1, b=2)>'
