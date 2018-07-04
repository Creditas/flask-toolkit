import pytest
from flask_toolkit import Representer


class CustomRepresenter(Representer):
    class Meta:
        wrapper = 'tests'


def test_representer_render_with_meta_wrapper():
    representer = CustomRepresenter()

    response = representer.render(data={})

    assert response['tests'] == {}


def test_representer_render_with_render_wrapper():
    representer = CustomRepresenter()

    response = representer.render(data={}, wrapper='render_tests')

    assert response['render_tests'] == {}


def test_representer_render_without_wrapper():
    representer = Representer()

    with pytest.raises(NotImplementedError):
        representer.render(data={})
