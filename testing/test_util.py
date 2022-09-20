from pytest_mqtt.util import probe_tcp_connect


def test_probe_tcp_connect_available():
    assert probe_tcp_connect("9.9.9.9", 443) is True


def test_probe_tcp_connect_unavailable():
    assert probe_tcp_connect("9.9.9.9", 444) is False
