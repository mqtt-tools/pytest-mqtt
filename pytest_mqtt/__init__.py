try:
    from importlib.metadata import PackageNotFoundError, version  # noqa
except ImportError:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[no-redef]  # noqa

from .model import MqttMessage  # noqa: F401

try:
    __version__ = version("pytest-mqtt")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
