try:
    from importlib.metadata import PackageNotFoundError, version  # noqa
except ImportError:  # pragma:nocover
    from importlib_metadata import PackageNotFoundError, version  # noqa

from .model import MqttMessage  # noqa:F401

try:
    __version__ = version("pytest-mqtt")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
