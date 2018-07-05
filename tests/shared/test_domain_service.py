import pytest
from flask_toolkit.shared import DomainService


def test_domain_service_execute_raising_not_implemented():
    with pytest.raises(NotImplementedError):
        DomainService().execute()
