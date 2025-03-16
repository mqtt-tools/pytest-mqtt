from pytest_mqtt.util import probe_tcp_connect


def test_probe_tcp_connect_available(httpserver):
    assert probe_tcp_connect(httpserver.host, httpserver.port) is True


def test_probe_tcp_connect_unavailable():
    assert probe_tcp_connect("localhost", 12345) is False
