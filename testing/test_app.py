from packaging.version import Version
from packaging.version import parse as parse_version

from pytest_mqtt import __version__


def test_app_version():
    assert isinstance(parse_version(__version__), Version)
